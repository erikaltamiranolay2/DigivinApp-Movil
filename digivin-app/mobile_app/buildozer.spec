[buildozer]
log_level = 2
warn_on_root = 1

[app]
title = DigivinApp
package.name = digivinapp
package.domain = org.digivin
source.dir = .
source.include_exts = py,kv,png,jpg
source.exclude_dirs = database, digivin-app/backend
version = 0.1

requirements = python3,kivy,https://github.com/kivy/pyjnius/archive/master.zip
android.permissions = INTERNET
orientation = portrait
fullscreen = 0

# Android build options
android.api = 33
android.minapi = 21
android.ndk = 25c
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.enable_androidx = True
android.add_compile_options = sourceCompatibility=1.8,targetCompatibility=1.8
