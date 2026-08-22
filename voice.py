"""
ThanviLang Voice Module
Voice input/output integration for ThanviLang.
"""

import sys


def speak(text: str):
    """
    Output text that can be connected to a
    text-to-speech engine later.
    """
    print(f"[Thanvi Voice] {text}")


def listen():
    """
    Placeholder for voice input.

    The browser/mobile interface can provide
    speech-to-text and send the resulting text
    to ThanviLang.
    """
    try:
        text = input("[Voice Input] ")
        return text.strip()
    except (EOFError, KeyboardInterrupt):
        return ""


def process_voice_command(command: str):
    """
    Process a voice command received by ThanviLang.
    """
    command = command.strip()

    if not command:
        return ""

    print(f"[Thanvi Voice Command] {command}")
    return command


if __name__ == "__main__":
    command = listen()

    if command:
        result = process_voice_command(command)
        speak(f"You said: {result}")
