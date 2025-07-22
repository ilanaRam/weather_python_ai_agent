import pyttsx3  # for voice answering (output)
import speech_recognition as sr


class Voice:
    def __init__(self):
        self.use_voice = True

    def set_output_voice(self,
                         use_voice):
        if use_voice:
            self.use_voice = True
        else:
            self.use_voice = False


    def produce_voice(self,
                      my_text: str):
        if self.use_voice:
            engine = pyttsx3.init()
            engine.say(my_text)
            engine.runAndWait()

    def get_voice(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("🎤 Listening... Please say something.")
            recognizer.adjust_for_ambient_noise(source)  # Optional: helps with noisy background
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text
        except sr.UnknownValueError:
            print("❌ Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"🔌 Could not request results from Google Speech Recognition service; {e}")
        return None

# if __name__ == '__main__':
#     get_voice()
