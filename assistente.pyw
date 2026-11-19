import difflib
import json
import os
import re
import subprocess
import webbrowser
from pathlib import Path

import sounddevice as sd
import speech_recognition as sr

# settings
LANGUAGE = "pt_br"        # change to your language
OPEN_WORDS = ("open", "abrir", "abra", "abre") # change to your language
USE_WAKE_WORD = False     
WAKE_WORDS = ("hey claude", "hey cloud", "hey clod", "ei claude")
LISTEN_SECONDS = 4
SAMPLE_RATE = 16000
MATCH_CUTOFF = 0.6        
CONFIG_FILE = Path(__file__).with_name("commands.json")

START_MENU_DIRS = [
    Path(os.environ.get("ProgramData", "")) / "Microsoft/Windows/Start Menu/Programs",
    Path(os.environ.get("APPDATA", "")) / "Microsoft/Windows/Start Menu/Programs",
]
IGNORE_WORDS = ("uninstall", "desinstalar", "readme", "license", "help")


# command list
def scan_start_menu():
    apps = {}
    for folder in START_MENU_DIRS:
        if not folder.is_dir():
            continue
        for lnk in folder.rglob("*.lnk"):
            name = lnk.stem.lower()
            if any(word in name for word in IGNORE_WORDS):
                continue
            apps[name] = str(lnk)
    return apps


def load_config():
    if not CONFIG_FILE.exists():
        return {}
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return json.load(f)


def build_targets():
    config = load_config()
    targets = {name: ("file", path) for name, path in scan_start_menu().items()}

    for name, path in config.get("folders", {}).items():
        targets[name.lower()] = ("file", os.path.expandvars(path))
    for name, url in config.get("sites", {}).items():
        targets[name.lower()] = ("url", url)
    for name, cmd in config.get("programs", {}).items():
        targets[name.lower()] = ("cmd", [os.path.expandvars(p) for p in cmd])
    for alias, real in config.get("aliases", {}).items():
        if real.lower() in targets:
            targets[alias.lower()] = targets[real.lower()]
    return targets


# voice
def listen(seconds=LISTEN_SECONDS):
    audio = sd.rec(int(seconds * SAMPLE_RATE), samplerate=SAMPLE_RATE,
                   channels=1, dtype="int16")
    sd.wait()
    data = sr.AudioData(audio.tobytes(), SAMPLE_RATE, 2)
    try:
        return sr.Recognizer().recognize_google(data, language=LANGUAGE).lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("No internet or voice service available.")
        return ""


def strip_wake_word(text):
    for word in WAKE_WORDS:
        if word in text:
            return True, text.replace(word, "", 1).strip()
    return False, text


# interpretation
def extract_command(text):
    pattern = r"\b(?:" + "|".join(OPEN_WORDS) + r")\b\s+(.+)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None


def find_target(phrase, targets):
    contained = [name for name in targets if len(name) >= 3 and name in phrase] # exact name
    if contained:
        return max(contained, key=len)
    close = difflib.get_close_matches(phrase, targets.keys(), n=1, cutoff=MATCH_CUTOFF) # approximate name
    return close[0] if close else None


def open_target(kind, value):
    if kind == "url":
        webbrowser.open(value)
    elif kind == "cmd":
        subprocess.Popen(value)
    else:
        os.startfile(value)  # Windows only


def handle(text, targets):
    phrase = extract_command(text)
    if phrase is None:
        print(f"I didn't hear a command to open. I heard: '{text}'")
        return
    name = find_target(phrase, targets)
    if not name:
        print(f"I didn't find any app similar to '{phrase}'.")
        return
    kind, value = targets[name]
    print(f"Opening {name}...")
    try:
        open_target(kind, value)
    except OSError as error:
        print(f"I couldn't open {name}: {error}")


def main():
    targets = build_targets()
    print(f"{len(targets)} apps, folders and loaded sites.")
    while True:
        print("Listening...")
        text = listen()
        if not text:
            continue
        print("You said:", text)

        if USE_WAKE_WORD:
            heard, text = strip_wake_word(text)
            if not heard:
                continue
            if not text:
                print("You can speak:")
                text = listen()
                print("You said:", text)

        handle(text, targets)


if __name__ == "__main__":
    main()
