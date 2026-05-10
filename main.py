from __future__ import annotations

import webbrowser
from typing import Any

from kivy.lang import Builder

from kivymd.app import MDApp

# Repository for "Source code" in-app link (Play update / README).
SOURCE_CODE_URL = "https://github.com/ermuhanovdias/MortgageCalculator"

KV = """
#:import dp kivy.metrics.dp

MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDNavigationLayout:

        MDTopAppBar:
            type: "small"
            pos_hint: {"top": 1}

            MDTopAppBarLeadingButtonContainer:

                MDActionTopAppBarButton:
                    icon: "menu"
                    on_release: nav_drawer.set_state("toggle")

            MDTopAppBarTitle:
                text: "Калькулятор ипотеки"

        MDScreenManager:

            MDScreen:
                name: "main"

                MDScrollView:
                    MDBoxLayout:
                        orientation: "vertical"
                        adaptive_height: True
                        padding: "16dp"
                        spacing: "12dp"

                        MDLabel:
                            text: "Введите параметры кредита"
                            adaptive_height: True
                            role: "large"
                            font_style: "Title"

                        MDTextField:
                            id: field_loan
                            mode: "filled"
                            on_focus: if not self.focus: app.on_loan_focus_out()

                            MDTextFieldLeadingIcon:
                                icon: "cash"

                            MDTextFieldHintText:
                                text: "Сумма кредита (руб.)"

                            MDTextFieldHelperText:
                                text: "Минимум 100"
                                mode: "persistent"

                        MDTextField:
                            id: field_months
                            mode: "filled"
                            on_focus: if not self.focus: app.on_months_focus_out()

                            MDTextFieldLeadingIcon:
                                icon: "calendar-month"

                            MDTextFieldHintText:
                                text: "Срок (месяцев)"

                            MDTextFieldHelperText:
                                text: "Минимум 1"
                                mode: "persistent"

                        MDTextField:
                            id: field_rate
                            mode: "filled"
                            on_focus: if not self.focus: app.on_rate_focus_out()

                            MDTextFieldLeadingIcon:
                                icon: "percent"

                            MDTextFieldHintText:
                                text: "Процентная ставка (% годовых)"

                            MDTextFieldHelperText:
                                text: "Минимум 1%"
                                mode: "persistent"

                        MDLabel:
                            id: label_payment
                            text: "Ежемесячный платёж: —"
                            adaptive_height: True
                            padding: 0, "8dp", 0, 0
                            role: "medium"
                            font_style: "Title"

                        MDButton:
                            style: "tonal"
                            on_release: app.open_source_repository()

                            MDButtonText:
                                text: "Исходный код (GitHub)"

        MDNavigationDrawer:
            id: nav_drawer
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
                        text: "Меню"
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
"""


def _parse_positive_float(text: str, default: float = 0.0) -> float:
    text = (text or "").strip().replace(",", ".")
    if not text:
        return default
    try:
        return float(text)
    except ValueError:
        return default


def monthly_annuity_payment(principal: float, annual_percent: float, months: int) -> float:
    """Annuity payment; if annual rate is 0, use simple division."""
    if months < 1:
        months = 1
    if principal <= 0:
        return 0.0
    if annual_percent <= 0:
        return principal / months
    r = annual_percent / 100.0 / 12.0
    factor = (1.0 + r) ** months
    return principal * (r * factor) / (factor - 1.0)


class MortgageCalculatorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self._loan = 1_000_000.0
        self._months = 120
        self._rate = 12.0
        # self.root is not set until after build() returns; use _ui for ids access.
        self._ui = Builder.load_string(KV)
        self._prime_fields_from_state()
        self._update_payment_label()
        return self._ui

    def open_source_repository(self, *args: Any) -> None:
        webbrowser.open(SOURCE_CODE_URL)

    def on_loan_focus_out(self) -> None:
        raw = _parse_positive_float(self._ui.ids.field_loan.text)
        if raw < 1.0:
            raw = 100.0
        self._loan = raw
        self._ui.ids.field_loan.text = str(int(self._loan))
        self._update_payment_label()

    def on_months_focus_out(self) -> None:
        raw = _parse_positive_float(self._ui.ids.field_months.text)
        months = int(round(raw))
        if months < 1:
            months = 1
        self._months = months
        self._ui.ids.field_months.text = str(self._months)
        self._update_payment_label()

    def on_rate_focus_out(self) -> None:
        raw = _parse_positive_float(self._ui.ids.field_rate.text)
        if raw < 1.0:
            raw = 1.0
        self._rate = raw
        # Show without trailing .0 when integer
        self._ui.ids.field_rate.text = (
            str(int(self._rate)) if self._rate == int(self._rate) else str(self._rate)
        )
        self._update_payment_label()

    def _prime_fields_from_state(self) -> None:
        self._ui.ids.field_loan.text = str(int(self._loan))
        self._ui.ids.field_months.text = str(self._months)
        self._ui.ids.field_rate.text = (
            str(int(self._rate)) if self._rate == int(self._rate) else str(self._rate)
        )

    def _update_payment_label(self) -> None:
        pay = monthly_annuity_payment(self._loan, self._rate, self._months)
        if pay <= 0:
            self._ui.ids.label_payment.text = "Ежемесячный платёж: —"
            return
        rounded = round(pay, 2)
        self._ui.ids.label_payment.text = f"Ежемесячный платёж: {rounded:.2f} руб."


MortgageCalculatorApp().run()
