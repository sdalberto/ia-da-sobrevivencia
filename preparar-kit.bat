@echo off
REM IA da Sobrevivencia - preparar o kit (PRECISA DE INTERNET, rode uma vez)
chcp 65001 >nul
cd /d "%~dp0"
set "PY="
if exist "%~dp0runtime\python\windows-x86_64\python\python.exe" set "PY=%~dp0runtime\python\windows-x86_64\python\python.exe"
if not defined PY (
  where py >nul 2>nul && set "PY=py -3"
)
if not defined PY (
  where python >nul 2>nul && set "PY=python"
)
if not defined PY (
  echo.
  echo  Python nao encontrado. Instale o Python 3 em https://www.python.org/downloads/
  echo  (marque "Add python.exe to PATH") e rode este arquivo de novo.
  echo  Depois, o preparador pode incluir um Python portatil no kit.
  echo.
  pause
  exit /b 1
)
%PY% "%~dp0sobrevivencia.py" %* prepare
pause
