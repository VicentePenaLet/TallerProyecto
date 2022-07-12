from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from plyer import filechooser
from kivymd.toast import toast
from detectorSift import search_img_in_db, add_id
from kivy.uix.screenmanager import ScreenManager, Screen

import cv2
import os
import numpy as np
import pandas as pd
from voiceCommand import Speaker, listener
from threading import Thread
cwd = os.getcwd()

Window.size = (300, 530)

class MainWindow(Screen):
    pass


class SecondWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class Example(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open(cwd+"/galletas.npy", 'rb') as f:
            self.df = np.load(f, allow_pickle=True)
        self.db = add_id(pd.read_csv(cwd+"/galletas_DB.csv"),"galleta")
        self.labels = ["Product", "Brand", "Price", "Description", "Ingredientes", "allergies"]
        self.speaker = Speaker()

    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file("kv/MainWindow.kv")

    def file_chooser1(self):
        filechooser.open_file(on_selection=self.selected)


    def selected(self, selection1):
        self.image_path = selection1[0]
        toast(self.image_path)
        self.root.get_screen('main').ids.img1.source = self.image_path
        self.root.get_screen('main').ids.hidden_button.opacity = 1
        self.root.get_screen('main').ids.hidden_button.disabled = False

    def search_in_db(self):
        pass

    def look_for_matches(self):
        imageSift = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        self.product = search_img_in_db(imageSift, self.df, self.db, 0.75)
        for label in self.labels:
            widget = getattr(self.root.get_screen("second").ids, label)
            print(self.product[label].iloc[0])
            widget.secondary_text = str(self.product[label].iloc[0])

    def speaker_thread_product(self):
        p1 = Thread(target=self.text_to_speech_product)
        p1.start()

    def speaker_thread_brand(self):
        p1 = Thread(target=self.text_to_speech_brand)
        p1.start()

    def speaker_thread_price(self):
        p1 = Thread(target=self.text_to_speech_price)
        p1.start()

    def speaker_thread_description(self):
        p1 = Thread(target=self.text_to_speech_description)
        p1.start()

    def speaker_thread_ingredientes(self):
        p1 = Thread(target=self.text_to_speech_ingredientes)
        p1.start()

    def speaker_thread_allergies(self):
        p1 = Thread(target=self.text_to_speech_allergies)
        p1.start()

    def text_to_speech_product(self):
        if self.speaker.active:
            self.speaker.stop()
        else:
            self.speaker.speak(str(self.product["Product"].iloc[0]))

    def text_to_speech_brand(self):
        self.speaker.speak(str(self.product["Brand"].iloc[0]))

    def text_to_speech_price(self):
        self.speaker.speak(str(self.product["Price"].iloc[0]))

    def text_to_speech_description(self):
        self.speaker.speak(str(self.product["Description"].iloc[0]))

    def text_to_speech_ingredientes(self):
        self.speaker.speak(str(self.product["Ingredientes"].iloc[0]))

    def text_to_speech_allergies(self):
        self.speaker.speak(str(self.product["allergies"].iloc[0]))


Example().run()