@echo off
setlocal

REM Script to run linting and type checking on Windows

REM Navigate to backend directory if running from root
if exist "backend" (
    cd backend
)

REM Check for virtual environment in standard locations and set SCRIPTS directory
set "VENV_SCRIPTS="
if exist "..\.venv\Scripts\python.exe" set "VENV_SCRIPTS=..\.venv\Scripts"
if exist "..\venv\Scripts\python.exe" set "VENV_SCRIPTS=..\venv\Scripts"
if exist ".venv\Scripts\python.exe" set "VENV_SCRIPTS=.venv\Scripts"
if exist "venv\Scripts\python.exe" set "VENV_SCRIPTS=venv\Scripts"

if not defined VENV_SCRIPTS goto :UseGlobal

:UseVenv
echo Using local virtual environment scripts at: "%VENV_SCRIPTS%"
echo Running Ruff...
"%VENV_SCRIPTS%\ruff.exe" check .
echo.
echo Running Mypy...
"%VENV_SCRIPTS%\mypy.exe" .
goto :End

:UseGlobal
echo Virtual environment not found. Trying global commands...
echo Running Ruff...
ruff check .
echo.
echo Running Mypy...
mypy .
goto :End

:End
echo.
echo Linting complete!
