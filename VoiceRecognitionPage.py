import os
import sys
import tkinter as tk
import wave
from tkinter import ttk, filedialog

import numpy as np
import speech_recognition as sr
from langdetect import detect
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.fftpack import fft, fftfreq
from scipy.io import wavfile as wav
import matplotlib.pyplot as plt

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

        button_create_fft = ttk.Button(self, text="Create fft",
                                       command=lambda: self.create_fft())
        button_create_fft.grid(row=1, column=5, padx=10, pady=10)
        button_check_language = ttk.Button(self, text="Check language",
                                           command=lambda: self.check_language())
        button_check_language.grid(row=1, column=6, padx=10, pady=10)
        self.label_eng = tk.Label(self, text="", font=LARGE_FONT)
        self.label_eng.grid(row=3, column=6, padx=10, pady=10)
        self.label_de = tk.Label(self, text="", font=LARGE_FONT)
        self.label_de.grid(row=4, column=6, padx=10, pady=10)
        self.label_lang = tk.Label(self, text="", font=LARGE_FONT)
        self.label_lang.grid(row=5, column=6, padx=10, pady=10)
        self.name = tk.StringVar()
        e1 = tk.Entry(self, textvariable=self.name).grid(row=2, column=3, padx=10, pady=10)

    def take_sample(self):
        r = sr.Recognizer()
        print("Speak now!")
        print(sr.Microphone.list_microphone_names())
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

        filename = filedialog.askopenfilename(initialdir=ROOT_DIR + '/Voice_Samples/',
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

        figure = Figure(figsize=(5, 3), dpi=100)
        figure.canvas.set_window_title('Signal Wave...')

        first_subplot = figure.add_subplot(111)

        first_subplot.plot(Time, signal / 1000)
        first_subplot.set_title('Signal Wave')
        first_subplot.set_ylabel('Frequency [kHz]')
        first_subplot.set_xlabel('Time [s]')

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0, columnspan=5, padx=10, pady=30)

    def create_fft(self):

        figure = Figure(figsize=(5, 3), dpi=100)
        figure.canvas.set_window_title('FFT')
        first_subplot = figure.add_subplot(111)

        samplerate, data = wav.read(self.path_wav)
        samples = data.shape[0]

        datafft = fft(data)

        fftabs = abs(datafft)
        freqs = fftfreq(samples, 1/samplerate)

        first_subplot.set_title('FFT')
        first_subplot.set_xscale("log")
        first_subplot.set_ylabel('Amplitude')
        first_subplot.set_xlabel('Frequency [Hz]')
        first_subplot.set_xlim([10, samplerate / 2])
        first_subplot.grid(True)
        first_subplot.plot(freqs[:int(freqs.size / 2)], fftabs[:int(freqs.size / 2)])
        #first_subplot.show()

        # first_subplot.grid(True)
        # #first_subplot.plot(freqs, np.abs(fft_out))
        # first_subplot.plot(freqs[:int(freqs.size/2)], np.abs(fft_out)[:int(freqs.size/2)])
        # first_subplot.xlim([10 , rate/2])
        # first_subplot.plot(freqs, np.abs(fft_out))
        # first_subplot.set_xlabel('Frequency [Hz]')


        figure.tight_layout()

        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=5, column=0, columnspan=5, padx=10, pady=30)

    def check_language(self):
        ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__)

        filename = filedialog.askopenfilename(initialdir=ROOT_DIR + '/Voice_Samples/',
                                              title='Select wav file',
                                              filetypes=(
                                                  ("wav files", "*wav"),
                                                  ("all files", "*.*")))
        self.path_wav = filename
        r = sr.Recognizer()
        with sr.WavFile(self.path_wav) as source:  # use "test.wav" as the audio source
            audio = r.listen(source)  #
        try:
            text = r.recognize_google(audio_data=audio, language="en-GB",
                                      show_all=True)
            values = "You said in English: " + text["alternative"][0]["transcript"] + "; with confidence: " + str(
                text["alternative"][0]["confidence"])
            print(values)
            self.label_eng.config(text=values)
            language = detect(text["alternative"][0]["transcript"])
            if language == 'en':
                self.label_lang.config(text="Language of text is english")
        except LookupError:  # speech is unintelligible
            self.label_eng.config(text='Could not understand audio')

        try:
            text = r.recognize_google(audio_data=audio, language="de-DE", show_all=True)
            values = "You said in Deutsch: " + text["alternative"][0]["transcript"] + "; with confidence: " + str(
                text["alternative"][0]["confidence"])
            print(values)
            language = detect(text["alternative"][0]["transcript"])
            self.label_de.config(text=values)
            if language == 'de':
                self.label_lang.config(text="Language of text is deutsch")
        except LookupError:  # speech is unintelligible
            self.label_de.config(text='Could not understand audio')
