@echo off
cd /d %~dp0
set CURRENT_DIR=%cd%
call winkbvenv\Scripts\activate
cd /d %CURRENT_DIR%
python %~dp0main.py
pause
