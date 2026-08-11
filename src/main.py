from src.command_executor import execute_command
from src.command_parser import parse_command
from src.face_gate import run_face_gate
from src.speech_service import SpeechRecognitionService
from src.tts_service import TextToSpeechService


def select_input_method(
    speech_service,
    tts_service
):
    print()
    print("-" * 45)
    print("[1] Speak a command")
    print("[2] Type a command")
    print("[3] Exit")
    print("-" * 45)

    selected_option = input(
        "Choose an input method: "
    ).strip().lower()

    if selected_option in (
        "1",
        "voice",
        "speak"
    ):
        user_command = speech_service.listen()

        if user_command:
            return user_command

        fallback_message = (
            "I could not understand the voice command. "
            "Please type your command instead."
        )

        print(fallback_message)
        tts_service.speak(fallback_message)

        return input(
            "Type your command: "
        ).strip()

    if selected_option in (
        "2",
        "text",
        "type"
    ):
        return input(
            "Type your command: "
        ).strip()

    if selected_option in (
        "3",
        "exit",
        "quit"
    ):
        return "exit"

    print("Invalid selection. Please choose 1, 2 or 3.")
    return None


def run_cli_assistant():
    print("=" * 55)
    print("Multimodal AI Desktop Assistant")
    print("=" * 55)

    tts_service = TextToSpeechService()
    speech_service = SpeechRecognitionService()

    print("Starting face-detection access gate...")

    access_granted = run_face_gate()

    if not access_granted:
        denial_message = "Access was not granted."

        print(denial_message)
        tts_service.speak(denial_message)
        return

    welcome_message = (
        "Access granted successfully. "
        "You can speak or type a command."
    )

    print()
    print(welcome_message)
    print("Choose voice or text input from the menu.")

    tts_service.speak(welcome_message)

    try:
        while True:
            user_command = select_input_method(
                speech_service,
                tts_service
            )

            if user_command is None:
                continue

            if not user_command.strip():
                print(
                    "Assistant: No command was entered."
                )
                continue

            print(f"You: {user_command}")

            parsed_command = parse_command(
                user_command
            )

            result = execute_command(
                parsed_command
            )

            response_message = result["message"]

            print(
                f"Assistant: {response_message}"
            )

            if parsed_command["intent"] == "help":
                tts_service.speak(
                    "Here are the available commands."
                )
            else:
                tts_service.speak(
                    response_message
                )

            if result.get("should_exit", False):
                break

    except KeyboardInterrupt:
        closing_message = (
            "Session closed by the user."
        )

        print(f"\nAssistant: {closing_message}")
        tts_service.speak(closing_message)

    except EOFError:
        print("\nAssistant: Session closed.")

    finally:
        tts_service.stop()
        print(
            "AI assistant closed successfully."
        )


if __name__ == "__main__":
    run_cli_assistant()