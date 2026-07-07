"""
Головний застосунок: KivyMD з Bottom Navigation, що об'єднує три інструменти:
1. Створити M4B
2. Редагувати M4B
3. YouTube Downloader
"""

from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem

from screens.create_m4b import CreateM4BScreen
from screens.edit_m4b import EditM4BScreen
from screens.youtube_downloader import YoutubeDownloaderScreen


class M4BSuiteApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"

        root = MDBottomNavigation()

        create_tab = MDBottomNavigationItem(
            name="create_m4b",
            text="Створити M4B",
            icon="headphones",
        )
        create_tab.add_widget(CreateM4BScreen())
        root.add_widget(create_tab)

        edit_tab = MDBottomNavigationItem(
            name="edit_m4b",
            text="Редагувати M4B",
            icon="pencil",
        )
        edit_tab.add_widget(EditM4BScreen())
        root.add_widget(edit_tab)

        youtube_tab = MDBottomNavigationItem(
            name="youtube",
            text="YouTube",
            icon="youtube",
        )
        youtube_tab.add_widget(YoutubeDownloaderScreen())
        root.add_widget(youtube_tab)

        return root


if __name__ == "__main__":
    M4BSuiteApp().run()
