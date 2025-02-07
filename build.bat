@echo off

pyinstaller main.py -w -F --icon favicon.ico --distpath .
rmdir /s /q build
del main.spec