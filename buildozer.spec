[app]
# Заголовок приложения
title = EgeRu
# Имя пакета (без пробелов, в нижнем регистре)
package.name = egeru
# Домены пакета (рекомендуется использовать обратный доменный формат)
package.domain = org.example
# Каталог исходников (корень проекта)
source.dir = .
# Расширения файлов, включаемых в пакет
source.include_exts = py,kv,png,jpg,atlas,ttf,txt,json
# Версия приложения
version = 0.1
# Зависимости (обязательно указываем версии для kivy и kivymd)
requirements = python3,kivy==2.3.0,kivymd==1.1.1,pillow
# Ориентация экрана
orientation = portrait,landscape

# Если есть – укажите файлы иконки и заставки
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

[buildozer]
# Уровень логирования (0 = только ошибки, 1 = информация, 2 = отладка)
log_level = 2
# Предупреждение при запуске от root
warn_on_root = 1

[android]
# Архитектуры для сборки (рекомендуется указывать сразу arm64-v8a и armeabi-v7a)
android.archs = arm64-v8a,armeabi-v7a
# API уровня Android (можно указать актуальный, например 31 или выше)
android.api = 31
# Минимальный поддерживаемый API
android.minapi = 21
# Версия Android SDK
android.sdk = 31
# Версия Android NDK – можно указать 23b (проверьте наличие выбранной версии)
android.ndk = 23b
# Автоматическое принятие лицензий SDK (полезно для автоматизированных сборок)
android.accept_sdk_license = True
# Фильтры для логкат (уменьшаем шум)
android.logcat_filters = *:S python:D
