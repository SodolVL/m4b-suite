"""
Екран "YouTube Downloader" — завантаження аудіо (MP3) з відео/плейлиста/каналу
для подальшої роботи в M4B Editor.
"""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.list import MDList, OneLineListItem
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

from common.file_manager import AppFileManager


class YoutubeDownloaderScreen(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(16), spacing=dp(12), **kwargs)
        self.save_folder = None
        self.numbering_enabled = False
        self._build_ui()

    def _build_ui(self):
        self.url_field = MDTextField(
            hint_text="Посилання на відео / плейлист / канал",
        )
        self.add_widget(self.url_field)

        row = MDBoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        row.add_widget(MDLabel(text="Нумерація файлів (01_Назва)"))
        switch = MDSwitch()
        switch.bind(active=self.on_numbering_switch)
        row.add_widget(switch)
        self.add_widget(row)

        folder_row = MDBoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        folder_row.add_widget(
            MDRaisedButton(text="Обрати папку збереження", on_release=self.pick_save_folder)
        )
        self.folder_label = MDLabel(text="Папка не обрана")
        folder_row.add_widget(self.folder_label)
        self.add_widget(folder_row)

        self.add_widget(
            MDRaisedButton(
                text="Аналізувати посилання",
                on_release=self.analyze_link,
            )
        )

        self.scroll = ScrollView()
        self.results_list = MDList()
        self.scroll.add_widget(self.results_list)
        self.add_widget(self.scroll)

        self.add_widget(
            MDRaisedButton(
                text="Завантажити обране",
                md_bg_color=(0.2, 0.6, 0.3, 1),
                on_release=self.start_download,
            )
        )

    def on_numbering_switch(self, instance, value):
        self.numbering_enabled = value

    def pick_save_folder(self, *args):
        fm = AppFileManager(
            select_path_callback=self.on_folder_selected,
            select_dir=True,
        )
        fm.open()

    def on_folder_selected(self, path):
        self.save_folder = path
        self.folder_label.text = path

    def analyze_link(self, *args):
        url = self.url_field.text.strip()
        print(f"TODO: викликати yt-dlp --flat-playlist для аналізу {url}")
        # Заглушка результату
        self.results_list.clear_widgets()
        self.results_list.add_widget(OneLineListItem(text="Приклад: Глава 1 (12:34)"))
        self.results_list.add_widget(OneLineListItem(text="Приклад: Глава 2 (15:02)"))

    def start_download(self, *args):
        print(
            f"TODO: запустити yt-dlp завантаження в {self.save_folder}, "
            f"нумерація={self.numbering_enabled}"
        )
