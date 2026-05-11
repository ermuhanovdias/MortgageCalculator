import webbrowser

from kivy.lang import Builder
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.tab import (
    MDTabsCarousel,
    MDTabsItem,
    MDTabsItemIcon,
    MDTabsItemText,
    MDTabsPrimary,
)
from kivymd.uix.textfield import (
    MDTextField,
    MDTextFieldHelperText,
    MDTextFieldHintText,
)

SOURCE_CODE_URL = "https://github.com/ermuhanovdias/MortgageCalculator"

# Icons and titles for horizontal tabs (mortgage app sections).
TAB_ITEMS = (
    ("calculator", "Ипотека"),
    ("chart-line", "Графики"),
    ("information-outline", "Инфо"),
)

KV = """
#:import dp kivy.metrics.dp

MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDNavigationLayout:

        MDScreenManager:

            MDScreen:
                name: "main"

                MDBoxLayout:
                    orientation: "vertical"
                    # Toolbar is MDTopAppBar (~56dp small); tabs sit flush below it like Material layout
                    padding: 0, dp(56), 0, 0
                    spacing: 0

                    MDTabsPrimary:
                        id: main_tabs
                        size_hint_y: 1
                        indicator_anim: False

                        MDDivider:

                        MDTabsCarousel:
                            id: tab_carousel
                            size_hint_y: 1

        MDNavigationDrawer:
            id: nav_drawer
            drawer_type: "modal"
            radius: (0, dp(16), dp(16), 0)

            MDNavigationDrawerMenu:

                MDNavigationDrawerHeader:
                    orientation: "vertical"
                    padding: 0, 0, 0, "12dp"
                    adaptive_height: True

                    MDLabel:
                        text: "Калькулятор ипотеки"
                        adaptive_height: True
                        padding: "16dp", 0, "16dp", 0
                        font_style: "Display"
                        role: "small"

                    MDLabel:
                        text: "Меню навигации"
                        adaptive_height: True
                        padding: "18dp", 0, "18dp", 0
                        font_style: "Title"
                        role: "large"

                MDNavigationDrawerDivider:

                MDNavigationDrawerLabel:
                    text: "Разделы"

                MDNavigationDrawerItem:
                    MDNavigationDrawerItemLeadingIcon:
                        icon: "calculator"
                    MDNavigationDrawerItemText:
                        text: "Расчёт ипотеки"

                MDNavigationDrawerItem:
                    MDNavigationDrawerItemLeadingIcon:
                        icon: "chart-line"
                    MDNavigationDrawerItemText:
                        text: "Графики и диаграммы"

                MDNavigationDrawerItem:
                    on_release: app.open_repository()
                    MDNavigationDrawerItemLeadingIcon:
                        icon: "github"
                    MDNavigationDrawerItemText:
                        text: "Исходный код"

                MDNavigationDrawerDivider:

                MDNavigationDrawerLabel:
                    text: "Дополнительно"

                MDNavigationDrawerItem:
                    MDNavigationDrawerItemLeadingIcon:
                        icon: "information-outline"
                    MDNavigationDrawerItemText:
                        text: "О приложении"

        MDTopAppBar:
            id: top_bar
            type: "small"
            pos_hint: {"top": 1}

            MDTopAppBarLeadingButtonContainer:

                MDActionTopAppBarButton:
                    icon: "menu"
                    on_release: root.ids.nav_drawer.set_state("toggle")

            MDTopAppBarTitle:
                text: "Калькулятор ипотеки"

            MDTopAppBarTrailingButtonContainer:
                MDActionTopAppBarButton:
                    icon: "star"
                    on_release: app.open_repository()
"""


def _build_mortgage_tab_content() -> MDScrollView:
    """First tab: same demo content as before (greeting + sample field)."""
    box = MDBoxLayout(
        orientation="vertical",
        adaptive_height=True,
        padding=dp(16),
        spacing=dp(16),
    )
    box.add_widget(
        MDLabel(
            text="Привет, калькулятор ипотеки",
            halign="center",
            adaptive_height=True,
        )
    )
    field = MDTextField(
        mode="filled",
    )
    field.add_widget(MDTextFieldHintText(text="Пример текстового поля"))
    field.add_widget(
        MDTextFieldHelperText(
            text="Подсказка под полем",
            mode="persistent",
        )
    )
    box.add_widget(field)
    scroll = MDScrollView()
    scroll.add_widget(box)
    return scroll


class MortgageCalculatorApp(MDApp):
    def build(self):
        # Reference UI: dark top bar + tabs, but white content area.
        # We use Light theme as a base so the content renders on a light surface.
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        return Builder.load_string(KV)

    def _on_tabs_switch(self, tabs: MDTabsPrimary, tab_item, tab_content) -> None:
        """Triggered every time the current tab is changed."""
        tab_title = None
        try:
            if tab_item is not None and hasattr(tab_item, "walk"):
                for w in tab_item.walk():
                    if isinstance(w, MDTabsItemText):
                        tab_title = w.text
                        break
        except Exception:
            tab_title = None

        # Keep logs in English (required).
        print(f"Tab switched: {tab_title}")

    def on_start(self) -> None:
        tabs: MDTabsPrimary = self.root.ids.main_tabs
        carousel: MDTabsCarousel = self.root.ids.tab_carousel
        top_bar = self.root.ids.top_bar

        tabs.bind(on_tab_switch=self._on_tabs_switch)

        # Dark app bar + dark tab strip (indicator still uses primary palette).
        dark_bg = getattr(self.theme_cls, "bg_dark", "#000000")
        tabs.md_bg_color = dark_bg
        top_bar.md_bg_color = dark_bg

        # Content area below tabs.
        carousel.md_bg_color = "#FFFFFF"

        for index, (icon, title) in enumerate(TAB_ITEMS):
            tabs.add_widget(
                MDTabsItem(
                    MDTabsItemIcon(icon=icon),
                    MDTabsItemText(text=title),
                )
            )
            if index == 0:
                carousel.add_widget(_build_mortgage_tab_content())
            elif index == 1:
                carousel.add_widget(
                    MDLabel(
                        text="Раздел «Графики» — контент позже.",
                        halign="center",
                        valign="middle",
                        size_hint=(1, 1),
                    )
                )
            else:
                carousel.add_widget(
                    MDLabel(
                        text="Раздел «Инфо» — кратко о приложении.\n"
                        "Исходный код: меню слева → «Исходный код».",
                        halign="center",
                        valign="middle",
                        size_hint=(1, 1),
                    )
                )

        tabs.switch_tab(icon=TAB_ITEMS[0][0])

    def open_repository(self, *args) -> None:
        drawer = self.root.ids.get("nav_drawer")
        if drawer is not None:
            drawer.set_state("close")
        webbrowser.open(SOURCE_CODE_URL)


MortgageCalculatorApp().run()
