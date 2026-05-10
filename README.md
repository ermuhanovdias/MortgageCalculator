# Mortgage Calculator (Kivy / KivyMD)

## Русский

Мобильное приложение «Калькулятор ипотеки» на Python с [Kivy](https://kivy.org/) и [KivyMD](https://kivymd.readthedocs.io/).

### Запуск локально

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Сборка APK (Buildozer, Linux или WSL)

```bash
buildozer -f buildozer-32-bit.spec android debug
buildozer -f buildozer-64-bit.spec android debug
```

Для публикации в Google Play нужны **подписанные release**-сборки и загрузка **AAB/APK** для обеих архитектур в консоли Play — см. [документацию Play](https://support.google.com/googleplay/android-developer/).

### Исходный код

Репозиторий: https://github.com/ermuhanovdias/MortgageCalculator

---

## English

Python **mortgage calculator** demo app using **Kivy** and **KivyMD**.

### Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
python main.py
```

### Build APK (Buildozer on Linux/WSL)

```bash
buildozer -f buildozer-32-bit.spec android debug
buildozer -f buildozer-64-bit.spec android debug
```

For **Google Play**, upload signed **release** artifacts for **armeabi-v7a** and **arm64-v8a** (or use AAB) via Play Console.

### Source

https://github.com/ermuhanovdias/MortgageCalculator
