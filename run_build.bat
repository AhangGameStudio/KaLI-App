@echo off
chcp 65001 >nul
echo ==========================================
echo   Kali Matrix - 自动打包启动器 (Windows版)
echo ==========================================
echo.

echo [INFO] 正在检测 WSL 环境...
wsl --status >nul 2>&1
if %errorlevel% neq 0 goto ErrorWSL

echo [INFO] 正在修复脚本格式 (Windows - Linux)...
:: 去除 Windows 回车符，防止报错 $'\r': command not found
wsl sed -i 's/\r$//' build_apk.sh

echo [INFO] 正在赋予执行权限...
wsl chmod +x build_apk.sh

echo [INFO] 启动打包脚本...
echo ------------------------------------------
wsl ./build_apk.sh
echo ------------------------------------------
echo.
echo 执行结束。
pause
exit /b

:ErrorWSL
echo [ERROR] 未检测到 WSL (Windows Subsystem for Linux)
echo 请确保你已经安装了 Ubuntu 或其他 Linux 发行版
echo 如果你是通过虚拟机 (VirtualBox 或 VMware) 使用 Linux
echo 请直接在虚拟机终端中运行 ./build_apk.sh
pause
exit /b
