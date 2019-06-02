from tkinter import ttk, filedialog

import speech_recognition as sr
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
import wave
import sys
import os

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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

        label2 = tk.Label(self, text="Name Audio Save", font=LARGE_FONT)
        label2.grid(row=1, column=3, padx=10, pady=10)

        button_load_wav = ttk.Button(self, text="Load WAV",
                            command=lambda: self.load_wav())
        button_load_wav.grid(row=1, column=4, padx=10, pady=10)


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

    def load_wav(self):

        ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__)

        filename = filedialog.askopenfilename(initialdir= ROOT_DIR + '/Voice_Samples/',
                                              title='Select wav file',
                                              filetypes=(
                                              ("wav files", "*wav"),
                                              ("all files", "*.*")))
        self.path_wav = filename

        spf = wave.open(self.path_wav, 'r')

        # Extract Raw Audio from Wav File
        signal = spf.readframes(-1)
        signal = np.fromstring(signal, 'Int16')
        fs = spf.getframerate()

        # If Stereo
        if spf.getnchannels() == 2:
            print('Just mono files')
            sys.exit(0)

        Time = np.linspace(0, len(signal) / fs, num=len(signal))

        figure = Figure(figsize=(10, 4), dpi=100)
        figure.canvas.set_window_title('Signal Wave...')

        first_subplot = figure.add_subplot(111)

        first_subplot.plot(Time, signal)
        first_subplot.set_title('Signal Wave')
        first_subplot.set_title('Signal Wave')
        first_subplot.set_ylabel('Frequency [Hz]')
        first_subplot.set_xlabel('Time [s]')

        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0, columnspan=8, padx=10, pady=30)


