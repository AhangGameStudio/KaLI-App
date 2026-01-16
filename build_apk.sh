#!/bin/bash
set -e  # 遇到错误立即停止

echo "========================================"
echo "  Kali Matrix App - Android Packaging"
echo "========================================"

echo "[1/3] 更新系统并安装必要依赖..."
sudo apt update
# 安装 README 中列出的所有依赖
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

echo "[2/3] 安装/更新 Buildozer..."
pip3 install --user --upgrade buildozer

# 确保 ~/.local/bin 在 PATH 中
export PATH=$PATH:~/.local/bin

echo "[3/3] 开始构建 APK..."
echo "注意：如果是第一次运行，这可能需要较长时间下载 Android SDK/NDK。"
echo "如果提示接受许可协议 (License Agreement)，请输入 'y' 并回车。"

# 运行 buildozer
buildozer -v android debug

echo "========================================"
echo "打包完成！"
echo "APK 文件应位于 bin/ 目录下。"
