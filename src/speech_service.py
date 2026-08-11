import speech_recognition as sr


class SpeechRecognitionService:
    def __init__(self, language="en-US"):
        self.recognizer = sr.Recognizer()
        self.language = language

        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

    def listen(self):
        try:
            with sr.Microphone() as microphone:
                print()
                print("Listening... Please speak now.")

                self.recognizer.adjust_for_ambient_noise(
                    microphone,
                    duration=0.7
                )

                audio = self.recognizer.listen(
                    microphone,
                    timeout=6,
                    phrase_time_limit=10
                )

            print("Recognizing your command...")

            recognized_text = (
                self.recognizer.recognize_google(
                    audio,
                    language=self.language
                )
            )

            recognized_text = recognized_text.strip()

            print(
                f"Recognized command: {recognized_text}"
            )

            return recognized_text

        except sr.WaitTimeoutError:
            print(
                "No speech was detected before the timeout."
            )
            return None

        except sr.UnknownValueError:
            print(
                "The speech could not be understood."
            )
            return None

        except sr.RequestError as error:
            print(
                "The online speech-recognition service "
                "is unavailable."
            )
            print(f"Reason: {error}")
            return None

        except OSError as error:
            print(
                "The microphone could not be accessed."
            )
            print(f"Reason: {error}")
            return None

        except Exception as error:
            print(
                f"Speech-recognition error: {error}"
            )
            return None


if __name__ == "__main__":
    speech_service = SpeechRecognitionService()

    command = speech_service.listen()

    if command:
        print(f"You said: {command}")
    else:
        print("No command was recognized.")