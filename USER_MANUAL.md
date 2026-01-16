# KaLI-App 用户使用文档

## 1. 简介

KaLI-App 是一款跨平台安全工具包，集成了多种安全相关功能，包括系统自检、网络安全监控、WIFI扫描与破解、漏洞挖掘等。本文档将详细介绍如何使用这些功能。

## 2. 安装指南

### 2.1 PC端安装

#### Windows系统
1. **下载安装包**：从官方网站下载最新版本的 KaLI-App 安装包
2. **运行安装程序**：双击安装包，按照提示完成安装
3. **安装依赖**：安装程序会自动安装必要的依赖库
4. **启动应用**：安装完成后，从开始菜单启动 KaLI-App

#### Linux系统
1. **下载源码**：从 GitHub 克隆或下载源码
   ```bash
   git clone https://github.com/AhangGameStudio/KaLI-App.git
   ```
2. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```
3. **启动应用**：
   ```bash
   python main.py
   ```

### 2.2 移动端安装

#### Android系统
1. **下载APK**：从官方网站下载最新版本的 APK 文件
2. **安装APK**：在设备上打开 APK 文件，按照提示完成安装
3. **授予权限**：首次启动时，按照提示授予必要的权限
4. **启动应用**：安装完成后，从应用列表启动 KaLI-App

## 3. 功能使用指南

### 3.1 PC端自检程序

#### 3.1.1 启动自检
1. 打开 KaLI-App
2. 在主界面点击 **SYSTEM SELF-CHECK** 标签页
3. 点击 **RUN SELF-CHECK** 按钮开始自检

#### 3.1.2 查看结果
自检完成后，您可以看到以下信息：
- **系统信息**：显示操作系统版本、架构等基本信息
- **硬件配置**：显示CPU、内存、存储等硬件信息
- **性能指标**：显示CPU、内存、磁盘等性能指标
- **检测到的问题**：显示系统中发现的潜在问题
- **进程信息**：显示系统中运行的进程信息
- **服务状态**：显示系统服务的运行状态

#### 3.1.3 生成报告
1. 点击 **GENERATE REPORT** 按钮
2. 系统会生成一个详细的自检报告文件
3. 报告文件保存在应用目录中，文件名格式为 `system_self_check_report_YYYYMMDD_HHMMSS.json`

### 3.2 网络安全程序

#### 3.2.1 启动监控
1. 打开 KaLI-App
2. 在主界面点击 **NETWORK SECURITY** 标签页
3. 点击 **START MONITORING** 按钮开始网络安全监控

#### 3.2.2 查看状态
监控过程中，您可以看到以下信息：
- **安全状态**：显示当前网络安全状态
- **网络统计**：显示网络流量、数据包等统计信息
- **最近数据包**：显示最近捕获的网络数据包
- **阻止的IP**：显示被系统阻止的可疑IP地址
- **安全日志**：显示安全事件日志
- **漏洞扫描结果**：显示系统和网络漏洞扫描结果

#### 3.2.3 扫描文件
1. 在 **FILE SCAN** 部分，输入要扫描的文件路径
2. 点击 **SCAN FILE** 按钮
3. 系统会扫描文件并显示扫描结果

#### 3.2.4 扫描漏洞
1. 点击 **SCAN SYSTEM** 按钮扫描系统漏洞
2. 点击 **SCAN NETWORK** 按钮扫描网络漏洞
3. 系统会显示扫描结果和详细的漏洞信息

### 3.3 移动端无线WIFI扫描与破解工具

#### 3.3.1 启动扫描
1. 打开 KaLI-App
2. 在主界面点击 **WIFI扫描与破解** 按钮
3. 点击 **刷新接口** 按钮刷新网络接口列表
4. 选择要使用的网络接口
5. 点击 **开始扫描** 按钮开始扫描周围的WIFI网络

#### 3.3.2 查看扫描结果
扫描完成后，您可以看到以下信息：
- **SSID**：网络名称
- **BSSID**：网络MAC地址
- **Signal**：信号强度
- **Channel**：信道
- **Encryption**：加密方式

#### 3.3.3 破解密码
1. 从扫描结果中选择要破解的网络
2. 点击 **尝试破解** 按钮
3. 系统会尝试使用各种方法破解网络密码
4. 破解完成后，系统会显示破解结果

### 3.4 移动端漏洞挖掘工具

#### 3.4.1 启动分析
1. 打开 KaLI-App
2. 在主界面点击 **漏洞挖掘工具** 按钮
3. 在 **应用路径** 输入框中输入要分析的应用路径
4. 点击 **开始分析** 按钮开始漏洞分析

#### 3.4.2 查看分析结果
分析完成后，您可以看到以下信息：
- **漏洞总数**：发现的漏洞总数
- **严重程度分布**：不同严重程度的漏洞数量
- **发现的漏洞**：详细的漏洞信息，包括：
  - 漏洞类型
  - 严重程度
  - 位置
  - 修复建议

#### 3.4.3 生成报告
1. 点击 **生成报告** 按钮
2. 系统会生成一个详细的漏洞分析报告文件
3. 报告文件保存在应用目录中，文件名格式为 `vulnerability_report_YYYYMMDD_HHMMSS.txt`

## 4. 高级功能

### 4.1 配置管理
1. 应用配置文件位于以下位置：
   - Windows: `%APPDATA%\KaLI-App\config\config.json`
   - Linux: `~/.config/KaLI-App/config.json`
   - macOS: `~/Library/Preferences/KaLI-App/config.json`
   - Android: `/data/data/com.ahang.KaLI-App/files/config.json`

2. 配置选项说明：
   - `app_name`: 应用名称
   - `version`: 应用版本
   - `debug`: 调试模式
   - `log_level`: 日志级别
   - `timeout`: 超时时间
   - `max_history`: 最大历史记录数
   - `wordlist_path`: 字典文件路径
   - `plugins`: 插件列表

### 4.2 插件系统
KaLI-App 支持插件系统，您可以通过以下方式管理插件：
1. 在配置文件中添加或移除插件
2. 插件文件应放置在 `plugins` 目录中

### 4.3 命令行使用
KaLI-App 也可以通过命令行使用：

#### 4.3.1 PC端命令行
```bash
# 运行系统自检
python main.py --self-check

# 运行网络安全监控
python main.py --security-monitor

# 扫描文件
python main.py --scan-file <file_path>

# 扫描漏洞
python main.py --scan-vulnerabilities
```

#### 4.3.2 移动端命令行（Termux）
```bash
# 运行系统自检
python mobile_app.py --self-check

# 运行网络安全监控
python mobile_app.py --security-monitor

# 扫描WIFI
python mobile_app.py --scan-wifi

# 扫描漏洞
python mobile_app.py --scan-vulnerabilities
```

## 5. 故障排除

### 5.1 常见问题

#### 5.1.1 PC端问题
| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 应用无法启动 | 依赖库缺失 | 重新安装依赖库 |
| 自检失败 | 权限不足 | 以管理员权限运行应用 |
| 网络监控失败 | 防火墙阻止 | 允许应用通过防火墙 |
| 扫描速度慢 | 系统资源不足 | 关闭其他占用资源的程序 |

#### 5.1.2 移动端问题
| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 应用崩溃 | 内存不足 | 关闭其他应用 |
| 权限错误 | 权限未授予 | 在设置中授予必要的权限 |
| 扫描失败 | 网络接口问题 | 检查网络接口状态 |
| 破解失败 | 加密方式复杂 | 尝试使用更强的字典文件 |

### 5.2 错误日志
应用的错误日志位于以下位置：
- Windows: `%APPDATA%\KaLI-App\logs\`
- Linux: `~/.cache/KaLI-App/logs/`
- macOS: `~/Library/Caches/KaLI-App/logs/`
- Android: `/data/data/com.ahang.KaLI-App/files/logs/`

### 5.3 联系支持
如果您遇到无法解决的问题，请通过以下方式联系支持：
- 电子邮件: support@kali-app.com
- GitHub Issues: https://github.com/AhangGameStudio/KaLI-App/issues
- 论坛: https://forum.kali-app.com

## 6. 安全注意事项

### 6.1 法律合规
- 使用 KaLI-App 时，请遵守当地法律法规
- 未经授权，不得使用 WIFI 破解功能破解他人的网络
- 漏洞扫描功能仅用于测试自己的系统和网络

### 6.2 隐私保护
- KaLI-App 不会收集或上传用户数据
- 所有数据处理均在本地进行
- 请妥善保管生成的报告文件，避免敏感信息泄露

### 6.3 安全建议
- 定期更新 KaLI-App 到最新版本
- 使用强密码保护应用
- 仅在安全的环境中使用 KaLI-App
- 定期备份重要数据

## 7. 更新与维护

### 7.1 检查更新
1. 打开 KaLI-App
2. 在主界面点击 **关于** 按钮
3. 点击 **检查更新** 按钮
4. 系统会检查是否有最新版本

### 7.2 手动更新
1. 从官方网站下载最新版本
2. 按照安装指南重新安装应用
3. 安装过程中，系统会保留您的配置文件

### 7.3 版本历史
| 版本 | 发布日期 | 主要变更 |
|------|----------|----------|
| 1.0.0 | 2026-01-16 | 初始版本，包含所有核心功能 |

## 8. 致谢

感谢以下项目和工具对 KaLI-App 的贡献：
- Python
- Kivy
- psutil
- scapy
- Wifite2
- aircrack-ng
- reaver
- nmap
- 以及所有开源安全工具

## 9. 许可证

KaLI-App 使用 MIT 许可证开源，详细信息请查看 LICENSE 文件。

---

**© 2026 AhangGameStudio. 保留所有权利。**
