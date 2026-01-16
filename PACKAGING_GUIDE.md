# APP 打包指南 (Android APK)

由于你的电脑是 Windows 系统，且无法访问 Google Colab，这里提供两种可行的替代打包方案。

---

## 方案一：使用 GitHub Actions (推荐 - 最简单)

这种方法不需要你在本地安装任何复杂的环境，只要你能访问 GitHub 网站即可。所有的打包工作都在 GitHub 的云端服务器上完成。

### 步骤

1. **注册 GitHub 账号**: 如果没有，请去 [github.com](https://github.com/) 注册一个。
2. **创建仓库**: 在 GitHub 上创建一个新的空仓库 (Repository)。
3. **上传代码**: 将你电脑上的所有项目文件上传到这个仓库中。
   - 确保包含 `.github/workflows/build.yml` 这个文件夹和文件。
   - 确保包含 `mobile_app.py`, `data.py`, `buildozer.spec` 等文件。
4. **自动打包**:
   - 一旦你把代码上传（Push）上去，GitHub Actions 就会自动开始运行打包脚本。
   - 点击仓库页面顶部的 **"Actions"** 标签。
   - 你会看到一个正在运行的工作流（Build Android APK）。
5. **下载 APK**:
   - 等待几分钟（通常 10-15 分钟），直到状态变成绿色的对号。
   - 点击那个工作流任务，在页面底部的 **"Artifacts"** 区域，你会看到一个名为 `KaliMatrix-APK` 的压缩包。
   - 点击下载，解压后就是可以在手机上安装的 `.apk` 文件了。

---

## 方案二：使用 WSL (本地 Linux 子系统)

如果你完全无法访问 GitHub，或者坚持要在本地打包，你必须启用 Windows 的 Linux 子系统 (WSL)。

### 步骤

1. **启用 WSL**:
   - 右键点击 Windows 开始按钮 -> **Windows PowerShell (管理员)**。
   - 输入命令：`wsl --install`。
   - 安装完成后，**重启电脑**。
   - 重启后，系统会自动弹出一个 Ubuntu 的终端窗口，让你设置用户名和密码。

2. **在 WSL 中安装环境**:
   - 打开 Ubuntu 终端（在开始菜单搜索 Ubuntu）。
   - 依次复制并运行以下命令（这一步需要下载很多东西，请保持网络畅通）：

   ```bash
   # 更新软件源
   sudo apt update
   
   # 安装 Python 和系统依赖
   sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
   
   # 安装 Buildozer
   pip3 install --user --upgrade buildozer cython
   
   # 将 Buildozer 加入环境变量 (如果提示找不到命令)
   export PATH=$PATH:~/.local/bin
   ```

3. **开始打包**:
   - 在 Ubuntu 终端中，进入你的项目目录。
   - *提示：WSL 可以直接访问 Windows 文件。假设你的项目在桌面上：*
   ```bash
   cd /mnt/c/Users/阿航/Desktop/app
   ```
   - 运行打包命令：
   ```bash
   buildozer android debug
   ```
   - 第一次运行会下载 Android SDK，耗时较长。

4. **获取 APK**:
   - 打包成功后，APK 文件会生成在项目目录下的 `bin` 文件夹中。
   - 你可以直接在 Windows 的文件管理器中看到它。
