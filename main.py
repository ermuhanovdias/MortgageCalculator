import webbrowser

from kivy.clock import Clock
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
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
                                icon: "view-grid-outline"
                            MDTabsItemText:
                                text: "Input"

                        MDTabsItem:
                            MDTabsItemIcon:
                                icon: "table"
                            MDTabsItemText:
                                text: "Table"

                        MDTabsItem:
                            MDTabsItemIcon:
                                icon: "chart-line"
                            MDTabsItemText:
                                text: "Graph"

                        MDTabsItem:
                            MDTabsItemIcon:
                                icon: "chart-pie"
                            MDTabsItemText:
                                text: "Chart"

                        MDTabsItem:
                            MDTabsItemIcon:
                                icon: "book-open-variant"
                            MDTabsItemText:
                                text: "Sum"

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

                                    # Like reference: stacked filled fields with hint only (no persistent helper).
                                    MDTextField:
                                        mode: "filled"
                                        size_hint_y: None
                                        height: self.minimum_height
                                        input_filter: "float"
                                        MDTextFieldLeadingIcon:
                                            icon: "home-variant-outline"
                                        MDTextFieldHintText:
                                            text: "Стоимость недвижимости, ₽"

                                    MDTextField:
                                        mode: "filled"
                                        size_hint_y: None
                                        height: self.minimum_height
                                        input_filter: "int"
                                        MDTextFieldLeadingIcon:
                                            icon: "calendar"
                                        MDTextFieldHintText:
                                            text: "Срок кредита, лет"

                                    MDTextField:
                                        mode: "filled"
                                        size_hint_y: None
                                        height: self.minimum_height
                                        input_filter: "float"
                                        MDTextFieldLeadingIcon:
                                            icon: "cash"
                                        MDTextFieldHintText:
                                            text: "Сумма кредита, ₽"

                                    MDTextField:
                                        mode: "filled"
                                        size_hint_y: None
                                        height: self.minimum_height
                                        input_filter: "float"
                                        MDTextFieldLeadingIcon:
                                            icon: "wallet-outline"
                                        MDTextFieldHintText:
                                            text: "Первоначальный взнос, ₽"

                                    # Bottom row: icon on the left field only (same pattern as Interest / Payment type).
                                    MDBoxLayout:
                                        orientation: "horizontal"
                                        spacing: dp(8)
                                        size_hint_y: None
                                        height: self.minimum_height

                                        MDTextField:
                                            mode: "filled"
                                            size_hint_x: 0.5
                                            size_hint_y: None
                                            height: self.minimum_height
                                            input_filter: "float"
                                            MDTextFieldLeadingIcon:
                                                icon: "bank"
                                            MDTextFieldHintText:
                                                text: "Ставка, % годовых"

                                        MDTextField:
                                            id: field_payment_type
                                            mode: "filled"
                                            size_hint_x: 0.5
                                            size_hint_y: None
                                            height: self.minimum_height
                                            on_focus: if self.focus: app.open_payment_type_menu()
                                            MDTextFieldHintText:
                                                text: "Тип платежа"

                            MDBoxLayout:
                                orientation: "vertical"
                                size_hint: 1, 1

                                MDLabel:
                                    text: "Таблица — график платежей (скоро)."
                                    halign: "center"
                                    valign: "middle"
                                    size_hint: 1, 1

                            MDBoxLayout:
                                orientation: "vertical"
                                size_hint: 1, 1

                                MDLabel:
                                    text: "График — кривые и динамика (скоро)."
                                    halign: "center"
                                    valign: "middle"
                                    size_hint: 1, 1

                            MDBoxLayout:
                                orientation: "vertical"
                                size_hint: 1, 1

                                MDLabel:
                                    text: "Диаграммы — визуализация (скоро)."
                                    halign: "center"
                                    valign: "middle"
                                    size_hint: 1, 1

                            MDBoxLayout:
                                orientation: "vertical"
                                size_hint: 1, 1

                                MDLabel:
                                    text: "Итоги — сводка по кредиту (скоро)."
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
                text: "Mortgage Calculator"

            MDTopAppBarTrailingButtonContainer:
                MDActionTopAppBarButton:
                    icon: "star"
                    on_release: app.open_repository()
"""


class MortgageCalculatorApp(MDApp):
    payment_type_menu: MDDropdownMenu | None = None

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

        tabs.switch_tab(icon="view-grid-outline")

        self._setup_payment_type_dropdown()

    def _setup_payment_type_dropdown(self) -> None:
        """Bind MDDropdownMenu to payment type field (lesson: annuity vs differentiated)."""
        field = self.root.ids.field_payment_type
        menu_items = [
            {
                "text": "Аннуитетный",
                "leading_icon": "chart-timeline-variant",
                "on_release": lambda *a, t="Аннуитетный": self._on_payment_type_chosen(t),
            },
            {
                "text": "Дифференцированный",
                "leading_icon": "chart-line-variant",
                "on_release": lambda *a, t="Дифференцированный": self._on_payment_type_chosen(t),
            },
        ]
        self.payment_type_menu = MDDropdownMenu(
            caller=field,
            items=menu_items,
            position="bottom",
            width_mult=5,
        )

    def open_payment_type_menu(self, *args) -> None:
        """KV calls this when the payment type field gains focus."""
        if self.payment_type_menu:
            self.payment_type_menu.open()

    def _on_payment_type_chosen(self, label: str) -> None:
        """Write selected menu text into the field and close menu (lesson pattern)."""
        if self.payment_type_menu:
            self.payment_type_menu.dismiss()

        def apply_choice(_dt):
            field = self.root.ids.field_payment_type
            field.text = label
            field.focus = False

        # Small delay so dismiss finishes before updating text (similar to lesson Clock.schedule_once).
        Clock.schedule_once(apply_choice, 0.05)

    def open_repository(self, *args) -> None:
        drawer = self.root.ids.get("nav_drawer")
        if drawer is not None:
            drawer.set_state("close")
        webbrowser.open(SOURCE_CODE_URL)


# If dropdown menus misbehave on some KivyMD builds, pin a known-good version, e.g.:
#   pip install "kivy>=2.3,<3" "kivymd>=2.0.0" --upgrade
# On Android, soft keyboard + overlays sometimes need: Window.softinput_mode (see Kivy docs).


MortgageCalculatorApp().run()
