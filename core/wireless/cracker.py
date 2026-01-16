# WIFI破解模块
# 基于Wifite2的破解功能

import os
import subprocess
import time

class WifiCracker:
    def __init__(self):
        self.is_cracking = False
        self.crack_process = None
        self.supported_attacks = {
            "wep": "WEP encryption cracking",
            "wpa": "WPA/WPA2 handshake capture and crack",
            "wps": "WPS PIN attack",
            "pmkid": "PMKID hash capture and crack"
        }
    
    def crack(self, network, interface=None, attack_type="wpa", wordlist=None):
        """破解WIFI密码"""
        if not network:
            return {"success": False, "error": "Network information required"}
        
        # 从network对象中提取bssid
        target_bssid = network.get('bssid')
        if not target_bssid:
            return {"success": False, "error": "Target BSSID required"}
        
        if attack_type not in self.supported_attacks:
            return {"success": False, "error": f"Unsupported attack type: {attack_type}"}
        
        self.is_cracking = True
        
        try:
            # 尝试使用Wifite2进行破解
            wifite_path = os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'wifite2', 'Wifite.py')
            wifite_path = os.path.abspath(wifite_path)
            
            if os.path.exists(wifite_path):
                result = self._wifite_crack(wifite_path, target_bssid, interface, attack_type, wordlist)
            else:
                # 如果Wifite2不存在，返回错误
                result = {"success": False, "error": "Wifite2 not found"}
                
        except Exception as e:
            result = {"success": False, "error": str(e)}
        finally:
            self.is_cracking = False
            self.crack_process = None
        
        return result
    
    def stop_crack(self):
        """停止破解"""
        if self.crack_process:
            try:
                self.crack_process.kill()
            except:
                pass
    
    def get_supported_attacks(self):
        """获取支持的攻击类型"""
        return self.supported_attacks
    
    def _wifite_crack(self, wifite_path, target_bssid, interface, attack_type, wordlist):
        """使用Wifite2进行破解"""
        # 构建命令
        cmd = ['python', wifite_path, '--bssid', target_bssid]
        
        # 添加接口参数
        if interface:
            cmd.extend(['--iface', interface])
        
        # 根据攻击类型添加参数
        if attack_type == "wep":
            cmd.extend(['--wep'])
        elif attack_type == "wpa":
            cmd.extend(['--wpa'])
        elif attack_type == "wps":
            cmd.extend(['--wps'])
        elif attack_type == "pmkid":
            cmd.extend(['--pmkid'])
        
        # 添加字典文件
        if wordlist and os.path.exists(wordlist):
            cmd.extend(['--dict', wordlist])
        
        # 执行命令
        self.crack_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待命令完成
        stdout, stderr = self.crack_process.communicate()
        
        # 解析输出
        result = self._parse_wifite_crack_output(stdout, stderr)
        
        return result
    
    def _parse_wifite_crack_output(self, stdout, stderr):
        """解析Wifite2的破解输出"""
        # 简单的解析逻辑，实际需要根据Wifite2的输出格式调整
        result = {"success": False, "password": None, "error": "Crack failed"}
        
        # 检查输出中是否有密码
        lines = stdout.split('\n')
        for line in lines:
            if 'KEY FOUND' in line or 'Password:' in line or 'password' in line.lower():
                # 提取密码
                parts = line.split(':')
                if len(parts) > 1:
                    password = parts[1].strip()
                    result["success"] = True
                    result["password"] = password
                    result["error"] = None
                    break
        
        # 如果没有找到密码，检查错误信息
        if not result["success"]:
            if "No targets found" in stdout:
                result["error"] = "Target not found"
            elif "No handshake" in stdout:
                result["error"] = "No handshake captured"
            elif stderr:
                result["error"] = stderr[:200]  # 只取前200个字符
            else:
                result["error"] = "Crack failed"
        
        return result