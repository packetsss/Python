@echo off
set /p id=""
echo %id%

cd C:\Users\pyjpa\miniconda3\Scripts
COPY "C:\Users\pyjpa\Desktop\Python\Python Tutorial PyQt5\ui_files\%id%.ui" "C:\Users\pyjpa\miniconda3\Scripts\%id%.ui"

pyuic5.exe -x "%id%.ui" -o "%id%.py"


MOVE /Y "%id%.py" "C:\Users\pyjpa\Desktop\Python\Python Tutorial PyQt5\ui_files\%id%.py"

MOVE /Y "%id%.ui" "C:\Users\pyjpa\Desktop\Python\Python Tutorial PyQt5\ui_files\%id%.ui"


:: COPY "%id%.exe" "C:\Users\pyjpa\Desktop\Python\Python Tutorial PyQt5\ui_files\aj.exe"