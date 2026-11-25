@echo off
cd /d "%~dp0"
py -3.11 --version >nul 2>&1
if errorlevel 1 (
 echo Instale Python 3.11 con el lanzador py.
 pause
 exit /b 1
)
if not exist venv\Scripts\python.exe py -3.11 -m venv venv
if errorlevel 1 goto error
call venv\Scripts\activate.bat
if not exist venv\.dependencies_ok (
 python -m pip install -r requirements.txt
 if errorlevel 1 goto error
 echo OK>venv\.dependencies_ok
)
python -m streamlit run app.py
if errorlevel 1 goto error
exit /b 0
:error
echo No se pudo iniciar LPTraffic. Revise Python y las dependencias.
pause
exit /b 1
