@echo off
cd /d D:\travel_subsidy_tool

python -m pip install -q pyinstaller ttkbootstrap

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

pyinstaller --onefile --windowed --name "差旅津贴计算器" --add-data "utils;utils" main_gui.py

echo.
echo ? 打包完成！
pause