import subprocess
import webbrowser

from datetime import datetime
from urllib.parse import quote_plus

from src.command_parser import SAMPLE_COMMANDS


WEBSITE_URLS = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://github.com"
}


def create_result(
    success,
    message,
    should_exit=False
):
    return {
        "success": success,
        "message": message,
        "should_exit": should_exit
    }


def execute_command(parsed_command):
    intent = parsed_command["intent"]
    parameter = parsed_command["parameter"]

    try:
        if intent == "empty":
            return create_result(
                False,
                "Please enter a command."
            )

        if intent == "greeting":
            return create_result(
                True,
                "Hello! How can I assist you?"
            )

        if intent == "tell_time":
            current_time = (
                datetime.now()
                .strftime("%I:%M %p")
                .lstrip("0")
            )

            return create_result(
                True,
                f"The current time is {current_time}."
            )

        if intent == "tell_date":
            current_date = datetime.now().strftime(
                "%A, %B %d, %Y"
            )

            return create_result(
                True,
                f"Today's date is {current_date}."
            )

        if intent == "open_calculator":
            subprocess.Popen(
                ["calc.exe"]
            )

            return create_result(
                True,
                "Opening Calculator."
            )

        if intent == "open_notepad":
            subprocess.Popen(
                ["notepad.exe"]
            )

            return create_result(
                True,
                "Opening Notepad."
            )

        if intent == "open_website":
            website_url = WEBSITE_URLS.get(
                parameter
            )

            if website_url is None:
                return create_result(
                    False,
                    "That website is not supported."
                )

            webbrowser.open(
                website_url
            )

            return create_result(
                True,
                f"Opening {parameter.title()}."
            )

        if intent == "web_search":
            if not parameter:
                return create_result(
                    False,
                    "Please provide something to search for."
                )

            encoded_query = quote_plus(
                parameter
            )

            search_url = (
                "https://www.google.com/search?q="
                + encoded_query
            )

            webbrowser.open(
                search_url
            )

            return create_result(
                True,
                f"Searching the web for {parameter}."
            )

        if intent == "help":
            command_list = "\n".join(
                f"- {command}"
                for command in SAMPLE_COMMANDS
            )

            return create_result(
                True,
                "Available commands:\n"
                + command_list
            )

        if intent == "exit":
            return create_result(
                True,
                "Goodbye! Closing the assistant.",
                should_exit=True
            )

        return create_result(
            False,
            (
                "I did not understand that command. "
                "Type 'help' to see the available commands."
            )
        )

    except FileNotFoundError:
        return create_result(
            False,
            "The requested application was not found."
        )

    except Exception as error:
        return create_result(
            False,
            f"Command execution failed: {error}"
        )