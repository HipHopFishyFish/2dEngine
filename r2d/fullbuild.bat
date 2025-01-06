@echo off

python3 build.py %*
pyinstaller --onefile --hidden-import=tkinter --hidden-import=keyboard %1
rmdir /s /q build
del *.spec