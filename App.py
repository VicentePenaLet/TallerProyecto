from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from plyer import filechooser
from kivymd.toast import toast
from detectorSift import search_img_in_db, add_id
import cv2
import os
import numpy as np
import pandas as pd

cwd = os.getcwd()

Window.size = (300, 530)

class Example(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open(cwd+"/galletas.npy", 'rb') as f:
            self.df = np.load(f, allow_pickle=True)
        self.db = add_id(pd.read_csv(cwd+"/galletas_DB.csv"),"galleta")


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
        self.root.ids.img1.source = self.image_path
        self.root.ids.hidden_button.opacity = 1
        self.root.ids.hidden_button.disabled = False

    def search_in_db(self):
        pass

    def look_for_matches(self):
        imageSift = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        self.product = search_img_in_db(imageSift, self.df, self.db, 0.75)
        print(self.product.columns)
        print(self.product)


Example().run()