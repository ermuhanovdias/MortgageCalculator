import webbrowser

from kivy.lang import Builder

from kivymd.app import MDApp

SOURCE_CODE_URL = "https://github.com/ermuhanovdias/MortgageCalculator"

KV = """
#:import dp kivy.metrics.dp

MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDNavigationLayout:

        # Order matters: TopAppBar must be last so the menu button receives touches
        # (drawer/s scrim must not sit above the bar).

        MDScreenManager:

            MDScreen:
                name: "main"

                MDScrollView:

                    MDBoxLayout:
                        orientation: "vertical"
                        adaptive_height: True
                        # Reserve space under floating top bar (avoids title overlap with content)
                        padding: "16dp", "72dp", "16dp", "16dp"
                        spacing: "16dp"

                        MDLabel:
                            text: "Привет, калькулятор ипотеки"
                            halign: "center"
                            adaptive_height: True

                        MDTextField:
                            mode: "filled"

                            MDTextFieldHintText:
                                text: "Пример текстового поля"

                            MDTextFieldHelperText:
                                text: "Подсказка под полем"
                                mode: "persistent"

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
            type: "small"
            pos_hint: {"top": 1}

            MDTopAppBarLeadingButtonContainer:

                MDActionTopAppBarButton:
                    icon: "menu"
                    on_release: root.ids.nav_drawer.set_state("toggle")

            MDTopAppBarTitle:
                text: "Калькулятор ипотеки"
"""


class MortgageCalculatorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return Builder.load_string(KV)

    def open_repository(self, *args) -> None:
        drawer = self.root.ids.get("nav_drawer")
        if drawer is not None:
            drawer.set_state("close")
        webbrowser.open(SOURCE_CODE_URL)


MortgageCalculatorApp().run()
