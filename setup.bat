@echo off

set python_installer=python-3.4.4.amd64.msi

msiexec /i %cd%\%python_installer% /quiet /norestart

setx PATH "%PATH%;C:\Python34"

python --version

IF ERRORLEVEL 1 (
    echo Помилка встановлення Python.
    exit /b 1
) ELSE (
    echo Python успішно встановлено.
)

echo Копіювання скрипта в папку автозапуску...

set python_script_path=%cd%\monitoring.py
set bat_file_path=%cd%\run_script.bat

set startup_folder=%USERPROFILE%\Start Menu\Programs\Startup

copy %python_script_path% "%startup_folder%"
copy %bat_file_path% "%startup_folder%"

echo Скрипт успішно скопійовано в папку автозапуску.

echo Процес завершено.
pause
exit
