import pyttsx3


class TextToSpeechService:
    def __init__(self, speech_rate=175, volume=1.0):
        self.engine = None
        self.available = False

        try:
            self.engine = pyttsx3.init()

            self.engine.setProperty(
                "rate",
                speech_rate
            )

            self.engine.setProperty(
                "volume",
                volume
            )

            self.available = True
            print("Text-to-speech service is ready.")

        except Exception as error:
            print(
                "Warning: Text-to-speech could not be initialized."
            )
            print(f"Reason: {error}")

    def speak(self, text):
        if not self.available or self.engine is None:
            return False

        speech_text = " ".join(
            str(text).split()
        )

        if not speech_text:
            return False

        try:
            self.engine.say(speech_text)
            self.engine.runAndWait()
            return True

        except Exception as error:
            print(
                f"Text-to-speech error: {error}"
            )
            return False

    def stop(self):
        if self.engine is not None:
            try:
                self.engine.stop()
            except Exception:
                pass


if __name__ == "__main__":
    tts_service = TextToSpeechService()

    success = tts_service.speak(
        "Hello Elias. The text to speech service "
        "is working successfully."
    )

    if success:
        print("Speech test completed successfully.")
    else:
        print("Speech test failed.")