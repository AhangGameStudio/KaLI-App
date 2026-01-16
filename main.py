import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import random
import threading
import time
from data import KALI_TOOLS
from core.network import network_security
from core.system import system_self_checker

# Matrix Theme Colors
COLOR_BG = "#000000"
COLOR_FG = "#00FF41"  # Matrix Green
COLOR_HL = "#008F11"  # Darker Green
COLOR_TXT = "#003B00" # Very Dark Green for backgrounds
FONT_MAIN = ("Consolas", 10)
FONT_HEADER = ("Consolas", 14, "bold")
FONT_TITLE = ("Consolas", 20, "bold")

class MatrixButton(tk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            bg=COLOR_BG, 
            fg=COLOR_FG, 
            activebackground=COLOR_HL, 
            activeforeground=COLOR_BG,
            bd=1,
            relief="solid",
            font=FONT_MAIN
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['bg'] = COLOR_HL
        self['fg'] = COLOR_BG

    def on_leave(self, e):
        self['bg'] = COLOR_BG
        self['fg'] = COLOR_FG

class MatrixKaliApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KALI LINUX MATRIX LAUNCHER")
        self.root.geometry("1100x700")
        self.root.configure(bg=COLOR_BG)
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", 
                        background=COLOR_BG, 
                        foreground=COLOR_FG, 
                        fieldbackground=COLOR_BG,
                        font=FONT_MAIN)
        style.configure("Treeview.Heading", 
                        background=COLOR_TXT, 
                        foreground=COLOR_FG, 
                        font=FONT_HEADER)
        style.map("Treeview", 
                  background=[('selected', COLOR_HL)], 
                  foreground=[('selected', COLOR_BG)])

        # Setup UI
        self.setup_header()
        self.setup_main_area()
        self.setup_footer()
        
        # Select first category by default
        self.cat_listbox.select_set(0)
        self.on_category_select(None)

    def setup_header(self):
        header_frame = tk.Frame(self.root, bg=COLOR_BG, bd=2, relief="solid")
        header_frame.pack(fill="x", padx=5, pady=5)
        
        title_label = tk.Label(header_frame, text="SYSTEM STATUS: ONLINE // USER: NEO", 
                               bg=COLOR_BG, fg=COLOR_FG, font=FONT_TITLE)
        title_label.pack(pady=10)
        
        self.matrix_canvas = tk.Canvas(header_frame, height=40, bg=COLOR_BG, highlightthickness=0)
        self.matrix_canvas.pack(fill="x")
        self.start_matrix_effect()

    def setup_main_area(self):
        main_frame = tk.Frame(self.root, bg=COLOR_BG)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Create Notebook for tabbed interface
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)

        # Tool Launcher Tab
        tool_tab = tk.Frame(self.notebook, bg=COLOR_BG)
        self.notebook.add(tool_tab, text="TOOL LAUNCHER")

        # Left: Categories
        left_frame = tk.Frame(tool_tab, bg=COLOR_BG, width=250)
        left_frame.pack(side="left", fill="y", padx=(0, 5))
        
        tk.Label(left_frame, text="[ CATEGORIES ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(fill="x", pady=5)
        
        self.cat_listbox = tk.Listbox(left_frame, bg=COLOR_BG, fg=COLOR_FG, 
                                      selectbackground=COLOR_HL, selectforeground=COLOR_BG,
                                      font=FONT_MAIN, bd=1, relief="solid")
        self.cat_listbox.pack(fill="both", expand=True)
        self.cat_listbox.bind("<<ListboxSelect>>", self.on_category_select)
        
        for cat in KALI_TOOLS.keys():
            self.cat_listbox.insert(tk.END, cat)

        # Middle: Tools List
        middle_frame = tk.Frame(tool_tab, bg=COLOR_BG)
        middle_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(middle_frame, text="[ TOOLS ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(fill="x", pady=5)
        
        columns = ("name", "cmd")
        self.tool_tree = ttk.Treeview(middle_frame, columns=columns, show="headings")
        self.tool_tree.heading("name", text="TOOL NAME")
        self.tool_tree.heading("cmd", text="COMMAND")
        self.tool_tree.column("name", width=150)
        self.tool_tree.column("cmd", width=100)
        self.tool_tree.pack(fill="both", expand=True)
        self.tool_tree.bind("<<TreeviewSelect>>", self.on_tool_select)

        # Right: Details & Action
        right_frame = tk.Frame(tool_tab, bg=COLOR_BG, width=350)
        right_frame.pack(side="right", fill="y", padx=(5, 0))
        
        tk.Label(right_frame, text="[ INTEL ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(fill="x", pady=5)
        
        self.desc_text = tk.Text(right_frame, bg=COLOR_BG, fg=COLOR_FG, font=FONT_MAIN, 
                                 height=10, width=30, wrap="word", bd=1, relief="solid")
        self.desc_text.pack(fill="x", pady=5)
        self.desc_text.insert("1.0", "Select a tool to analyze...")
        self.desc_text.config(state="disabled")
        
        # Execution Panel
        tk.Label(right_frame, text="[ EXECUTION ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(fill="x", pady=(20, 5))
        
        self.wsl_var = tk.BooleanVar(value=True)
        wsl_check = tk.Checkbutton(right_frame, text="USE WSL LAYER", variable=self.wsl_var, 
                                   bg=COLOR_BG, fg=COLOR_FG, selectcolor="black", activebackground=COLOR_BG, activeforeground=COLOR_FG, font=FONT_MAIN)
        wsl_check.pack(anchor="w")

        self.cmd_entry = tk.Entry(right_frame, bg=COLOR_BG, fg=COLOR_FG, insertbackground=COLOR_FG, font=FONT_MAIN, bd=1, relief="solid")
        self.cmd_entry.pack(fill="x", pady=10)
        
        self.run_btn = MatrixButton(right_frame, text="INITIATE SEQUENCE", command=self.run_tool)
        self.run_btn.pack(fill="x", pady=5)
        
        # Enhanced Output Panel
        tk.Label(right_frame, text="[ SYSTEM OUTPUT ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(fill="x", pady=(10, 5))
        
        self.output_text = tk.Text(right_frame, bg=COLOR_BG, fg=COLOR_FG, font=FONT_MAIN,
                                   height=15, width=30, bd=2, relief="ridge", highlightbackground=COLOR_HL, highlightthickness=2)
        self.output_text.pack(fill="both", expand=True, pady=5)
        self.output_text.insert("1.0", "SYSTEM READY. SELECT A TOOL AND INITIATE SEQUENCE.\n\n")

        # Network Security Tab
        security_tab = tk.Frame(self.notebook, bg=COLOR_BG)
        self.notebook.add(security_tab, text="NETWORK SECURITY")
        
        # Security Tab Content
        self.setup_security_tab(security_tab)
        
        # System Self-Check Tab
        self_check_tab = tk.Frame(self.notebook, bg=COLOR_BG)
        self.notebook.add(self_check_tab, text="SYSTEM SELF-CHECK")
        
        # System Self-Check Tab Content
        self.setup_self_check_tab(self_check_tab)


    def setup_footer(self):
        footer = tk.Label(self.root, text="CONNECTED TO MAINFRAME // SECURE CONNECTION", 
                          bg=COLOR_BG, fg=COLOR_HL, font=("Consolas", 8))
        footer.pack(side="bottom", fill="x")

    def setup_security_tab(self, parent):
        """设置网络安全标签页"""
        # Main security frame
        security_frame = tk.Frame(parent, bg=COLOR_BG)
        security_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Top: Status and Controls
        status_frame = tk.Frame(security_frame, bg=COLOR_BG, bd=2, relief="solid")
        status_frame.pack(fill="x", pady=5)
        
        # Status section
        status_left = tk.Frame(status_frame, bg=COLOR_BG)
        status_left.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        
        tk.Label(status_left, text="[ SECURITY STATUS ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(anchor="w")
        self.security_status_var = tk.StringVar(value="INITIALIZING")
        status_label = tk.Label(status_left, textvariable=self.security_status_var, bg=COLOR_BG, fg=COLOR_FG, font=FONT_MAIN)
        status_label.pack(anchor="w", pady=5)
        
        # Control section
        status_right = tk.Frame(status_frame, bg=COLOR_BG)
        status_right.pack(side="right", padx=10, pady=10)
        
        self.start_security_btn = MatrixButton(status_right, text="START MONITORING", command=self.start_security_monitoring)
        self.start_security_btn.pack(side="left", padx=5)
        
        self.stop_security_btn = MatrixButton(status_right, text="STOP MONITORING", command=self.stop_security_monitoring, state="disabled")
        self.stop_security_btn.pack(side="left", padx=5)
        
        # Vulnerability Scan Buttons
        self.scan_system_btn = MatrixButton(status_right, text="SCAN SYSTEM", command=self.scan_system_vulnerabilities)
        self.scan_system_btn.pack(side="left", padx=5)
        
        self.scan_network_btn = MatrixButton(status_right, text="SCAN NETWORK", command=self.scan_network_vulnerabilities)
        self.scan_network_btn.pack(side="left", padx=5)
        
        # Middle: Statistics and Info
        stats_frame = tk.Frame(security_frame, bg=COLOR_BG)
        stats_frame.pack(fill="both", expand=True, pady=5)
        
        # Left: Network Statistics
        stats_left = tk.Frame(stats_frame, bg=COLOR_BG, width=300, bd=2, relief="solid")
        stats_left.pack(side="left", fill="y", padx=(0, 5))
        
        tk.Label(stats_left, text="[ NETWORK STATISTICS ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(fill="x", pady=5)
        
        self.stats_text = tk.Text(stats_left, bg=COLOR_BG, fg=COLOR_FG, font=FONT_MAIN, height=15, bd=1, relief="solid")
        self.stats_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.stats_text.insert("1.0", "NETWORK STATISTICS WILL APPEAR HERE\n\n")
        self.stats_text.config(state="disabled")
        
        # Middle: Recent Packets
        stats_middle = tk.Frame(stats_frame, bg=COLOR_BG, bd=2, relief="solid")
        stats_middle.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(stats_middle, text="[ RECENT PACKETS ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(fill="x", pady=5)
        
        self.packets_text = tk.Text(stats_middle, bg=COLOR_BG, fg=COLOR_FG, font=FONT_MAIN, bd=1, relief="solid")
        self.packets_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.packets_text.insert("1.0", "RECENT PACKETS WILL APPEAR HERE\n\n")
        self.packets_text.config(state="disabled")
        
        # Right: Security Info
        stats_right = tk.Frame(stats_frame, bg=COLOR_BG, width=300, bd=2, relief="solid")
        stats_right.pack(side="right", fill="y", padx=(5, 0))
        
        # Blocked IPs
        tk.Label(stats_right, text="[ BLOCKED IPS ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(fill="x", pady=5)
        
        self.blocked_ips_text = tk.Text(stats_right, bg=COLOR_BG, fg=COLOR_FG, font=FONT_MAIN, height=10, bd=1, relief="solid")
        self.blocked_ips_text.pack(fill="x", padx=5, pady=5)
        self.blocked_ips_text.insert("1.0", "BLOCKED IPS WILL APPEAR HERE\n\n")
        self.blocked_ips_text.config(state="disabled")
        
        # File Scan Section
        tk.Label(stats_right, text="[ FILE SCAN ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(fill="x", pady=5)
        
        scan_frame = tk.Frame(stats_right, bg=COLOR_BG)
        scan_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Label(scan_frame, text="File Path:", bg=COLOR_BG, fg=COLOR_FG, font=FONT_MAIN).pack(anchor="w")
        self.scan_path_entry = tk.Entry(scan_frame, bg=COLOR_BG, fg=COLOR_FG, insertbackground=COLOR_FG, font=FONT_MAIN, bd=1, relief="solid")
        self.scan_path_entry.pack(fill="x", pady=5)
        
        self.scan_btn = MatrixButton(scan_frame, text="SCAN FILE", command=self.scan_file)
        self.scan_btn.pack(fill="x", pady=5)
        
        # Bottom: Log and Vulnerability Info
        bottom_frame = tk.Frame(security_frame, bg=COLOR_BG)
        bottom_frame.pack(fill="x", pady=5)
        
        # Left: Security Log
        log_frame = tk.Frame(bottom_frame, bg=COLOR_BG, bd=2, relief="solid", width=600)
        log_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        tk.Label(log_frame, text="[ SECURITY LOG ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(anchor="w", padx=10, pady=5)
        
        self.security_log = tk.Text(log_frame, bg=COLOR_BG, fg=COLOR_FG, font=FONT_MAIN, height=10, bd=1, relief="solid")
        self.security_log.pack(fill="both", expand=True, padx=10, pady=5)
        self.security_log.insert("1.0", "SECURITY LOG WILL APPEAR HERE\n\n")
        
        # Right: Vulnerability Scan Results
        vuln_frame = tk.Frame(bottom_frame, bg=COLOR_BG, bd=2, relief="solid", width=400)
        vuln_frame.pack(side="right", fill="y", padx=(5, 0))
        
        tk.Label(vuln_frame, text="[ VULNERABILITY SCAN RESULTS ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(fill="x", pady=5)
        
        self.vuln_text = tk.Text(vuln_frame, bg=COLOR_BG, fg=COLOR_FG, font=FONT_MAIN, height=10, bd=1, relief="solid")
        self.vuln_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.vuln_text.insert("1.0", "VULNERABILITY SCAN RESULTS WILL APPEAR HERE\n\n")
        
        # Initialize security module
        network_security.initialize()
        self.log_security_message("Network security module initialized")
        self.update_security_status()

    def start_security_monitoring(self):
        """开始安全监控"""
        try:
            network_security.start_monitoring()
            self.log_security_message("Starting network security monitoring...")
            self.security_status_var.set("MONITORING")
            self.start_security_btn.config(state="disabled")
            self.stop_security_btn.config(state="normal")
            
            # Start status update thread
            self.security_update_thread = threading.Thread(target=self.security_update_loop, daemon=True)
            self.security_update_thread.start()
            
        except Exception as e:
            self.log_security_message(f"Error starting monitoring: {str(e)}")

    def stop_security_monitoring(self):
        """停止安全监控"""
        try:
            network_security.stop_monitoring()
            self.log_security_message("Stopping network security monitoring...")
            self.security_status_var.set("STOPPED")
            self.start_security_btn.config(state="normal")
            self.stop_security_btn.config(state="disabled")
        except Exception as e:
            self.log_security_message(f"Error stopping monitoring: {str(e)}")

    def security_update_loop(self):
        """安全状态更新循环"""
        while network_security.traffic_monitor.is_monitoring:
            self.update_security_status()
            time.sleep(2)

    def update_security_status(self):
        """更新安全状态"""
        try:
            # Get security status
            status = network_security.get_security_status()
            
            # Update status label
            status_text = status['status'].upper()
            self.security_status_var.set(f"STATUS: {status_text}")
            
            # Update network statistics
            stats = status['network']
            stats_text = f"Packet Count: {stats['packet_count']}\n"
            stats_text += f"Flow Count: {stats['flow_count']}\n"
            stats_text += f"Active Flows: {stats['active_flows']}\n\n"
            
            # Update top flows
            top_flows = network_security.get_top_flows(5)
            stats_text += "Top 5 Flows:\n"
            for flow, data in top_flows:
                stats_text += f"{flow}: {data['bytes']} bytes\n"
            
            self.stats_text.config(state="normal")
            self.stats_text.delete("1.0", tk.END)
            self.stats_text.insert("1.0", stats_text)
            self.stats_text.config(state="disabled")
            
            # Update recent packets
            recent_packets = network_security.get_recent_packets(10)
            packets_text = ""
            for packet in recent_packets:
                packets_text += f"{packet.get('timestamp', 'N/A')} - {packet.get('src', 'N/A')} -> {packet.get('dst', 'N/A')} ({packet.get('protocol', 'N/A')})\n"
            
            if packets_text:
                self.packets_text.config(state="normal")
                self.packets_text.delete("1.0", tk.END)
                self.packets_text.insert("1.0", packets_text)
                self.packets_text.config(state="disabled")
            
            # Update blocked IPs
            blocked_ips = network_security.get_blocked_ips()
            blocked_text = "\n".join(blocked_ips) if blocked_ips else "No blocked IPs"
            
            self.blocked_ips_text.config(state="normal")
            self.blocked_ips_text.delete("1.0", tk.END)
            self.blocked_ips_text.insert("1.0", blocked_text)
            self.blocked_ips_text.config(state="disabled")
            
        except Exception as e:
            self.log_security_message(f"Error updating status: {str(e)}")

    def scan_file(self):
        """扫描文件"""
        file_path = self.scan_path_entry.get()
        if not file_path:
            self.log_security_message("Please enter a file path")
            return
        
        try:
            self.log_security_message(f"Scanning file: {file_path}")
            result = network_security.scan_file(file_path)
            
            if result.get('detection'):
                detection = result['detection']
                self.log_security_message(f"MALWARE DETECTED: {detection['name']} ({detection['type']})")
            else:
                self.log_security_message("File scanned - No malware detected")
                
        except Exception as e:
            self.log_security_message(f"Error scanning file: {str(e)}")

    def log_security_message(self, message):
        """记录安全消息"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.security_log.insert(tk.END, log_message)
        self.security_log.see(tk.END)
    
    def scan_system_vulnerabilities(self):
        """扫描系统漏洞"""
        def execute_scan():
            try:
                self.log_security_message("Starting system vulnerability scan...")
                self.vuln_text.delete("1.0", tk.END)
                self.vuln_text.insert("1.0", "Scanning system for vulnerabilities...\n\n")
                
                # 执行系统漏洞扫描
                results = network_security.scan_system_vulnerabilities()
                
                # 生成报告
                report = network_security.generate_vulnerability_report(results)
                
                # 显示结果
                self.vuln_text.delete("1.0", tk.END)
                self.vuln_text.insert("1.0", report)
                
                self.log_security_message(f"System vulnerability scan completed. Found {results['summary']['total']} issues.")
                
            except Exception as e:
                self.log_security_message(f"Error scanning system vulnerabilities: {str(e)}")
                self.vuln_text.insert(tk.END, f"Error: {str(e)}\n\n")
        
        threading.Thread(target=execute_scan, daemon=True).start()
    
    def scan_network_vulnerabilities(self):
        """扫描网络漏洞"""
        def execute_scan():
            try:
                self.log_security_message("Starting network vulnerability scan...")
                self.vuln_text.delete("1.0", tk.END)
                self.vuln_text.insert("1.0", "Scanning network for vulnerabilities...\n\n")
                
                # 执行网络漏洞扫描
                results = network_security.scan_network_vulnerabilities()
                
                # 生成报告
                report = network_security.generate_vulnerability_report(results)
                
                # 显示结果
                self.vuln_text.delete("1.0", tk.END)
                self.vuln_text.insert("1.0", report)
                
                self.log_security_message(f"Network vulnerability scan completed. Found {results['summary']['total']} issues.")
                
            except Exception as e:
                self.log_security_message(f"Error scanning network vulnerabilities: {str(e)}")
                self.vuln_text.insert(tk.END, f"Error: {str(e)}\n\n")
        
        threading.Thread(target=execute_scan, daemon=True).start()


    def start_matrix_effect(self):
        width = 1000
        self.drops = [random.randint(-100, 0) for _ in range(int(width/10))]
        self.update_matrix()

    def update_matrix(self):
        self.matrix_canvas.delete("all")
        for i, y in enumerate(self.drops):
            char = random.choice("0123456789ABCDEF")
            x = i * 10
            # Draw trail
            for j in range(5):
                color = "#005500" if j < 4 else "#00FF41"
                self.matrix_canvas.create_text(x, y - (j*10), text=char, fill=color, font=("Courier", 8))
            
            self.drops[i] += 10
            if self.drops[i] > 50:
                self.drops[i] = random.randint(-50, 0)
        
        self.root.after(100, self.update_matrix)

    def on_category_select(self, event):
        selection = self.cat_listbox.curselection()
        if not selection:
            return
        
        cat = self.cat_listbox.get(selection[0])
        
        # Clear tree
        for item in self.tool_tree.get_children():
            self.tool_tree.delete(item)
            
        # Populate tree
        for tool in KALI_TOOLS.get(cat, []):
            self.tool_tree.insert("", "end", values=(tool["name"], tool["cmd"]))

    def on_tool_select(self, event):
        selection = self.tool_tree.selection()
        if not selection:
            return
            
        item = self.tool_tree.item(selection[0])
        tool_name = item['values'][0]
        tool_cmd = item['values'][1]
        
        # Find description
        desc = ""
        for cat in KALI_TOOLS.values():
            for t in cat:
                if t["name"] == tool_name:
                    desc = t["desc"]
                    break
        
        self.desc_text.config(state="normal")
        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert("1.0", f"TARGET: {tool_name}\n\nPROTOCOL: {tool_cmd}\n\nDATA: {desc}")
        
        # Add special note for Wifite
        if tool_name == "Wifite":
            self.desc_text.insert(tk.END, "\n\n{NOTICE} Wifite requires:")
            self.desc_text.insert(tk.END, "\n- Linux environment (WSL recommended)")
            self.desc_text.insert(tk.END, "\n- Root/sudo privileges")
            self.desc_text.insert(tk.END, "\n- Wireless network adapter in monitor mode")
            self.desc_text.insert(tk.END, "\n- Dependencies: aircrack-ng, reaver, etc.")
        
        self.desc_text.config(state="disabled")
        
        self.cmd_entry.delete(0, tk.END)
        self.cmd_entry.insert(0, f"{tool_cmd} --help")

    def run_tool(self):
        cmd = self.cmd_entry.get()
        if not cmd:
            return
            
        use_wsl = self.wsl_var.get()
        
        # Check if running on Windows and adjust command
        is_windows = os.name == 'nt'
        if is_windows and 'sudo' in cmd:
            # Remove sudo on Windows
            cmd = cmd.replace('sudo ', '')
            self.log_output(f"> ADJUSTING COMMAND FOR WINDOWS: {cmd}")
        
        self.log_output(f"> INITIALIZING {cmd}...")
        
        def execute():
            try:
                if use_wsl and is_windows:
                    # Check if WSL is available
                    self.log_output("> CHECKING WSL STATUS...")
                    
                    # Use binary mode to avoid encoding issues
                    wsl_check = subprocess.run('wsl --status', shell=True, capture_output=True)
                    
                    if wsl_check.returncode != 0:
                        self.log_output("> WSL NOT AVAILABLE")
                        self.log_output("> TO INSTALL WSL, RUN: wsl --install")
                        self.log_output("> THEN RESTART YOUR COMPUTER")
                        self.log_output("> SEQUENCE COMPLETE.")
                        return
                    
                    # Check if WSL distribution is installed
                    wsl_list = subprocess.run('wsl --list', shell=True, capture_output=True)
                    
                    # Convert to string with safe decoding
                    wsl_list_output = ''
                    try:
                        if wsl_list.stdout:
                            wsl_list_output = wsl_list.stdout.decode('utf-8', errors='ignore')
                    except:
                        pass
                    
                    # Check if any distribution is found
                    has_distribution = False
                    if wsl_list_output:
                        if "Ubuntu" in wsl_list_output or " kali" in wsl_list_output.lower():
                            has_distribution = True
                    else:
                        # If we can't decode, assume WSL is available
                        has_distribution = True
                    
                    if not has_distribution:
                        self.log_output("> NO WSL DISTRIBUTION FOUND")
                        self.log_output("> RUN: wsl --install Ubuntu")
                        self.log_output("> OR: wsl --install kali-linux")
                        self.log_output("> SEQUENCE COMPLETE.")
                        return
                    
                    # WSL is available, proceed
                    final_cmd = f"wsl {cmd}"
                    self.log_output(f"> EXECUTING VIA WSL: {final_cmd}")
                else:
                    final_cmd = cmd
                
                # Use binary mode for better control
                process = subprocess.Popen(final_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                stdout, _ = process.communicate()
                
                if stdout:
                    # Convert to string with strict filtering
                    # Only keep ASCII printable characters
                    filtered_output = []
                    for byte in stdout:
                        if 32 <= byte <= 126 or byte in (10, 13, 9):  # Printable ASCII + newlines + tab
                            filtered_output.append(chr(byte))
                    
                    filtered_str = ''.join(filtered_output)
                    
                    if filtered_str.strip():
                        # Split into lines and clean
                        lines = filtered_str.split('\n')
                        cleaned_lines = [line.strip() for line in lines if line.strip()]
                        
                        if cleaned_lines:
                            for line in cleaned_lines:
                                if line:  # Only non-empty lines
                                    self.log_output(line)
                        else:
                            self.log_output("> NO VALID OUTPUT")
                    else:
                        self.log_output("> NO PRINTABLE OUTPUT")
                else:
                    self.log_output("> NO OUTPUT")
                
                self.log_output(f"> COMMAND EXITED WITH CODE: {process.returncode}")
                
                if process.returncode != 0:
                    if use_wsl and is_windows:
                        self.log_output("> WSL COMMAND FAILED")
                        self.log_output("> CHECK IF WSL IS RUNNING PROPERLY")
                        self.log_output("> TRY: wsl --shutdown")
                        self.log_output("> THEN: wsl")
                
                self.log_output("> SEQUENCE COMPLETE.")
                
            except Exception as e:
                self.log_output(f"> SYSTEM FAILURE: {str(e)}")
                import traceback
                self.log_output(f"> DEBUG INFO: {traceback.format_exc()}")

        threading.Thread(target=execute, daemon=True).start()

    def setup_self_check_tab(self, parent):
        """设置系统自检标签页"""
        # Main self-check frame
        self_check_frame = tk.Frame(parent, bg=COLOR_BG)
        self_check_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Top: Status and Controls
        status_frame = tk.Frame(self_check_frame, bg=COLOR_BG, bd=2, relief="solid")
        status_frame.pack(fill="x", pady=5)
        
        # Status section
        status_left = tk.Frame(status_frame, bg=COLOR_BG)
        status_left.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        
        tk.Label(status_left, text="[ SYSTEM STATUS ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(anchor="w")
        self.self_check_status_var = tk.StringVar(value="READY")
        status_label = tk.Label(status_left, textvariable=self.self_check_status_var, bg=COLOR_BG, fg=COLOR_FG, font=FONT_MAIN)
        status_label.pack(anchor="w", pady=5)
        
        # Control section
        status_right = tk.Frame(status_frame, bg=COLOR_BG)
        status_right.pack(side="right", padx=10, pady=10)
        
        self.run_self_check_btn = MatrixButton(status_right, text="RUN SELF-CHECK", command=self.run_self_check)
        self.run_self_check_btn.pack(side="left", padx=5)
        
        self.generate_report_btn = MatrixButton(status_right, text="GENERATE REPORT", command=self.generate_self_check_report)
        self.generate_report_btn.pack(side="left", padx=5)
        
        # Middle: System Information
        info_frame = tk.Frame(self_check_frame, bg=COLOR_BG)
        info_frame.pack(fill="both", expand=True, pady=5)
        
        # Left: Basic System Info
        info_left = tk.Frame(info_frame, bg=COLOR_BG, width=300, bd=2, relief="solid")
        info_left.pack(side="left", fill="y", padx=(0, 5))
        
        tk.Label(info_left, text="[ SYSTEM INFO ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(fill="x", pady=5)
        
        self.system_info_text = tk.Text(info_left, bg=COLOR_BG, fg=COLOR_FG, font=FONT_MAIN, height=15, bd=1, relief="solid")
        self.system_info_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.system_info_text.insert("1.0", "SYSTEM INFORMATION WILL APPEAR HERE\n\n")
        self.system_info_text.config(state="disabled")
        
        # Middle: Hardware Info
        info_middle = tk.Frame(info_frame, bg=COLOR_BG, bd=2, relief="solid")
        info_middle.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(info_middle, text="[ HARDWARE CONFIGURATION ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(fill="x", pady=5)
        
        self.hardware_info_text = tk.Text(info_middle, bg=COLOR_BG, fg=COLOR_FG, font=FONT_MAIN, bd=1, relief="solid")
        self.hardware_info_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.hardware_info_text.insert("1.0", "HARDWARE INFORMATION WILL APPEAR HERE\n\n")
        self.hardware_info_text.config(state="disabled")
        
        # Right: Performance & Issues
        info_right = tk.Frame(info_frame, bg=COLOR_BG, width=300, bd=2, relief="solid")
        info_right.pack(side="right", fill="y", padx=(5, 0))
        
        # Performance Metrics
        tk.Label(info_right, text="[ PERFORMANCE METRICS ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(fill="x", pady=5)
        
        self.performance_text = tk.Text(info_right, bg=COLOR_BG, fg=COLOR_FG, font=FONT_MAIN, height=10, bd=1, relief="solid")
        self.performance_text.pack(fill="x", padx=5, pady=5)
        self.performance_text.insert("1.0", "PERFORMANCE DATA WILL APPEAR HERE\n\n")
        self.performance_text.config(state="disabled")
        
        # Issues
        tk.Label(info_right, text="[ DETECTED ISSUES ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(fill="x", pady=5)
        
        self.issues_text = tk.Text(info_right, bg=COLOR_BG, fg=COLOR_FG, font=FONT_MAIN, height=10, bd=1, relief="solid")
        self.issues_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.issues_text.insert("1.0", "ISSUES WILL APPEAR HERE\n\n")
        self.issues_text.config(state="disabled")
        
        # Bottom: Detailed Info
        detail_frame = tk.Frame(self_check_frame, bg=COLOR_BG, bd=2, relief="solid")
        detail_frame.pack(fill="x", pady=5)
        
        # Create notebook for detailed tabs
        detail_notebook = ttk.Notebook(detail_frame)
        detail_notebook.pack(fill="both", expand=True)
        
        # Processes Tab
        processes_tab = tk.Frame(detail_notebook, bg=COLOR_BG)
        detail_notebook.add(processes_tab, text="PROCESSES")
        
        self.processes_text = tk.Text(processes_tab, bg=COLOR_BG, fg=COLOR_FG, font=FONT_MAIN, bd=1, relief="solid")
        self.processes_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.processes_text.insert("1.0", "PROCESS INFORMATION WILL APPEAR HERE\n\n")
        self.processes_text.config(state="disabled")
        
        # Services Tab
        services_tab = tk.Frame(detail_notebook, bg=COLOR_BG)
        detail_notebook.add(services_tab, text="SERVICES")
        
        self.services_text = tk.Text(services_tab, bg=COLOR_BG, fg=COLOR_FG, font=FONT_MAIN, bd=1, relief="solid")
        self.services_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.services_text.insert("1.0", "SERVICE INFORMATION WILL APPEAR HERE\n\n")
        self.services_text.config(state="disabled")
        
        # Initialize with basic system info
        self.update_system_info()
    
    def update_system_info(self):
        """更新系统信息"""
        try:
            # Get basic system info
            system_info = system_self_checker.get_system_info()
            info_text = f"SYSTEM: {system_info['system']} {system_info['release']}\n"
            info_text += f"VERSION: {system_info['version']}\n"
            info_text += f"ARCHITECTURE: {system_info['architecture'][0]}\n"
            info_text += f"MACHINE: {system_info['machine']}\n"
            info_text += f"NODE: {system_info['node']}\n"
            
            self.system_info_text.config(state="normal")
            self.system_info_text.delete("1.0", tk.END)
            self.system_info_text.insert("1.0", info_text)
            self.system_info_text.config(state="disabled")
        except Exception as e:
            self.log_self_check_message(f"Error updating system info: {str(e)}")
    
    def run_self_check(self):
        """运行系统自检"""
        def execute_self_check():
            try:
                self.self_check_status_var.set("SCANNING")
                self.log_self_check_message("Starting system self-check...")
                
                # Generate full report
                report = system_self_checker.generate_report()
                
                # Update hardware info
                hardware = report['hardware_info']
                hardware_text = f"CPU: {hardware['cpu']['processor']}\n"
                hardware_text += f"CPU CORES: {hardware['cpu']['cpu_count_physical']} physical, {hardware['cpu']['cpu_count']} logical\n"
                hardware_text += f"CPU FREQUENCY: {hardware['cpu']['cpu_freq'].get('current', 'N/A')} MHz\n\n"
                
                hardware_text += f"MEMORY: {hardware['memory']['total'] / (1024**3):.2f} GB total\n"
                hardware_text += f"MEMORY AVAILABLE: {hardware['memory']['available'] / (1024**3):.2f} GB\n\n"
                
                hardware_text += f"STORAGE:\n"
                for storage in hardware['storage']:
                    try:
                        total_gb = storage['total'] / (1024**3)
                        used_gb = storage['used'] / (1024**3)
                        percent = storage['percent']
                        hardware_text += f"  {storage['mountpoint']}: {used_gb:.2f} GB / {total_gb:.2f} GB ({percent}%)\n"
                    except Exception:
                        pass
                
                self.hardware_info_text.config(state="normal")
                self.hardware_info_text.delete("1.0", tk.END)
                self.hardware_info_text.insert("1.0", hardware_text)
                self.hardware_info_text.config(state="disabled")
                
                # Update performance metrics
                performance = report['performance_metrics']
                performance_text = f"CPU USAGE: {report['hardware_info']['cpu']['cpu_percent']}%\n"
                performance_text += f"MEMORY USAGE: {report['hardware_info']['memory']['percent']}%\n\n"
                
                performance_text += f"DISK I/O:\n"
                if 'io_counters' in performance['disk']:
                    disk_io = performance['disk']['io_counters']
                    performance_text += f"  Read: {disk_io.read_bytes / (1024**2):.2f} MB\n"
                    performance_text += f"  Write: {disk_io.write_bytes / (1024**2):.2f} MB\n\n"
                
                performance_text += f"NETWORK I/O:\n"
                if 'io_counters' in performance['network']:
                    net_io = performance['network']['io_counters']
                    performance_text += f"  Sent: {net_io.bytes_sent / (1024**2):.2f} MB\n"
                    performance_text += f"  Received: {net_io.bytes_recv / (1024**2):.2f} MB\n"
                
                self.performance_text.config(state="normal")
                self.performance_text.delete("1.0", tk.END)
                self.performance_text.insert("1.0", performance_text)
                self.performance_text.config(state="disabled")
                
                # Update issues
                issues = report['issues']
                issues_text = ""
                if issues['critical']:
                    issues_text += "CRITICAL ISSUES:\n"
                    for issue in issues['critical']:
                        issues_text += f"  - {issue}\n"
                    issues_text += "\n"
                
                if issues['warning']:
                    issues_text += "WARNINGS:\n"
                    for issue in issues['warning']:
                        issues_text += f"  - {issue}\n"
                    issues_text += "\n"
                
                if issues['info']:
                    issues_text += "INFORMATION:\n"
                    for issue in issues['info']:
                        issues_text += f"  - {issue}\n"
                
                if not issues_text:
                    issues_text = "NO ISSUES DETECTED. SYSTEM IS HEALTHY.\n"
                
                self.issues_text.config(state="normal")
                self.issues_text.delete("1.0", tk.END)
                self.issues_text.insert("1.0", issues_text)
                self.issues_text.config(state="disabled")
                
                # Update processes
                processes = report['top_processes']
                processes_text = "TOP 20 PROCESSES BY CPU USAGE:\n\n"
                processes_text += f"{'PID':<8} {'NAME':<30} {'USER':<20} {'CPU%':<8} {'MEM%':<8} {'STATUS':<10}\n"
                processes_text += "-" * 100 + "\n"
                
                for proc in processes:
                    pid = proc.get('pid', 'N/A')
                    name = proc.get('name', 'N/A')[:30]
                    username = proc.get('username', 'N/A')[:20]
                    cpu_percent = proc.get('cpu_percent', 'N/A')
                    memory_percent = proc.get('memory_percent', 'N/A')
                    status = proc.get('status', 'N/A')[:10]
                    
                    processes_text += f"{pid:<8} {name:<30} {username:<20} {cpu_percent:<8} {memory_percent:<8} {status:<10}\n"
                
                self.processes_text.config(state="normal")
                self.processes_text.delete("1.0", tk.END)
                self.processes_text.insert("1.0", processes_text)
                self.processes_text.config(state="disabled")
                
                # Update services
                services = report['services']
                services_text = "SERVICES STATUS:\n\n"
                services_text += f"{'NAME':<40} {'STATUS':<20}\n"
                services_text += "-" * 60 + "\n"
                
                for service in services[:50]:  # Limit to 50 services
                    if isinstance(service, dict):
                        name = service.get('name', 'N/A')[:40]
                        status = service.get('status', 'N/A')[:20]
                        services_text += f"{name:<40} {status:<20}\n"
                
                self.services_text.config(state="normal")
                self.services_text.delete("1.0", tk.END)
                self.services_text.insert("1.0", services_text)
                self.services_text.config(state="disabled")
                
                self.self_check_status_var.set("COMPLETED")
                self.log_self_check_message("System self-check completed successfully")
                
            except Exception as e:
                self.self_check_status_var.set("ERROR")
                self.log_self_check_message(f"Error during self-check: {str(e)}")
                import traceback
                self.log_self_check_message(f"Debug info: {traceback.format_exc()}")
        
        threading.Thread(target=execute_self_check, daemon=True).start()
    
    def generate_self_check_report(self):
        """生成自检报告"""
        try:
            import json
            import datetime
            
            report = system_self_checker.generate_report()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = f"system_self_check_report_{timestamp}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            self.log_self_check_message(f"Report generated: {report_file}")
            messagebox.showinfo("Report Generated", f"System self-check report has been saved to:\n{report_file}")
            
        except Exception as e:
            self.log_self_check_message(f"Error generating report: {str(e)}")
    
    def log_output(self, text):
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)

    def log_self_check_message(self, message):
        """记录自检消息"""
        # 这里可以添加消息日志功能
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] SELF-CHECK: {message}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixKaliApp(root)
    root.mainloop()
