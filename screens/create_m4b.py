"""
Екран "Створити M4B" — вибір MP3, список розділів з операціями:
перейменування, порядок, об'єднання, обрізка, розбиття.
"""

import os
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

from common.file_manager import AppFileManager


class ChapterListItem(OneLineIconListItem):
    """Один пункт списку розділів з кнопками дій."""

    def __init__(self, chapter, index, screen, **kwargs):
        super().__init__(**kwargs)
        self.chapter = chapter
        self.index = index
        self.screen = screen
        self.text = chapter["title"]
        self.add_widget(IconLeftWidget(icon="file-music"))


class CreateM4BScreen(MDBoxLayout):
    """
    Головний контейнер для інструменту "Створити M4B".
    chapters: список dict {"title": str, "path": str, "start": float, "end": float}
    """

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.chapters = []
        self.fm = None

        self._build_ui()

    def _build_ui(self):
        # Верхня панель дій
        top_bar = MDBoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8), padding=dp(8))
        top_bar.add_widget(
            MDRaisedButton(text="Вибрати MP3", on_release=self.pick_mp3_files)
        )
        top_bar.add_widget(
            MDRaisedButton(text="Метадані та обкладинка", on_release=self.open_metadata)
        )
        top_bar.add_widget(
            MDRaisedButton(text="Якість звуку", on_release=self.open_quality_settings)
        )
        self.add_widget(top_bar)

        # Список розділів
        from kivymd.uix.list import MDList
        from kivy.uix.scrollview import ScrollView

        self.scroll = ScrollView()
        self.chapter_list = MDList()
        self.scroll.add_widget(self.chapter_list)
        self.add_widget(self.scroll)

        # Нижня панель — конвертація
        bottom_bar = MDBoxLayout(size_hint_y=None, height=dp(56), padding=dp(8))
        bottom_bar.add_widget(
            MDRaisedButton(
                text="Конвертувати в M4B",
                on_release=self.start_conversion,
                md_bg_color=(0.2, 0.6, 0.3, 1),
            )
        )
        self.add_widget(bottom_bar)

    # ---------- Вибір файлів ----------

    def pick_mp3_files(self, *args):
        self.fm = AppFileManager(
            select_path_callback=self.on_mp3_selected,
            ext_filter=[".mp3"],
            multiselect=True,
        )
        self.fm.open()

    def on_mp3_selected(self, paths):
        if isinstance(paths, str):
            paths = [paths]
        for p in paths:
            self.chapters.append({
                "title": os.path.splitext(os.path.basename(p))[0],
                "path": p,
                "start": None,
                "end": None,
            })
        self.refresh_chapter_list()

    # ---------- Відображення списку ----------

    def refresh_chapter_list(self):
        self.chapter_list.clear_widgets()
        for i, chapter in enumerate(self.chapters):
            item = ChapterListItem(chapter=chapter, index=i, screen=self)
            self.chapter_list.add_widget(item)

    # ---------- Дії над розділами (заглушки — наступний крок) ----------

    def rename_chapter(self, index, new_title):
        self.chapters[index]["title"] = new_title
        self.refresh_chapter_list()

    def move_chapter(self, index, direction):
        new_index = index + direction
        if 0 <= new_index < len(self.chapters):
            self.chapters[index], self.chapters[new_index] = (
                self.chapters[new_index],
                self.chapters[index],
            )
            self.refresh_chapter_list()

    def open_metadata(self, *args):
        print("TODO: відкрити екран метаданих (назва, автор, обкладинка, цикл...)")

    def open_quality_settings(self, *args):
        print("TODO: відкрити екран якості звуку (нормалізація, шумозаглушення, компресор, бітрейт, гучність)")

    def start_conversion(self, *args):
        print(f"TODO: запустити ffmpeg-конвертацію для {len(self.chapters)} розділів")
