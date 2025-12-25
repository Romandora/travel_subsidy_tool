@echo off
cd /d D:\travel_subsidy_tool

REM 安装依赖（首次运行）
python -m pip install -q -r requirements.txt

REM 运行 GUI 程序
python main_gui.py

pause