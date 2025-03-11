@echo off
chcp 65001 > nul
echo [启动] Mistral OCR 文档识别工具...

REM 尝试使用 poetry run
poetry run python -m src.main --gui 2>nul
if %errorlevel% equ 0 (
    exit /b 0
)

REM 如果 poetry 失败，尝试直接使用 python
echo [信息] Poetry 未安装或运行失败，尝试直接使用 Python...
python -m src.main --gui
if %errorlevel% neq 0 (
    echo [错误] 运行失败！请确保已安装 Python 并添加到系统环境变量中。
    echo [提示] 您也可以尝试手动运行：python -m src.main --gui
    pause
    exit /b 1
)

exit /b 0 