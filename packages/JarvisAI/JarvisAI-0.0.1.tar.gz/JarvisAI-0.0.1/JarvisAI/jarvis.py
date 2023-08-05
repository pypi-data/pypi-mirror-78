from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import os


mode = 'pro'  # dev or pro

if mode != 'dev':
    from . import action
if mode != 'pro':
    import action


class Jarvis:
    def __init__(self, jarvis_features_config, user_config):
        self.jarvis_features_config = jarvis_features_config
        self.user_config = user_config

    def txt2speech(self, mytext):
        try:
            myobj = gTTS(text=mytext, lang='en', slow=False)
            myobj.save("tmp.mp3")
            playsound("tmp.mp3")
            os.remove("tmp.mp3")
        except Exception:
            mytext = "Sorry I couldn't understand, or not implemented to handle this input"
            print(mytext)
            myobj = gTTS(text=mytext, lang='en', slow=False)
            myobj.save("tmp.mp3")
            playsound("tmp.mp3")
            os.remove("tmp.mp3")


    def mic_input(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            self.txt2speech("Say Something!")
            audio = r.listen(source)
        try:
            print("You: ", r.recognize_google(audio))
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            self.txt2speech("Sorry I couldn't understand, please try again")
            # print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            self.txt2speech("Sorry I couldn't understand, please try again")
            # print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def txt_input(self):
        inp = input("Enter Anything: " or "Nothing")
        if inp == "Nothing":
            self.txt2speech("Sorry I couldn't understand, please try again")
        else:
            return inp

    def get_user_input(self, inp_src):
        if inp_src == "mic":
            inp = self.mic_input()
        if inp_src == "txt":
            inp = self.txt_input()
        return inp

    def check_input(self, inp_txt):
        output = "Output from Jarvis"
        self.txt2speech(output)


def start(jarvis_features_config, user_config):
    inp_src = "txt"  # mic / txt

    jarvis_obj = Jarvis(jarvis_features_config, user_config)
    action_obj = action.Action(jarvis_features_config, user_config)
    while True:
        inp = jarvis_obj.get_user_input(inp_src)
        output = action_obj.take_action(inp)
        print(output)
        jarvis_obj.txt2speech(output)


if __name__ == '__main__':
    start()
