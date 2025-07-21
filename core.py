from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivymd.app import MDApp
import sys
from os import path, sep, getcwd
from kivy.lang import Builder
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.core.window import Window
from kivy.resources import resource_add_path
from logging import getLogger, ERROR
from kivymd.icon_definitions import md_icons
import string

from image_processing import converter
from ui_utils import shorten_path, column_to_int
from settings_manager import SettingsManager

# region app context
getLogger("PIL").setLevel(ERROR)

def temp_folder(file):
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(sys._MEIPASS)
        font_path = path.join(sys._MEIPASS, file)
    else:
        resource_add_path('.')
        font_path = file
    return font_path

LabelBase.register(DEFAULT_FONT, temp_folder("./assets/font/Vazirmatn-Medium.ttf"))

global alphabet
alphabet = list(string.ascii_uppercase)

global global_img_ext
global_img_ext = [".png", ".jpg"]

global icon_path
icon_path = temp_folder("assets/logo/logo.ico")

Window.size = (1000, 660)
# endregion

class MyApp(MDApp):
    title = "Behzisti"
    icon = icon_path
    resizable = False

    def build(self):
        self.icon_path = icon_path
        self.settings_manager = SettingsManager()
        self.selected_paths = {"pictures_path": "",
                               "destination": "",
                               "excel_path": "",
                               "dropdown_column_id": 0, "dropdown_column_card": 1, "dropdown_old_suffix": "",
                               "dropdown_new_suffix": "", "dropdown_delimiter": "None"}
        self.menu_items = {
            "column_id": alphabet,
            "column_card": alphabet,
            "old_suffix": global_img_ext,
            "new_suffix": global_img_ext,
            "delimiter": ["LF", "ﺪﻧﻮﺸﯿﭘ ﻥﻭﺪﺑ"]
        }
        self.speed_dial_data = {
            'ﯽﻠﺒﻗ ﺕﺎﻤﯿﻈﻨﺗ ﺎﺑ ﺍﺮﺟﺍ ': [
                'play',
                "on_release", lambda x: self.run_previous_config()
            ]
        }
        self.menus = {}
        for key, items in self.menu_items.items():
            self.menus[key] = MDDropdownMenu(
                items=[{
                    "viewclass": "OneLineListItem",
                    "text": item,
                    "on_release": lambda x=item, k=key: self.set_dropdown_value(x, k)}
                       for item in items],
                width_mult=4
            )
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Red"
        return Builder.load_file("main.kv")

    # region self function
    def toggle_theme(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

    def collect_input_data(self):
        delimiter = self.selected_paths.get("dropdown_delimiter", "")
        data = {
            "pictures_path": self.selected_paths.get("pictures_path", ""),
            "destination": self.selected_paths.get("destination", ""),
            "excel_path": self.selected_paths.get("excel_path", ""),
            "dropdown_new_suffix": self.selected_paths.get("dropdown_new_suffix", ""),
            "dropdown_old_suffix": self.selected_paths.get("dropdown_old_suffix", ""),
            "dropdown_delimiter": "" if delimiter == "ﺪﻧﻮﺸﯿﭘ ﻥﻭﺪﺑ" else delimiter,
            "dropdown_column_id": column_to_int(self.selected_paths.get("dropdown_column_id", "")),
            "dropdown_column_card": column_to_int(self.selected_paths.get("dropdown_column_card", ""))
        }
        return data

    @staticmethod
    def validate_input_data(data):
        required_fields = ["pictures_path", "destination", "excel_path",
                           "dropdown_new_suffix", "dropdown_old_suffix",
                           "dropdown_column_id", "dropdown_column_card"]
        validate_required_fields = all(data[field] for field in required_fields)
        validate_dropdown_delimiter = data["dropdown_delimiter"] != "None"
        return validate_required_fields and validate_dropdown_delimiter

    def save_settings(self, data):
        self.settings_manager.save_settings(data)

    def run_converter(self, data):
        converter(
            pictures_source_path=data["pictures_path"],
            pictures_destination_path=data["destination"],
            excel_path=data["excel_path"],
            old_ext=data["dropdown_old_suffix"],
            new_ext=data["dropdown_new_suffix"],
            prefix=data["dropdown_delimiter"],
            id_column=data["dropdown_column_id"],
            card_column=data["dropdown_column_card"]
        )
        self.show_snackbar("ﺪﺷ ﻡﺎﺠﻧﺍ ﺖﯿﻘﻓﻮﻣ ﺎﺑ ﻡﺎﻧ ﺮﯿﯿﻐﺗ")

    def run_previous_config(self):
        settings = self.settings_manager.load_settings()
        if settings:
            self.run_converter(settings)
        else:
            self.show_snackbar("ﺪﯿﻨﮐ ﻪﻓﺎﺿﺍ ﺍﺭ ﺕﺎﻤﯿﻈﻨﺗ ﻩﺭﺎﺑﻭﺩ ﺎﻔﻄﻟ ﺩﺍﺩ ﺥﺭ ﯽﯾﺎﻄﺧ")

    @staticmethod
    def show_snackbar(message):
        Snackbar(
            text=message,
            snackbar_x="5dp",
            snackbar_y="5dp",
            size_hint_x=.99,
            radius=[10, 10, 10, 10]
        ).open()

    # region file manager
    def open_file_manager(self, file_type, select_type, key, allowed_ext=[]):
        self.file_manager = MDFileManager(
            exit_manager=self.close_file_manager,
            select_path=self.select_path,
            selector=select_type
        )
        self.key = key
        self.current_file_type = file_type
        self.file_manager.ext = allowed_ext
        self.file_manager.show(getcwd())

    def close_file_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        self.selected_paths[self.key] = path
        self.show_snackbar(f"{self.current_file_type} ﺮﯿﺴﻣ: {shorten_path(path, 40)}")
        self.root.ids[self.key].text = f"...{shorten_path(path, 28)}"
        self.close_file_manager()

    # endregion

    # region dropdown
    def open_dropdown(self, dropdown_type, caller):
        self.menus[dropdown_type].caller = caller
        self.menus[dropdown_type].open()

    def set_dropdown_value(self, value, dropdown_type):
        id = f"dropdown_{dropdown_type}"
        self.root.ids[id].text = value
        self.selected_paths[id] = value
        self.menus[dropdown_type].dismiss()

    # endregion

    def submit(self):
        try:
            data = self.collect_input_data()
            if not self.validate_input_data(data):
                self.show_snackbar("ﺪﯿﻨﮐ ﺮﭘ ﻭﺭ ﯽﻟﺎﺧ ﯼﺎﻫ ﺪﻠﯿﻓ")
                return
            self.save_settings(data)
            self.show_snackbar("ﺩﻮﺸﯿﻣ ﺍﺮﺟﺍ ﺕﺎﯿﻠﻤﻋ ﻭ ﺪﺷ ﻩﺮﯿﺧﺫ ﺕﺎﻤﯿﻈﻨﺗ")
            self.run_converter(data)
        except Exception as e:
            self.show_snackbar(str(e))