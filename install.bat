@echo off

:start
cls

:errorNoPython

echo.
echo Error^: Python not installed
echo.
echo.
echo Downloading Python 3.7.0...
IF EXIST "%CD%\python-3.7.0.exe" (
  echo Found Installer at "%CD%\python-3.7.0.exe"
) ELSE (
  powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12, [Net.SecurityProtocolType]::Tls11, [Net.SecurityProtocolType]::Ssl3, [Net.SecurityProtocolType]::Tls; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.7.0/python-3.7.0.exe' -OutFile '%CD%\python-3.7.0.exe';}"
  echo Python download completed.
)

echo Installing Python...
powershell %CD%\python-3.7.0.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0 TargetDir=c:\Python\Python370
setx path "%PATH%;C:\Python\Python370\"
set "path=%PATH%;C:\Python\Python370\"

timeout /t 30 /nobreak > nul
echo Python Installation completed.
echo Installing python dependencies.
**start cmd /k python -m pip install requests
start cmd /k python -m pip install pyjavaproperties**

set python_ver=39

python get-pip.py

cd \
cd \python%python_ver%\Scripts\
pip install networkx
pip install pygame

pause
exit