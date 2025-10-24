[buildozer]
log_level = 2
warn_on_root = 1

# ...existing code...
[app]
title = DigivinApp
package.name = digivinapp
package.domain = org.digivin
source.dir = .
source.include_exts = py,kv,png,jpg
source.exclude_dirs = database, digivin-app/backend
version = 0.1
# Eliminar pyjnius y cython aquí si no los necesitas en la app móvil
requirements = python3,kivy,kivymd,requests,python-dotenv
android.permissions = INTERNET
orientation = portrait
fullscreen = 0

# Android build options
android.api = 33
android.minapi = 21
android.ndk = 25c
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Forzar compatibilidad Java 1.8 (ayuda con errores javac si aparecen)
android.enable_androidx = True
android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"
# ...existing code...