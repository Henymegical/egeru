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
android.ndk = 25b  # Явно указываем новую версию
android.sdk = 34
android.archs = arm64-v8a, armeabi-v7a
android.permissions = 
    INTERNET,
    ACCESS_NETWORK_STATE,
    WRITE_EXTERNAL_STORAGE,
    READ_EXTERNAL_STORAGE

android.gradle_dependencies =
    com.android.tools.build:gradle:7.4.2,
    androidx.appcompat:appcompat:1.6.1,
    androidx.core:core-ktx:1.12.0

p4a.branch = 2024.1.21
