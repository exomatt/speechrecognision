from tkinter import ttk

import speech_recognition as sr
import tkinter as tk
import os
import sys

LARGE_FONT = ("Verdana", 12)


class VoiceRecognitionPage(tk.Frame):
    def __init__(self, parent, controller):
        self.start, self.end, self.lastCode = 0, 0, -1
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Voice Page", font=LARGE_FONT)
        label.grid(row=0, column=5, padx=10, pady=10)

        button_load_image = ttk.Button(self, text="Take sample",
                            command=lambda: self.take_sample())
        button_load_image.grid(row=1, column=2, padx=10, pady=10)

        label2 = tk.Label(self, text="File Name", font=LARGE_FONT)
        label2.grid(row=1, column=3, padx=10, pady=10)

        self.name = tk.StringVar()
        e1 = tk.Entry(self, textvariable=self.name).grid(row=2, column=3, padx=10, pady=10)


    def take_sample(self):
        r = sr.Recognizer()
        print("Speak now!")

        ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__)

        with sr.Microphone() as source:
            audio = r.listen(source)

        with open(ROOT_DIR + '/Voice_Samples/' + self.name.get() + '.wav', "wb") as f:
            f.write(audio.get_wav_data())

        try:
            text = r.recognize_google(audio)
            print("You said: {}".format(text))
        except sr.UnknownValueError:
            print("Cannot recognize what you said")

