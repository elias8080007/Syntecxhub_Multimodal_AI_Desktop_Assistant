# Multimodal AI Desktop Assistant

Syntecxhub Artificial Intelligence Internship  
Final Task – End-to-End AI Capstone Project  
Developed by Elias Ibrahim Elias

## Project Overview

This project is a multimodal AI desktop assistant that combines a face-detection access gate, voice recognition, typed commands, spoken responses and safe Windows command execution.

The application first checks whether a face is visible through the webcam. After access is granted, the user can communicate with the assistant by speaking or typing.

## Important Note

The webcam component performs face-presence detection. It verifies that a face is visible, but it does not identify or authenticate a specific person. Therefore, it should not be considered a biometric security system.

## Main Features

- Real-time webcam face detection
- Face-presence access gate
- Voice-command recognition
- Typed-command alternative
- Text-to-speech responses
- Safe rule-based command interpretation
- Windows application launching
- Website and web-search support
- Automatic typed fallback when voice recognition fails
- Graphical interface developed with Tkinter
- Error handling for camera, microphone and unknown commands

## Application Workflow

1. Launch the graphical interface.
2. Click the Authenticate Face button.
3. Look toward the webcam.
4. Wait until access is granted.
5. Speak or type a command.
6. The command parser identifies the requested action.
7. The command executor performs the approved action.
8. The assistant displays and speaks its response.

## Supported Commands

Examples of supported commands include:

- Hello
- What time is it?
- What is today's date?
- Open calculator
- Open notepad
- Open YouTube
- Open Google
- Open GitHub
- Search the web for artificial intelligence
- Help
- Exit

## Technologies Used

- Python 3.11
- OpenCV
- SpeechRecognition
- PyAudio
- pyttsx3
- Tkinter
- Rule-based natural-language command parsing
- Git and GitHub

## Project Structure

```text
AI_capstone/
├── assets/
│   └── screenshots/
│       ├── assistant_gui.png
│       ├── face_access_gate.png
│       └── voice_command_result.png
├── src/
│   ├── __init__.py
│   ├── command_executor.py
│   ├── command_parser.py
│   ├── face_gate.py
│   ├── gui.py
│   ├── main.py
│   ├── speech_service.py
│   └── tts_service.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
