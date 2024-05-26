@echo off
REM 保存当前目录
set CURRENT_DIR=%cd%

REM 切换到上一级目录
cd ..

REM 激活虚拟环境
call winkbvenv\Scripts\activate

REM 返回到原始目录
cd %CURRENT_DIR%

REM 运行main.py
python main.py

REM 保持命令行窗口打开，以便查看输出结果
@REM pause
