# Kali Linux 工具数据库 (中文版)

KALI_TOOLS = {
    "信息收集 (Information Gathering)": [
        {"name": "Nmap", "cmd": "nmap", "desc": "网络探测工具和安全/端口扫描器，用于发现网络上的主机和服务。"},
        {"name": "Maltego", "cmd": "maltego", "desc": "开源情报(OSINT)和取证应用程序，用于展示数据之间的关系。"},
        {"name": "Recon-ng", "cmd": "recon-ng", "desc": "全功能的 Web 侦察框架，采用模块化设计。"},
        {"name": "Netdiscover", "cmd": "netdiscover", "desc": "主动/被动 ARP 侦察工具，用于发现无线网络中的主机。"},
        {"name": "Dmitry", "cmd": "dmitry", "desc": "Deepmagic 信息收集工具，用于主机信息搜索。"},
        {"name": "TheHarvester", "cmd": "theHarvester", "desc": "电子邮件、子域名和人员信息收集工具。"},
        {"name": "SpiderFoot", "cmd": "spiderfoot", "desc": "开源情报 (OSINT) 自动化工具，查询超过100个数据源。"},
        {"name": "Sherlock", "cmd": "sherlock", "desc": "通过用户名在社交网络上搜寻账户。"}
    ],
    "漏洞分析 (Vulnerability Analysis)": [
        {"name": "Nessus", "cmd": "nessus", "desc": "著名的漏洞扫描器 (通常需要单独安装)。"},
        {"name": "Nikto", "cmd": "nikto", "desc": "Web 服务器扫描器，测试多种危险文件和过时版本。"},
        {"name": "OpenVAS", "cmd": "openvas", "desc": "开放式漏洞评估扫描器，功能强大的安全管理工具。"},
        {"name": "Golismero", "cmd": "golismero", "desc": "Web 应用程序安全测试框架，自动整合其他工具的结果。"},
        {"name": "Lynis", "cmd": "lynis", "desc": "用于 Unix/Linux 系统的安全审计和加固工具。"}
    ],
    "Web 应用分析 (Web Application Analysis)": [
        {"name": "Burp Suite", "cmd": "burpsuite", "desc": "用于攻击 Web 应用程序的集成平台，包含拦截代理等。"},
        {"name": "OWASP ZAP", "cmd": "zaproxy", "desc": "OWASP Zed 攻击代理，易于使用的集成渗透测试工具。"},
        {"name": "SQLMap", "cmd": "sqlmap", "desc": "自动 SQL 注入和数据库接管工具。"},
        {"name": "WPScan", "cmd": "wpscan", "desc": "WordPress 安全扫描器，用于发现插件和主题漏洞。"},
        {"name": "Commix", "cmd": "commix", "desc": "自动化操作系统命令注入和利用工具。"},
        {"name": "Skipfish", "cmd": "skipfish", "desc": "高性能的主动 Web 应用程序安全侦察工具。"}
    ],
    "密码攻击 (Password Attacks)": [
        {"name": "John the Ripper", "cmd": "john", "desc": "快速的密码破解工具，支持多种哈希类型。"},
        {"name": "Hashcat", "cmd": "hashcat", "desc": "世界上最快的高级密码恢复工具，支持 GPU 加速。"},
        {"name": "Hydra", "cmd": "hydra", "desc": "支持多种协议的并行登录破解工具。"},
        {"name": "Medusa", "cmd": "medusa", "desc": "快速、并行、模块化的登录暴力破解工具。"},
        {"name": "Ophcrack", "cmd": "ophcrack", "desc": "基于彩虹表的 Windows 密码破解工具。"},
        {"name": "Wordlists", "cmd": "wordlists", "desc": "密码破解常用的字典文件集合。"}
    ],
    "无线攻击 (Wireless Attacks)": [
        {"name": "Aircrack-ng", "cmd": "aircrack-ng", "desc": "一套完整的 WiFi 安全评估工具 (802.11 WEP/WPA-PSK 破解)。"},
        {"name": "Kismet", "cmd": "kismet", "desc": "无线网络探测器、嗅探器和入侵检测系统。"},
        {"name": "Wifite", "cmd": "wifite", "desc": "自动化的无线攻击工具，支持 WEP/WPA/WPS。"},
        {"name": "Reaver", "cmd": "reaver", "desc": "针对 Wifi Protected Setup (WPS) 的暴力破解工具。"},
        {"name": "Fern Wifi Cracker", "cmd": "fern-wifi-cracker", "desc": "图形化的无线安全审计工具。"}
    ],
    "漏洞利用 (Exploitation Tools)": [
        {"name": "Metasploit Framework", "cmd": "msfconsole", "desc": "世界上最常用的渗透测试框架。"},
        {"name": "SearchSploit", "cmd": "searchsploit", "desc": "Exploit-DB 的命令行搜索工具。"},
        {"name": "Social Engineering Toolkit", "cmd": "setoolkit", "desc": "专为社会工程学设计的开源渗透测试框架。"},
        {"name": "Beef XSS", "cmd": "beef-xss", "desc": "浏览器利用框架，专注于客户端攻击。"},
        {"name": "Armitage", "cmd": "armitage", "desc": "Metasploit 的图形化网络攻击管理工具。"}
    ],
    "嗅探与欺骗 (Sniffing & Spoofing)": [
        {"name": "Wireshark", "cmd": "wireshark", "desc": "世界首屈一指的网络协议分析仪。"},
        {"name": "Bettercap", "cmd": "bettercap", "desc": "针对 WiFi、BLE 和以太网的“瑞士军刀”级中间人攻击工具。"},
        {"name": "Ettercap", "cmd": "ettercap", "desc": "综合性的中间人攻击套件。"},
        {"name": "Responder", "cmd": "responder", "desc": "LLMNR, NBT-NS 和 MDNS 投毒工具。"},
        {"name": "MacChanger", "cmd": "macchanger", "desc": "用于查看和修改网络接口 MAC 地址的工具。"}
    ],
    "后渗透 (Post Exploitation)": [
        {"name": "Mimikatz", "cmd": "mimikatz", "desc": "用于玩转 Windows 安全（如提取明文密码）的小工具。"},
        {"name": "Empire", "cmd": "empire", "desc": "基于 PowerShell 和 Python 的后渗透代理框架。"},
        {"name": "Powersploit", "cmd": "powersploit", "desc": "用于后渗透阶段的 PowerShell 脚本集合。"},
        {"name": "Weevely", "cmd": "weevely", "desc": "武器化的 Web Shell，用于隐蔽的后门维护。"}
    ],
    "取证工具 (Forensics)": [
        {"name": "Autopsy", "cmd": "autopsy", "desc": "易于使用的数字取证平台。"},
        {"name": "Binwalk", "cmd": "binwalk", "desc": "固件分析工具，用于提取文件系统代码。"},
        {"name": "Foremost", "cmd": "foremost", "desc": "基于文件头和内部结构的数据恢复程序。"},
        {"name": "Volatility", "cmd": "volatility", "desc": "高级内存取证框架。"}
    ],
    "报告工具 (Reporting Tools)": [
        {"name": "Faraday", "cmd": "faraday", "desc": "协作渗透测试和漏洞管理平台。"},
        {"name": "Pipal", "cmd": "pipal", "desc": "密码分析器，用于分析密码列表的统计信息。"}
    ]
}
