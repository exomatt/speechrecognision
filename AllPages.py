from VoiceRecognitionPage import VoiceRecognitionPage


class AllPages(object):
    def __init__(self, container, controller):
        self.AllFrames = {}
        self.AllFrames["VoiceRecognitionPage"] = VoiceRecognitionPage(parent=container, controller=controller)
        self.AllFrames["VoiceRecognitionPage"].grid(row=0, column=0, sticky="nsew")
