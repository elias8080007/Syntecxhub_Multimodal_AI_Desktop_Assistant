import tkinter as tk
from tkinter import scrolledtext

from src.command_executor import execute_command
from src.command_parser import parse_command
from src.face_gate import run_face_gate
from src.speech_service import SpeechRecognitionService
from src.tts_service import TextToSpeechService


class MultimodalAssistantGUI:
    BACKGROUND_COLOR = "#0F172A"
    PANEL_COLOR = "#1E293B"
    INPUT_COLOR = "#334155"
    PRIMARY_COLOR = "#38BDF8"
    SUCCESS_COLOR = "#22C55E"
    ERROR_COLOR = "#EF4444"
    WARNING_COLOR = "#F59E0B"
    TEXT_COLOR = "#F8FAFC"
    MUTED_TEXT_COLOR = "#94A3B8"

    def __init__(self, root):
        self.root = root
        self.authenticated = False

        self.tts_service = TextToSpeechService()
        self.speech_service = SpeechRecognitionService()

        self.configure_window()
        self.create_interface()
        self.disable_command_controls()

        self.add_message(
            "System",
            "Face authentication is required before using "
            "the assistant."
        )

    def configure_window(self):
        self.root.title(
            "Multimodal AI Desktop Assistant"
        )

        self.root.geometry("950x650")
        self.root.minsize(720, 520)

        self.root.configure(
            bg=self.BACKGROUND_COLOR
        )

        # Maximize the application on Windows so that the
        # command controls remain above the taskbar.
        try:
            self.root.state("zoomed")

        except tk.TclError:
            # Responsive fallback for systems that do not
            # support Tkinter's Windows "zoomed" state.
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            window_width = int(screen_width * 0.90)
            window_height = int(screen_height * 0.85)

            horizontal_position = max(
                (screen_width - window_width) // 2,
                0
            )

            vertical_position = max(
                (screen_height - window_height) // 2,
                0
            )

            self.root.geometry(
                f"{window_width}x{window_height}+"
                f"{horizontal_position}+{vertical_position}"
            )

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
        )

    def create_interface(self):
        header_frame = tk.Frame(
            self.root,
            bg=self.BACKGROUND_COLOR
        )

        header_frame.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )

        title_label = tk.Label(
            header_frame,
            text="Multimodal AI Desktop Assistant",
            font=("Segoe UI", 22, "bold"),
            bg=self.BACKGROUND_COLOR,
            fg=self.TEXT_COLOR
        )

        title_label.pack(anchor="w")

        subtitle_label = tk.Label(
            header_frame,
            text=(
                "Face Gate • Voice Commands • Text Commands "
                "• Spoken Responses"
            ),
            font=("Segoe UI", 11),
            bg=self.BACKGROUND_COLOR,
            fg=self.MUTED_TEXT_COLOR
        )

        subtitle_label.pack(
            anchor="w",
            pady=(5, 0)
        )

        authentication_frame = tk.Frame(
            self.root,
            bg=self.PANEL_COLOR,
            padx=18,
            pady=15
        )

        authentication_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        authentication_title = tk.Label(
            authentication_frame,
            text="Face-Detection Access Gate",
            font=("Segoe UI", 13, "bold"),
            bg=self.PANEL_COLOR,
            fg=self.TEXT_COLOR
        )

        authentication_title.pack(
            side="left"
        )

        self.status_label = tk.Label(
            authentication_frame,
            text="● Access Required",
            font=("Segoe UI", 11, "bold"),
            bg=self.PANEL_COLOR,
            fg=self.WARNING_COLOR
        )

        self.status_label.pack(
            side="left",
            padx=25
        )

        self.authentication_button = tk.Button(
            authentication_frame,
            text="Authenticate Face",
            command=self.authenticate_face,
            font=("Segoe UI", 10, "bold"),
            bg=self.PRIMARY_COLOR,
            fg="#082F49",
            activebackground="#7DD3FC",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        )

        self.authentication_button.pack(
            side="right"
        )

        history_title = tk.Label(
            self.root,
            text="Assistant Conversation",
            font=("Segoe UI", 13, "bold"),
            bg=self.BACKGROUND_COLOR,
            fg=self.TEXT_COLOR
        )

        history_title.pack(
            anchor="w",
            padx=25,
            pady=(10, 5)
        )

        self.conversation_history = (
            scrolledtext.ScrolledText(
                self.root,
                wrap=tk.WORD,
                height=10,
                font=("Segoe UI", 11),
                bg=self.PANEL_COLOR,
                fg=self.TEXT_COLOR,
                insertbackground=self.TEXT_COLOR,
                relief="flat",
                padx=15,
                pady=15,
                state="disabled"
            )
        )

        self.conversation_history.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 15)
        )

        self.conversation_history.tag_configure(
            "System",
            foreground=self.WARNING_COLOR,
            font=("Segoe UI", 11, "bold")
        )

        self.conversation_history.tag_configure(
            "You",
            foreground=self.PRIMARY_COLOR,
            font=("Segoe UI", 11, "bold")
        )

        self.conversation_history.tag_configure(
            "Assistant",
            foreground=self.SUCCESS_COLOR,
            font=("Segoe UI", 11, "bold")
        )

        command_frame = tk.Frame(
            self.root,
            bg=self.PANEL_COLOR,
            padx=18,
            pady=15
        )

        command_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 10)
        )

        command_label = tk.Label(
            command_frame,
            text="Enter a command",
            font=("Segoe UI", 11, "bold"),
            bg=self.PANEL_COLOR,
            fg=self.TEXT_COLOR
        )

        command_label.pack(
            anchor="w",
            pady=(0, 8)
        )

        input_frame = tk.Frame(
            command_frame,
            bg=self.PANEL_COLOR
        )

        input_frame.pack(fill="x")

        self.command_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            bg=self.INPUT_COLOR,
            fg=self.TEXT_COLOR,
            insertbackground=self.TEXT_COLOR,
            disabledbackground="#1F2937",
            disabledforeground=self.MUTED_TEXT_COLOR,
            relief="flat"
        )

        self.command_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=10,
            padx=(0, 10)
        )

        self.command_entry.bind(
            "<Return>",
            self.handle_enter_key
        )

        self.execute_button = tk.Button(
            input_frame,
            text="Execute",
            command=self.execute_typed_command,
            font=("Segoe UI", 10, "bold"),
            bg=self.SUCCESS_COLOR,
            fg="#052E16",
            activebackground="#86EFAC",
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=9
        )

        self.execute_button.pack(
            side="left"
        )

        action_frame = tk.Frame(
            self.root,
            bg=self.BACKGROUND_COLOR
        )

        action_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        self.speak_button = tk.Button(
            action_frame,
            text="🎤 Speak Command",
            command=self.listen_for_command,
            font=("Segoe UI", 10, "bold"),
            bg=self.PRIMARY_COLOR,
            fg="#082F49",
            activebackground="#7DD3FC",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=9
        )

        self.speak_button.pack(
            side="left",
            padx=(0, 10)
        )

        self.help_button = tk.Button(
            action_frame,
            text="Show Commands",
            command=self.show_available_commands,
            font=("Segoe UI", 10, "bold"),
            bg=self.INPUT_COLOR,
            fg=self.TEXT_COLOR,
            activebackground="#475569",
            activeforeground=self.TEXT_COLOR,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=9
        )

        self.help_button.pack(
            side="left",
            padx=(0, 10)
        )

        clear_button = tk.Button(
            action_frame,
            text="Clear Conversation",
            command=self.clear_conversation,
            font=("Segoe UI", 10),
            bg=self.INPUT_COLOR,
            fg=self.TEXT_COLOR,
            activebackground="#475569",
            activeforeground=self.TEXT_COLOR,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=9
        )

        clear_button.pack(
            side="left"
        )

        exit_button = tk.Button(
            action_frame,
            text="Exit",
            command=self.close_application,
            font=("Segoe UI", 10, "bold"),
            bg=self.ERROR_COLOR,
            fg=self.TEXT_COLOR,
            activebackground="#F87171",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=9
        )

        exit_button.pack(
            side="right"
        )

    def disable_command_controls(self):
        self.command_entry.configure(
            state="disabled"
        )

        self.execute_button.configure(
            state="disabled"
        )

        self.speak_button.configure(
            state="disabled"
        )

        self.help_button.configure(
            state="disabled"
        )

    def enable_command_controls(self):
        self.command_entry.configure(
            state="normal"
        )

        self.execute_button.configure(
            state="normal"
        )

        self.speak_button.configure(
            state="normal"
        )

        self.help_button.configure(
            state="normal"
        )

        self.command_entry.focus_set()

    def authenticate_face(self):
        self.authentication_button.configure(
            state="disabled"
        )

        self.status_label.configure(
            text="● Checking for a face...",
            fg=self.PRIMARY_COLOR
        )

        self.root.update_idletasks()

        try:
            access_granted = run_face_gate()

        except Exception as error:
            access_granted = False

            self.add_message(
                "System",
                f"Face gate error: {error}"
            )

        if access_granted:
            self.authenticated = True

            self.status_label.configure(
                text="● Access Granted",
                fg=self.SUCCESS_COLOR
            )

            self.authentication_button.configure(
                text="Authenticated",
                state="disabled",
                bg=self.SUCCESS_COLOR
            )

            self.enable_command_controls()

            message = (
                "Access granted successfully. "
                "You can now speak or type a command."
            )

            self.add_message(
                "Assistant",
                message
            )

            self.tts_service.speak(message)

        else:
            self.authenticated = False

            self.status_label.configure(
                text="● Access Denied",
                fg=self.ERROR_COLOR
            )

            self.authentication_button.configure(
                text="Try Again",
                state="normal",
                bg=self.PRIMARY_COLOR
            )

            message = (
                "Access was not granted. "
                "Please try face detection again."
            )

            self.add_message(
                "System",
                message
            )

            self.tts_service.speak(message)

    def handle_enter_key(self, event):
        self.execute_typed_command()

    def execute_typed_command(self):
        if not self.authenticated:
            self.add_message(
                "System",
                "Face authentication is required."
            )
            return

        user_command = (
            self.command_entry.get().strip()
        )

        if not user_command:
            self.add_message(
                "System",
                "Please enter a command first."
            )
            return

        self.command_entry.delete(0, tk.END)

        self.process_command(user_command)

    def listen_for_command(self):
        if not self.authenticated:
            self.add_message(
                "System",
                "Face authentication is required."
            )
            return

        self.status_label.configure(
            text="● Listening...",
            fg=self.PRIMARY_COLOR
        )

        self.speak_button.configure(
            state="disabled"
        )

        self.root.update_idletasks()

        user_command = self.speech_service.listen()

        self.speak_button.configure(
            state="normal"
        )

        self.status_label.configure(
            text="● Access Granted",
            fg=self.SUCCESS_COLOR
        )

        if not user_command:
            message = (
                "I could not understand the voice command. "
                "You can try again or type the command."
            )

            self.add_message(
                "Assistant",
                message
            )

            self.tts_service.speak(message)
            return

        self.process_command(user_command)

    def process_command(self, user_command):
        self.add_message(
            "You",
            user_command
        )

        try:
            parsed_command = parse_command(
                user_command
            )

            result = execute_command(
                parsed_command
            )

            response_message = result["message"]

            self.add_message(
                "Assistant",
                response_message
            )

            if parsed_command["intent"] == "help":
                self.tts_service.speak(
                    "The available commands are "
                    "displayed in the conversation."
                )
            else:
                self.tts_service.speak(
                    response_message
                )

            if result.get("should_exit", False):
                self.root.after(
                    1000,
                    self.close_application
                )

        except Exception as error:
            error_message = (
                "An unexpected error occurred while "
                "processing the command."
            )

            self.add_message(
                "System",
                f"{error_message}\nDetails: {error}"
            )

            self.tts_service.speak(
                error_message
            )

    def show_available_commands(self):
        self.process_command("help")

    def add_message(self, speaker, message):
        self.conversation_history.configure(
            state="normal"
        )

        self.conversation_history.insert(
            tk.END,
            f"{speaker}: ",
            speaker
        )

        self.conversation_history.insert(
            tk.END,
            f"{message}\n\n"
        )

        self.conversation_history.configure(
            state="disabled"
        )

        self.conversation_history.see(
            tk.END
        )

    def clear_conversation(self):
        self.conversation_history.configure(
            state="normal"
        )

        self.conversation_history.delete(
            "1.0",
            tk.END
        )

        self.conversation_history.configure(
            state="disabled"
        )

        self.add_message(
            "System",
            "Conversation cleared."
        )

    def close_application(self):
        self.tts_service.stop()
        self.root.destroy()


def launch_gui():
    root = tk.Tk()

    MultimodalAssistantGUI(root)

    root.mainloop()


if __name__ == "__main__":
    launch_gui()