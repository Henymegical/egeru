
[app]
title = EgeRu
package.name = egeru
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,txt,json
version = 0.1
requirements = 
    python3,
    kivy==2.3.0,
    kivymd==1.2.0,
    android,
    pillow,
    openssl,
    certifi,
    requests

orientation = portrait
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 34
android.archs = arm64-v8a, armeabi-v7a

p4a.branch = master  # Используем главную ветку
