import webbrowser
from datetime import date
from kivy.clock import Clock
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDModalDatePicker
from kivymd.uix.tab import MDTabsItemText, MDTabsPrimary

SOURCE_CODE_URL = "https://github.com/ermuhanovdias/MortgageCalculator"


def _fmt_rub(value: float) -> str:
    """Format amount as integer rubles with spaces as thousands separators."""
    s = f"{round(value):,}".replace(",", " ")
    return f"{s} ₽"


def _fmt_pct(value: float) -> str:
    return f"{value:.2f} %"


def _parse_start_date(raw: str) -> date | None:
    raw = (raw or "").strip().replace("/", ".")
    if not raw:
        return None
    parts = raw.split(".")
    if len(parts) != 3:
        return None
    try:
        d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
        return date(y, m, d)
    except (ValueError, OverflowError):
        return None


def _monthly_rate_percent(annual_percent: float) -> float:
    """Monthly rate as decimal (e.g. 0.007916 for 9.5% p.a.)."""
    return (annual_percent / 100.0) / 12.0


def _annuity_monthly_payment(principal: float, annual_percent: float, n_months: int) -> float:
    if n_months <= 0 or principal <= 0:
        return 0.0
    i = _monthly_rate_percent(annual_percent)
    if i <= 0:
        return principal / n_months
    pow_term = (1.0 + i) ** n_months
    return principal * (i * pow_term) / (pow_term - 1.0)


def _effective_annual_percent(nominal_annual_percent: float) -> float:
    """EAR from nominal annual rate with monthly compounding (lesson-style headline rate)."""
    i = _monthly_rate_percent(nominal_annual_percent)
    if i <= 0:
        return 0.0
    return 100.0 * ((1.0 + i) ** 12 - 1.0)


def _totals_annuity(principal: float, annual_percent: float, n_months: int) -> tuple[float, float, float]:
    """Returns (monthly_payment, total_interest, total_paid)."""
    monthly = _annuity_monthly_payment(principal, annual_percent, n_months)
    total_paid = monthly * n_months
    return monthly, max(0.0, total_paid - principal), total_paid


def _totals_differentiated(principal: float, annual_percent: float, n_months: int) -> tuple[float, float, float, float]:
    """
    Returns (first_month_payment, last_month_payment, total_interest, total_paid).
    """
    if n_months <= 0 or principal <= 0:
        return 0.0, 0.0, 0.0, 0.0
    i = _monthly_rate_percent(annual_percent)
    principal_part = principal / n_months
    balance = principal
    total_interest = 0.0
    total_paid = 0.0
    first_pay = 0.0
    last_pay = 0.0
    for month_idx in range(n_months):
        interest = balance * i
        pay = principal_part + interest
        total_interest += interest
        total_paid += pay
        balance -= principal_part
        if month_idx == 0:
            first_pay = pay
        last_pay = pay
    return first_pay, last_pay, total_interest, total_paid


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

                                    MDTextField:
                                        id: field_start_date
                                        mode: "filled"
                                        size_hint_y: None
                                        height: self.minimum_height
                                        on_focus: if self.focus: app.open_start_date_picker()
                                        MDTextFieldLeadingIcon:
                                            icon: "calendar"
                                        MDTextFieldHintText:
                                            text: "Дата начала"

                                    # Like reference: stacked filled fields with hint only (no persistent helper).
                                    MDTextField:
                                        id: field_property_price
                                        mode: "filled"
                                        size_hint_y: None
                                        height: self.minimum_height
                                        input_filter: "float"
                                        MDTextFieldLeadingIcon:
                                            icon: "home-variant-outline"
                                        MDTextFieldHintText:
                                            text: "Стоимость недвижимости, ₽"

                                    MDTextField:
                                        id: field_term_years
                                        mode: "filled"
                                        size_hint_y: None
                                        height: self.minimum_height
                                        input_filter: "int"
                                        MDTextFieldLeadingIcon:
                                            icon: "calendar-clock"
                                        MDTextFieldHintText:
                                            text: "Срок кредита, лет"

                                    MDTextField:
                                        id: field_loan_amount
                                        mode: "filled"
                                        size_hint_y: None
                                        height: self.minimum_height
                                        input_filter: "float"
                                        MDTextFieldLeadingIcon:
                                            icon: "cash"
                                        MDTextFieldHintText:
                                            text: "Сумма кредита, ₽"

                                    MDTextField:
                                        id: field_down_payment
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
                                            id: field_rate
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

                                    MDButton:
                                        style: "filled"
                                        size_hint_x: 1
                                        size_hint_y: None
                                        height: dp(48)
                                        on_release: app.calculate()
                                        MDButtonText:
                                            text: "Рассчитать"

                                    MDLabel:
                                        text: "Результаты расчёта"
                                        adaptive_height: True
                                        bold: True

                                    MDLabel:
                                        id: label_result_monthly
                                        adaptive_height: True
                                        text: "—"

                                    MDLabel:
                                        id: label_result_interest
                                        adaptive_height: True
                                        text: "—"

                                    MDLabel:
                                        id: label_result_total
                                        adaptive_height: True
                                        text: "—"

                                    MDLabel:
                                        id: label_result_effective
                                        adaptive_height: True
                                        text: "—"

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
        self._apply_default_form_values()
        # Lesson: run same calculation as the button so the screen shows numbers on launch.
        Clock.schedule_once(lambda _dt: self.calculate(), 0.15)

    def calculate(self, *args) -> None:
        """
        Read Input tab fields, compute mortgage summary (no input validation yet — lesson scope).
        Updates result labels; logs in English.
        """
        ids = self.root.ids
        start_d = _parse_start_date(ids.field_start_date.text)

        try:
            principal = float((ids.field_loan_amount.text or "0").replace(" ", "").replace(",", "."))
            years_f = float((ids.field_term_years.text or "0").replace(",", "."))
            n_months = max(0, int(round(years_f * 12)))
            annual = float((ids.field_rate.text or "0").replace(",", "."))
        except ValueError:
            ids.label_result_monthly.text = "Ошибка: проверьте числовые поля"
            ids.label_result_interest.text = "—"
            ids.label_result_total.text = "—"
            ids.label_result_effective.text = "—"
            print("Calculate failed: invalid numeric input")
            return
        pay_type = (ids.field_payment_type.text or "").strip()

        if start_d:
            print(f"Calculate using start date: {start_d.isoformat()}")
        else:
            print("Calculate: start date not parsed, continuing with loan math only")

        eff = _effective_annual_percent(annual)

        if n_months <= 0 or principal <= 0:
            ids.label_result_monthly.text = "Платёж: —"
            ids.label_result_interest.text = "Переплата по процентам: —"
            ids.label_result_total.text = "Общая сумма выплат: —"
            ids.label_result_effective.text = f"Эффективная ставка (год): {_fmt_pct(eff)}"
            print("Calculate skipped: invalid principal or term")
            return

        if pay_type == "Дифференцированный":
            first_m, last_m, interest, total = _totals_differentiated(principal, annual, n_months)
            ids.label_result_monthly.text = (
                f"Платёж: {_fmt_rub(first_m)} (1-й мес.) → {_fmt_rub(last_m)} (последний)"
            )
        else:
            monthly, interest, total = _totals_annuity(principal, annual, n_months)
            ids.label_result_monthly.text = f"Ежемесячный платёж: {_fmt_rub(monthly)}"

        ids.label_result_interest.text = f"Переплата по процентам: {_fmt_rub(interest)}"
        ids.label_result_total.text = f"Общая сумма выплат: {_fmt_rub(total)}"
        ids.label_result_effective.text = f"Эффективная ставка (год): {_fmt_pct(eff)}"

        print(
            f"Calculate done: type={pay_type!r}, principal={principal}, months={n_months}, "
            f"interest={interest:.2f}, total={total:.2f}"
        )

    def _apply_default_form_values(self) -> None:
        """Lesson defaults: sample loan params + today's date in the start date field."""
        ids = self.root.ids
        ids.field_start_date.text = date.today().strftime("%d.%m.%Y")
        ids.field_property_price.text = "5000000"
        ids.field_term_years.text = "10"
        ids.field_loan_amount.text = "5000000"
        ids.field_down_payment.text = "0"
        ids.field_rate.text = "9.5"
        ids.field_payment_type.text = "Аннуитетный"

    def open_start_date_picker(self, *args) -> None:
        """Open modal date picker (KivyMD 2.x: bind on_ok / on_cancel, not callback)."""
        field = self.root.ids.field_start_date
        picker_date = date.today()
        raw = (field.text or "").strip().replace("/", ".")
        if raw:
            parts = raw.split(".")
            if len(parts) == 3:
                try:
                    d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
                    picker_date = date(y, m, d)
                except (ValueError, OverflowError):
                    pass
        dlg = MDModalDatePicker(
            year=picker_date.year,
            month=picker_date.month,
            day=picker_date.day,
        )
        dlg.bind(on_ok=self._on_start_date_ok, on_cancel=self._on_start_date_cancel)
        dlg.open()

    def _on_start_date_ok(self, picker_instance: MDModalDatePicker) -> None:
        chosen = picker_instance.get_date()[0]
        field = self.root.ids.field_start_date
        field.text = chosen.strftime("%d.%m.%Y")
        field.focus = False
        print(f"Start date selected: {chosen.isoformat()}")

    def _on_start_date_cancel(self, picker_instance: MDModalDatePicker) -> None:
        self.root.ids.field_start_date.focus = False
        print("Start date picker cancelled")

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
