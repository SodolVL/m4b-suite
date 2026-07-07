"""
Екран "Редагувати M4B" — вибір готового M4B, автозчитування chapters/метаданих,
далі той самий функціонал, що й у "Створити M4B".
"""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

from common.file_manager import AppFileManager
from screens.create_m4b import CreateM4BScreen


class EditM4BScreen(MDBoxLayout):
    """
    Обгортка над CreateM4BScreen: спочатку просить обрати готовий M4B,
    зчитує з нього chapters/метадані/обкладинку, а далі показує той самий
    редактор списку розділів.
    """

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.fm = None
        self.editor = None
        self._build_ui()

    def _build_ui(self):
        self.intro_box = MDBoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        self.intro_box.add_widget(
            MDLabel(text="Оберіть готовий M4B-файл для редагування", halign="center")
        )
        self.intro_box.add_widget(
            MDRaisedButton(
                text="Вибрати M4B",
                pos_hint={"center_x": 0.5},
                on_release=self.pick_m4b_file,
            )
        )
        self.add_widget(self.intro_box)

    def pick_m4b_file(self, *args):
        self.fm = AppFileManager(
            select_path_callback=self.on_m4b_selected,
            ext_filter=[".m4b"],
            multiselect=False,
        )
        self.fm.open()

    def on_m4b_selected(self, path):
        print(f"TODO: зчитати chapters/метадані/обкладинку з {path} (ffprobe)")
        chapters = self._read_chapters_stub(path)

        # Ховаємо вступний екран, показуємо повний редактор
        self.remove_widget(self.intro_box)
        self.editor = CreateM4BScreen()
        self.editor.chapters = chapters
        self.editor.refresh_chapter_list()
        self.add_widget(self.editor)

    def _read_chapters_stub(self, path):
        """
        TODO: реалізувати через ffprobe:
        ffprobe -i input.m4b -print_format json -show_chapters
        Поки що повертає порожній список — заповнюється реальним парсингом пізніше.
        """
        return []
