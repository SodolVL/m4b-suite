"""
Спільний файловий менеджер для застосунку.
Використовує KivyMD MDFileManager, розширений функцією створення папок
та фільтрацією за типом файлу.

Використання (з будь-якого екрану):

    from common.file_manager import AppFileManager

    self.fm = AppFileManager(
        select_path_callback=self.on_file_selected,
        ext_filter=['.mp3'],       # None = показувати всі файли
        select_dir=False,          # True = вибір папки замість файлу
        multiselect=False,         # True = дозволити вибір кількох файлів
    )
    self.fm.open()

    def on_file_selected(self, path):
        print("Обрано:", path)
"""

import os
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivy.utils import platform


def get_storage_root():
    """Повертає кореневу папку сховища залежно від платформи."""
    if platform == "android":
        from android.storage import primary_external_storage_path
        return primary_external_storage_path()
    return os.path.expanduser("~")


class AppFileManager:
    """
    Обгортка над MDFileManager, що додає:
    - фільтр за розширенням файлу
    - режим вибору папки (не тільки файлу)
    - множинний вибір файлів
    - кнопку "Створити нову папку" в поточній директорії
    """

    def __init__(
        self,
        select_path_callback,
        ext_filter=None,
        select_dir=False,
        multiselect=False,
        preview=False,
    ):
        self.select_path_callback = select_path_callback
        self.ext_filter = [e.lower() for e in ext_filter] if ext_filter else None
        self.select_dir = select_dir
        self.multiselect = multiselect
        self.selected_files = []
        self._new_folder_dialog = None

        self.manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=preview,
            selector="folder" if select_dir else "file",
        )

        if self.multiselect:
            self.manager.selector = "multi"

        # Додаємо кнопку створення папки в шапку менеджера
        self.manager.use_access = False

    # ---------- Публічні методи ----------

    def open(self, start_path=None):
        path = start_path or get_storage_root()
        self.manager.show(path)

    def exit_manager(self, *args):
        self.manager.close()

    def select_path(self, path):
        """Викликається при виборі файлу/папки/файлів."""
        if self.ext_filter and not self.select_dir:
            if isinstance(path, list):
                path = [p for p in path if self._matches_filter(p)]
            elif not self._matches_filter(path):
                self.manager.close()
                return

        self.manager.close()
        self.select_path_callback(path)

    def _matches_filter(self, path):
        if os.path.isdir(path):
            return True
        _, ext = os.path.splitext(path)
        return ext.lower() in self.ext_filter

    # ---------- Створення нової папки ----------

    def prompt_create_folder(self, parent_dir, on_created=None):
        """Показує діалог для введення назви нової папки."""
        self._new_folder_parent = parent_dir
        self._on_folder_created = on_created

        self._folder_name_field = MDTextField(
            hint_text="Назва нової папки",
        )

        self._new_folder_dialog = MDDialog(
            title="Створити папку",
            type="custom",
            content_cls=self._folder_name_field,
            buttons=[
                MDFlatButton(
                    text="СКАСУВАТИ",
                    on_release=lambda *a: self._new_folder_dialog.dismiss(),
                ),
                MDFlatButton(
                    text="СТВОРИТИ",
                    on_release=self._do_create_folder,
                ),
            ],
        )
        self._new_folder_dialog.open()

    def _do_create_folder(self, *args):
        name = self._folder_name_field.text.strip()
        if not name:
            self._new_folder_dialog.dismiss()
            return

        new_path = os.path.join(self._new_folder_parent, name)
        try:
            os.makedirs(new_path, exist_ok=True)
        except OSError as e:
            print(f"Помилка створення папки: {e}")

        self._new_folder_dialog.dismiss()

        if self._on_folder_created:
            self._on_folder_created(new_path)
