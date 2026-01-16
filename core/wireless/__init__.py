# 无线WIFI扫描与破解工具模块
# 基于现有Wifite2工具进行封装和扩展

import os
import subprocess
import threading
import time
from core.wireless.scanner import WifiScanner
from core.wireless.cracker import WifiCracker

class WirelessTool:
    def __init__(self):
        self.scanner = WifiScanner()
        self.cracker = WifiCracker()
        self.is_scanning = False
        self.is_cracking = False
        self.scan_results = []
        self.crack_results = {}
    
    def start_scan(self, interface=None):
        """开始WIFI扫描"""
        if self.is_scanning:
            return {"status": "error", "message": "Scanning already in progress"}
        
        self.is_scanning = True
        self.scan_results = []
        
        def scan_thread():
            try:
                self.scan_results = self.scanner.scan(interface)
            finally:
                self.is_scanning = False
        
        # 启动扫描线程
        thread = threading.Thread(target=scan_thread, daemon=True)
        thread.start()
        
        return {"status": "started", "message": "Scanning started"}
    
    def stop_scan(self):
        """停止WIFI扫描"""
        if not self.is_scanning:
            return {"status": "error", "message": "No scanning in progress"}
        
        self.scanner.stop_scan()
        self.is_scanning = False
        return {"status": "stopped", "message": "Scanning stopped"}
    
    def get_scan_results(self):
        """获取扫描结果"""
        return self.scan_results
    
    def start_crack(self, target_bssid, attack_type="wpa", wordlist=None):
        """开始破解"""
        if self.is_cracking:
            return {"status": "error", "message": "Cracking already in progress"}
        
        if not target_bssid:
            return {"status": "error", "message": "Target BSSID required"}
        
        self.is_cracking = True
        self.crack_results[target_bssid] = {"status": "in_progress", "result": None}
        
        def crack_thread():
            try:
                result = self.cracker.crack(target_bssid, attack_type, wordlist)
                self.crack_results[target_bssid] = {"status": "completed", "result": result}
            except Exception as e:
                self.crack_results[target_bssid] = {"status": "error", "result": str(e)}
            finally:
                self.is_cracking = False
        
        # 启动破解线程
        thread = threading.Thread(target=crack_thread, daemon=True)
        thread.start()
        
        return {"status": "started", "message": f"Cracking started for {target_bssid}"}
    
    def stop_crack(self):
        """停止破解"""
        if not self.is_cracking:
            return {"status": "error", "message": "No cracking in progress"}
        
        self.cracker.stop_crack()
        self.is_cracking = False
        return {"status": "stopped", "message": "Cracking stopped"}
    
    def get_crack_status(self, target_bssid):
        """获取破解状态"""
        return self.crack_results.get(target_bssid, {"status": "not_started", "result": None})
    
    def get_supported_attacks(self):
        """获取支持的攻击类型"""
        return self.cracker.get_supported_attacks()
    
    def get_interface_info(self):
        """获取网络接口信息"""
        return self.scanner.get_interface_info()

# 全局实例
wireless_tool = WirelessTool()

# 示例用法
if __name__ == "__main__":
    print("Wireless Tool Test")
    
    # 扫描WIFI
    print("Scanning for WIFI networks...")
    result = wireless_tool.start_scan()
    print(f"Scan started: {result}")
    
    # 等待扫描完成
    time.sleep(10)
    
    # 获取扫描结果
    results = wireless_tool.get_scan_results()
    print(f"Scan results: {len(results)} networks found")
    
    for network in results:
        print(f"SSID: {network.get('ssid', 'N/A')}, BSSID: {network.get('bssid', 'N/A')}, Signal: {network.get('signal', 'N/A')}")