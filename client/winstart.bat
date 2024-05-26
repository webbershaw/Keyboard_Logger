@echo off

set CURRENT_DIR=%cd%


cd ..


call winkbvenv\Scripts\activate


cd %CURRENT_DIR%


python main.py


pause
