import webbrowser

from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsItemText, MDTabsPrimary

SOURCE_CODE_URL = "https://github.com/ermuhanovdias/MortgageCalculator"

# Tabs + first-tab form live in KV below (lesson: declarative UI, no programmatic tab loop).
KV = """
#:import Clock kivy.clock.Clock
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

                        MDTabsItem:
                            MDTabsItemIcon:
                                icon: "calculator"
                            MDTabsItemText:
                                text: "Ипотека"

                        MDTabsItem:
                            MDTabsItemIcon:
                                icon: "chart-line"
                            MDTabsItemText:
                                text: "Графики"

                        MDTabsItem:
                            MDTabsItemIcon:
                                icon: "information-outline"
                            MDTabsItemText:
                                text: "Инфо"

                        MDDivider:

                        MDTabsCarousel:
                            id: tab_carousel
                            size_hint_y: 1

                            MDScrollView:
                                do_scroll_x: False
                                size_hint: 1, 1

                                MDBoxLayout:
                                    orientation: "vertical"
                                    spacing: dp(12)
                                    padding: dp(16)
                                    size_hint_y: None
                                    height: self.minimum_height

                                    MDLabel:
                                        text: "Параметры кредита"
                                        adaptive_height: True
                                        bold: True

                                    MDTextField:
                                        mode: "filled"
                                        size_hint_y: None
                                        height: dp(96)
                                        input_filter: "float"
                                        MDTextFieldLeadingIcon:
                                            icon: "home-variant-outline"
                                        MDTextFieldHintText:
                                            text: "Стоимость недвижимости, ₽"
                                        MDTextFieldHelperText:
                                            text: "Оценочная или договорная цена объекта"
                                            mode: "persistent"

                                    MDTextField:
                                        mode: "filled"
                                        size_hint_y: None
                                        height: dp(96)
                                        input_filter: "int"
                                        MDTextFieldLeadingIcon:
                                            icon: "calendar"
                                        MDTextFieldHintText:
                                            text: "Срок кредита, лет"
                                        MDTextFieldHelperText:
                                            text: "Полных лет (например, 20)"
                                            mode: "persistent"

                                    MDTextField:
                                        mode: "filled"
                                        size_hint_y: None
                                        height: dp(96)
                                        input_filter: "float"
                                        MDTextFieldLeadingIcon:
                                            icon: "cash"
                                        MDTextFieldHintText:
                                            text: "Сумма кредита, ₽"
                                        MDTextFieldHelperText:
                                            text: "Обычно цена минус первоначальный взнос"
                                            mode: "persistent"

                                    MDBoxLayout:
                                        orientation: "horizontal"
                                        spacing: dp(8)
                                        size_hint_y: None
                                        height: dp(96)

                                        MDTextField:
                                            mode: "filled"
                                            size_hint_x: 0.42
                                            size_hint_y: None
                                            height: dp(96)
                                            input_filter: "float"
                                            MDTextFieldLeadingIcon:
                                                icon: "bank"
                                            MDTextFieldHintText:
                                                text: "Ставка, % годовых"
                                            MDTextFieldHelperText:
                                                text: "Годовых, в процентах"
                                                mode: "persistent"

                                        MDTextField:
                                            mode: "filled"
                                            size_hint_x: 0.58
                                            size_hint_y: None
                                            height: dp(96)
                                            input_filter: "float"
                                            MDTextFieldLeadingIcon:
                                                icon: "wallet-outline"
                                            MDTextFieldHintText:
                                                text: "Первоначальный взнос, ₽"
                                            MDTextFieldHelperText:
                                                text: "Сумма взноса при оформлении"
                                                mode: "persistent"

                                    MDTextField:
                                        mode: "filled"
                                        size_hint_y: None
                                        height: dp(96)
                                        MDTextFieldLeadingIcon:
                                            icon: "credit-card-outline"
                                        MDTextFieldHintText:
                                            text: "Тип платежа"
                                        MDTextFieldHelperText:
                                            text: "Аннуитет или дифференцированный график"
                                            mode: "persistent"

                            MDBoxLayout:
                                orientation: "vertical"
                                size_hint: 1, 1

                                MDLabel:
                                    text: "Раздел «Графики» — контент позже."
                                    halign: "center"
                                    valign: "middle"
                                    size_hint: 1, 1

                            MDBoxLayout:
                                orientation: "vertical"
                                size_hint: 1, 1

                                MDLabel:
                                    text: "Раздел «Инфо» — кратко о приложении. Исходный код: меню слева → «Исходный код»."
                                    halign: "center"
                                    valign: "middle"
                                    size_hint: 1, 1

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
        carousel = self.root.ids.tab_carousel
        top_bar = self.root.ids.top_bar

        tabs.bind(on_tab_switch=self._on_tabs_switch)

        # Dark app bar + dark tab strip (indicator still uses primary palette).
        dark_bg = getattr(self.theme_cls, "bg_dark", "#000000")
        tabs.md_bg_color = dark_bg
        top_bar.md_bg_color = dark_bg

        # Content area below tabs.
        carousel.md_bg_color = "#FFFFFF"

        tabs.switch_tab(icon="calculator")

    def open_repository(self, *args) -> None:
        drawer = self.root.ids.get("nav_drawer")
        if drawer is not None:
            drawer.set_state("close")
        webbrowser.open(SOURCE_CODE_URL)


MortgageCalculatorApp().run()
