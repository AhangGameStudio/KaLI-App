# WIFI扫描模块
# 基于Wifite2的扫描功能

import os
import subprocess
import time
import json

class WifiScanner:
    def __init__(self):
        self.is_scanning = False
        self.scan_process = None
    
    def scan(self, interface=None, timeout=30):
        """扫描周围的WIFI网络"""
        self.is_scanning = True
        results = []
        
        try:
            # 尝试使用Wifite2进行扫描
            wifite_path = os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'wifite2', 'Wifite.py')
            wifite_path = os.path.abspath(wifite_path)
            
            if os.path.exists(wifite_path):
                # 使用Wifite2的扫描功能
                cmd = ['python', wifite_path, '--scan', '--iface', interface] if interface else ['python', wifite_path, '--scan']
                
                # 执行命令
                self.scan_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # 等待扫描完成
                try:
                    stdout, stderr = self.scan_process.communicate(timeout=timeout)
                    
                    # 解析Wifite2的输出
                    results = self._parse_wifite_output(stdout)
                except subprocess.TimeoutExpired:
                    self.scan_process.kill()
                    results = [{"ssid": "Scan timeout", "bssid": "N/A", "signal": "N/A", "channel": "N/A", "encryption": "N/A"}]
            else:
                # 如果Wifite2不存在，使用系统命令
                results = self._system_scan(interface)
                
        except Exception as e:
            results = [{"ssid": f"Error: {str(e)}", "bssid": "N/A", "signal": "N/A", "channel": "N/A", "encryption": "N/A"}]
        finally:
            self.is_scanning = False
            self.scan_process = None
        
        return results
    
    def stop_scan(self):
        """停止扫描"""
        if self.scan_process:
            try:
                self.scan_process.kill()
            except:
                pass
    
    def get_interface_info(self):
        """获取网络接口信息"""
        interfaces = []
        
        try:
            # 使用系统命令获取接口信息
            if os.name == 'nt':
                # Windows系统
                output = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], text=True, stderr=subprocess.DEVNULL)
                # 解析输出
                interfaces = self._parse_windows_interfaces(output)
            else:
                # Linux/Mac系统
                output = subprocess.check_output(['iwconfig'], text=True, stderr=subprocess.DEVNULL)
                # 解析输出
                interfaces = self._parse_linux_interfaces(output)
                
        except Exception:
            pass
        
        return interfaces
    
    def _parse_wifite_output(self, output):
        """解析Wifite2的扫描输出"""
        results = []
        
        # 简单的解析逻辑，实际需要根据Wifite2的输出格式调整
        lines = output.split('\n')
        for line in lines:
            if 'BSSID' in line and 'ESSID' in line:
                # 提取信息
                parts = line.split()
                bssid = parts[0]
                ssid = ' '.join(parts[2:])
                results.append({
                    "ssid": ssid,
                    "bssid": bssid,
                    "signal": "N/A",
                    "channel": "N/A",
                    "encryption": "N/A"
                })
        
        return results
    
    def _system_scan(self, interface):
        """使用系统命令进行扫描"""
        results = []
        
        try:
            if os.name == 'nt':
                # Windows系统
                output = subprocess.check_output(['netsh', 'wlan', 'show', 'networks', 'mode=bssid'], text=True, stderr=subprocess.DEVNULL)
                results = self._parse_windows_scan(output)
            else:
                # Linux/Mac系统
                if interface:
                    cmd = ['iwlist', interface, 'scan']
                else:
                    cmd = ['iwlist', 'scan']
                
                output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
                results = self._parse_linux_scan(output)
                
        except Exception:
            results = [{"ssid": "System scan failed", "bssid": "N/A", "signal": "N/A", "channel": "N/A", "encryption": "N/A"}]
        
        return results
    
    def _parse_windows_scan(self, output):
        """解析Windows系统的扫描输出"""
        results = []
        current_network = {}
        
        lines = output.split('\n')
        for line in lines:
            line = line.strip()
            
            if 'SSID' in line:
                if current_network:
                    results.append(current_network)
                    current_network = {}
                current_network['ssid'] = line.split(':', 1)[1].strip()
            elif 'BSSID' in line:
                current_network['bssid'] = line.split(':', 1)[1].strip()
            elif 'Signal' in line:
                current_network['signal'] = line.split(':', 1)[1].strip()
            elif 'Channel' in line:
                current_network['channel'] = line.split(':', 1)[1].strip()
            elif 'Authentication' in line:
                current_network['encryption'] = line.split(':', 1)[1].strip()
        
        if current_network:
            results.append(current_network)
        
        return results
    
    def _parse_linux_scan(self, output):
        """解析Linux系统的扫描输出"""
        results = []
        current_network = {}
        
        lines = output.split('\n')
        for line in lines:
            line = line.strip()
            
            if 'ESSID' in line:
                if current_network:
                    results.append(current_network)
                    current_network = {}
                current_network['ssid'] = line.split(':', 1)[1].strip('"')
            elif 'Address' in line:
                current_network['bssid'] = line.split(':', 1)[1].strip()
            elif 'Quality' in line:
                current_network['signal'] = line.split('=')[1].split(' ')[0]
            elif 'Channel' in line:
                current_network['channel'] = line.split(':', 1)[1].strip()
            elif 'Encryption key' in line:
                current_network['encryption'] = 'WEP' if 'on' in line else 'Open'
            elif 'IE: IEEE 802.11i/WPA2 Version 1' in line:
                current_network['encryption'] = 'WPA2'
            elif 'IE: IEEE 802.11i/WPA Version 1' in line:
                current_network['encryption'] = 'WPA'
        
        if current_network:
            results.append(current_network)
        
        return results
    
    def _parse_windows_interfaces(self, output):
        """解析Windows接口信息"""
        interfaces = []
        current_interface = {}
        
        lines = output.split('\n')
        for line in lines:
            line = line.strip()
            
            if 'Name' in line:
                if current_interface:
                    interfaces.append(current_interface)
                    current_interface = {}
                current_interface['name'] = line.split(':', 1)[1].strip()
            elif 'State' in line:
                current_interface['state'] = line.split(':', 1)[1].strip()
        
        if current_interface:
            interfaces.append(current_interface)
        
        return interfaces
    
    def _parse_linux_interfaces(self, output):
        """解析Linux接口信息"""
        interfaces = []
        
        lines = output.split('\n')
        current_interface = {}
        
        for line in lines:
            if ':' in line and not line.startswith(' '):
                if current_interface:
                    interfaces.append(current_interface)
                    current_interface = {}
                
                interface_name = line.split(':')[0].strip()
                current_interface['name'] = interface_name
            elif 'ESSID' in line:
                current_interface['ssid'] = line.split(':', 1)[1].strip('"')
            elif 'Mode' in line:
                current_interface['mode'] = line.split(':', 1)[1].strip()
        
        if current_interface:
            interfaces.append(current_interface)
        
        return interfaces