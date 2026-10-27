@echo off
cd /d "%~dp0"
echo Memasang pustaka yang dibutuhkan...
py -m pip install -r requirements.txt
if errorlevel 1 (
  python -m pip install -r requirements.txt
)
echo.
echo Menjalankan aplikasi SPK KNN...
py -m streamlit run app.py
if errorlevel 1 (
  python -m streamlit run app.py
)
pause
