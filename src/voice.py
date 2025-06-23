import pyttsx3  # for voice answering


class Voice:
    def __init__(self):
        self.if_to_speak = False

    def set_voice(self,
                  if_to_speak):
        self.if_to_speak = if_to_speak

    def make_voice(self,
                   my_text: str):
        if self.if_to_speak:
            engine = pyttsx3.init()
            engine.say(my_text)
            engine.runAndWait()

