# Kali Matrix Launcher

一个基于 Python 的“黑客帝国”风格 Kali Linux 工具启动器，支持桌面端和移动端。

## 目录
- [桌面版 (Windows/Linux)](#桌面版-windowslinux)
- [移动端 (Android)](#移动端-android)

---

## 桌面版 (Windows/Linux)

### 依赖
- Python 3.x
- Tkinter (通常随 Python 安装)
- WSL (Windows Subsystem for Linux) - 推荐用于执行实际命令

### 运行
```bash
python main.py
```
这启动基于 Tkinter 的桌面应用，包含数字雨特效、工具分类和 WSL 集成。

---

## 移动端 (Android)

本项目包含一个使用 **Kivy** 框架构建的移动端版本，专为触摸屏设计。

### 准备工作
在开发机上安装 Kivy:
```bash
pip install kivy
```

### 预览
在电脑上预览移动端界面：
```bash
python mobile_app.py
```
*注意：如遇中文乱码，请确保系统中有微软雅黑 (Windows) 或其他中文字体。*

### 打包 APK (Android)

要将应用打包安装到手机上，推荐使用 **Buildozer**。由于 Buildozer 仅支持 Linux/macOS，Windows 用户建议使用 **WSL** 或 **Google Colab**。

#### 步骤 1: 安装依赖 (在 Ubuntu/Debian/WSL 中)
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip3 install --user --upgrade buildozer
```

#### 步骤 2: 打包
在项目根目录（包含 `buildozer.spec` 的目录）运行：
```bash
# 这会下载 Android SDK/NDK 并编译，第一次运行可能需要较长时间
buildozer android debug
```

#### 步骤 3: 安装
编译完成后，APK 文件会在 `bin/` 目录下。
- 将 APK 发送到手机并安装。
- 或者通过 USB 连接手机后运行 `buildozer android deploy run`。

### 功能说明
- **界面**: 全中文，黑客帝国主题。
- **导航**: 支持分类浏览、工具详情查看。
- **操作**: 点击“复制命令”可将 Kali 工具命令复制到剪贴板，方便在 Termux 或 NetHunter 终端中粘贴运行。

---

## 文件结构
- `main.py`: 桌面版主程序 (Tkinter)
- `mobile_app.py`: 移动版主程序 (Kivy)
- `data.py`: 工具数据库 (中文版)
- `buildozer.spec`: Android 打包配置文件

## 常见问题 (Troubleshooting)

### 1. 依赖安装失败 (libgstreamer/libunwind 错误)
如果在安装依赖时遇到 `libgstreamer1.0-dev : depends: libunwind-dev` 或 `E: 无法纠正问题` 错误，请尝试以下命令修复：

```bash
sudo apt-get update
sudo apt-get --fix-broken install
sudo apt-get install aptitude
sudo aptitude install libgstreamer1.0-dev
```
当 `aptitude` 询问解决方案时，选择接受能够降级/修复依赖的方案（通常是第二个选项）。
