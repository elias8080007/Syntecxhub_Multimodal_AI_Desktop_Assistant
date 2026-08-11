import re


SAMPLE_COMMANDS = [
    "What time is it?",
    "What is today's date?",
    "Open Calculator",
    "Open Notepad",
    "Open YouTube",
    "Open Google",
    "Open GitHub",
    "Search the web for artificial intelligence",
    "Show available commands",
    "Exit"
]


def parse_command(user_text):
    original_text = user_text.strip()

    normalized_text = " ".join(
        original_text.lower().split()
    )

    if not normalized_text:
        return {
            "intent": "empty",
            "parameter": None,
            "original_text": original_text
        }

    exit_commands = {
        "exit",
        "quit",
        "close",
        "close assistant",
        "goodbye"
    }

    if normalized_text in exit_commands:
        return {
            "intent": "exit",
            "parameter": None,
            "original_text": original_text
        }

    help_commands = {
        "help",
        "show commands",
        "show available commands",
        "what can you do",
        "available commands"
    }

    if normalized_text in help_commands:
        return {
            "intent": "help",
            "parameter": None,
            "original_text": original_text
        }

    search_patterns = [
        r"^search the web for (.+)$",
        r"^search for (.+)$",
        r"^google (.+)$"
    ]

    for pattern in search_patterns:
        search_match = re.match(
            pattern,
            normalized_text
        )

        if search_match:
            search_query = search_match.group(1).strip()

            return {
                "intent": "web_search",
                "parameter": search_query,
                "original_text": original_text
            }

    if (
        "what time" in normalized_text
        or normalized_text == "time"
        or "tell me the time" in normalized_text
    ):
        return {
            "intent": "tell_time",
            "parameter": None,
            "original_text": original_text
        }

    if (
        "what is today's date" in normalized_text
        or "what is the date" in normalized_text
        or normalized_text == "date"
        or "tell me the date" in normalized_text
    ):
        return {
            "intent": "tell_date",
            "parameter": None,
            "original_text": original_text
        }

    if (
        "open calculator" in normalized_text
        or "start calculator" in normalized_text
    ):
        return {
            "intent": "open_calculator",
            "parameter": None,
            "original_text": original_text
        }

    if (
        "open notepad" in normalized_text
        or "start notepad" in normalized_text
    ):
        return {
            "intent": "open_notepad",
            "parameter": None,
            "original_text": original_text
        }

    websites = {
        "open youtube": "youtube",
        "open google": "google",
        "open github": "github"
    }

    for command_text, website_name in websites.items():
        if normalized_text == command_text:
            return {
                "intent": "open_website",
                "parameter": website_name,
                "original_text": original_text
            }

    greeting_commands = {
        "hello",
        "hi",
        "hey",
        "hello assistant",
        "good morning",
        "good afternoon",
        "good evening"
    }

    if normalized_text in greeting_commands:
        return {
            "intent": "greeting",
            "parameter": None,
            "original_text": original_text
        }

    return {
        "intent": "unknown",
        "parameter": normalized_text,
        "original_text": original_text
    }