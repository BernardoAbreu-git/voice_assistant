# Voice Assistant

[Versão em português abaixo](#assistente-de-voz-português) (ignore this if you don't speak portuguese)

A Python script for Windows that opens apps, folders and websites by voice. Say "open Spotify" and it opens.

## How it works

It records a few seconds from your microphone, turns the speech into text with Google's speech recognition, and looks for what you said in a list of targets.

The list is built when the program starts. It reads the shortcuts from the Windows Start Menu, so most installed apps work without any setup. Websites, folders, programs that need arguments and nicknames go in `commands.json`.

If the name you said is not exact, it picks the closest one. "visual studio" finds "Visual Studio Code".

## Setup

You need Python 3 on Windows.

```
pip install -r requirements.txt
python assistente.py
```

When it prints `Listening...`, say "open" and the name of the app, for example "open discord". It listens in 4 second windows, so speak right after the message shows up.

## Settings

At the top of `assistente.py`:

- `LANGUAGE`: language of the speech recognition. `"en-US"` for English, `"pt-BR"` for Portuguese.
- `OPEN_WORDS`: the words that start a command.
- `USE_WAKE_WORD`: if `True`, it only reacts after you say "hey claude".
- `MATCH_CUTOFF`: from 0 to 1. Higher means the name has to be closer. If it opens the wrong app, raise it. If it can't find what you said, lower it.

## commands.json

Add what the Start Menu doesn't have:

- `sites`: name and URL, opened in your default browser.
- `folders`: name and path.
- `programs`: name and the full command, for things that need arguments.
- `aliases`: another name for something that already exists, useful when the recognition keeps hearing a different word.

## Limitations

- Windows only.
- Needs internet for the speech recognition.
- The wake word is simple and works inside the same 4 second windows.

## Ideas for later

- Answer questions with an AI.
- Offline speech recognition.
- A wake word that listens continuously.

---

# Assistente de Voz (Português)

Um script em Python para Windows que abre aplicativos, pastas e sites por comando de voz. Diga "open Spotify" e ele abre.

## Como funciona

Ele grava alguns segundos do microfone, transforma a fala em texto com o reconhecimento de voz do Google e procura o que você falou numa lista de alvos.

A lista é montada quando o programa começa. Ele lê os atalhos do Menu Iniciar do Windows, então a maioria dos apps instalados funciona sem configurar nada. Sites, pastas, programas que precisam de argumentos e apelidos ficam no `commands.json`.

Se o nome que você falou não for exato, ele escolhe o mais parecido. "visual studio" encontra "Visual Studio Code".

## Instalação

Você precisa do Python 3 no Windows.

```
pip install -r requirements.txt
python assistente.py
```

Quando aparecer `Listening...`, diga "open" e o nome do app, por exemplo "open discord". Ele escuta em janelas de 4 segundos, então fale logo depois que a mensagem aparecer.

## Configurações

No topo do `assistente.py`:

- `LANGUAGE`: idioma do reconhecimento de voz. `"en-US"` para inglês, `"pt-BR"` para português.
- `OPEN_WORDS`: as palavras que iniciam um comando.
- `USE_WAKE_WORD`: se for `True`, ele só reage depois de você dizer "hey claude".
- `MATCH_CUTOFF`: de 0 a 1. Quanto maior, mais parecido o nome precisa ser. Se ele abrir o app errado, aumente. Se não achar o que você falou, diminua.

## commands.json

Adicione o que o Menu Iniciar não tem:

- `sites`: nome e URL, abertos no seu navegador padrão.
- `folders`: nome e caminho.
- `programs`: nome e o comando completo, para o que precisa de argumentos.
- `aliases`: outro nome para algo que já existe, útil quando o reconhecimento entende sempre uma palavra diferente.

## Limitações

- Só funciona no Windows.
- Precisa de internet para o reconhecimento de voz.
- A palavra de ativação é simples e funciona dentro das mesmas janelas de 4 segundos.

## Ideias para depois

- Responder perguntas usando uma IA.
- Reconhecimento de voz offline.
- Uma palavra de ativação que escuta o tempo todo.
