[app]
title = M4B Suite
package.name = m4bsuite
package.domain = org.vitaliy

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,mutagen,plyer

# Android дозволи: сховище (читання/запис для файлового менеджера, ffmpeg-виводу),
# інтернет (yt-dlp)
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

android.api = 34
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a

orientation = portrait
fullscreen = 0

# icon.filename = %(source.dir)s/icon.png  # додай власну іконку 512x512 і розкоментуй

[buildozer]
log_level = 2
warn_on_root = 1
