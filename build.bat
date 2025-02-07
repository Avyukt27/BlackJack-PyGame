@echo off

pyinstaller main.py -w -F --distpath .
rmdir /s /q build
del main.spec