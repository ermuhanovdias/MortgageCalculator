# Default local spec (same as 32-bit). Use: buildozer android debug

[app]

title = Mortgage Calculator

package.name = mortgagecalculator

package.domain = org.mortgagecalculator

source.dir = .

source.include_exts = py,png,jpg,kv,atlas,json

source.include_patterns = data/*

version = 0.3

requirements = python3,kivy,kivymd,pillow

icon.filename = %(source.dir)s/data/logo/logo_512_min.png

presplash.filename = %(source.dir)s/data/logo/presplash_512_kivy_min.png

orientation = all

osx.kivy_version = 2.3.0

fullscreen = 0

android.presplash_color = #263238

android.accept_sdk_license = True

android.api = 33

android.minapi = 21

android.ndk = 25b

android.enable_androidx = True

android.allow_backup = True

android.permissions = INTERNET

android.archs = armeabi-v7a

ios.kivy_ios_url = https://github.com/kivy/kivy-ios

ios.kivy_ios_branch = master

ios.ios_deploy_url = https://github.com/phonegap/ios-deploy

ios.ios_deploy_branch = 1.12.2

ios.codesign.allowed = false

[buildozer]

log_level = 2

warn_on_root = 1
