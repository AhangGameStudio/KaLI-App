# 跨平台工具模块
# 提供统一的工具调用接口

import os
import subprocess
import threading
from core.config import platform_config, app_config

class ToolManager:
    """工具管理类"""
    
    def __init__(self):
        self.tools = {
            'wifite': {
                'path': None,
                'description': 'Wireless network scanner and cracker',
                'required': True,
                'dependencies': ['python3', 'aircrack-ng', 'reaver']
            },
            'aircrack-ng': {
                'path': None,
                'description': 'WiFi password cracking tool',
                'required': False,
                'dependencies': []
            },
            'reaver': {
                'path': None,
                'description': 'WPS PIN cracker',
                'required': False,
                'dependencies': []
            },
            'nmap': {
                'path': None,
                'description': 'Network scanner',
                'required': False,
                'dependencies': []
            }
        }
        
        # 初始化工具路径
        self._initialize_tool_paths()
    
    def _initialize_tool_paths(self):
        """初始化工具路径"""
        for tool_name in self.tools:
            # 首先尝试使用工具管理器中的路径
            tool_path = platform_config.get_tool_path(tool_name)
            if tool_path:
                self.tools[tool_name]['path'] = tool_path
            else:
                # 尝试使用系统路径
                try:
                    if platform_config.is_windows():
                        # Windows系统使用where命令
                        result = subprocess.run(['where', tool_name], capture_output=True, text=True)
                        if result.returncode == 0:
                            self.tools[tool_name]['path'] = result.stdout.strip().split('\n')[0]
                    else:
                        # Unix系统使用which命令
                        result = subprocess.run(['which', tool_name], capture_output=True, text=True)
                        if result.returncode == 0:
                            self.tools[tool_name]['path'] = result.stdout.strip()
                except Exception:
                    pass
    
    def get_tool_path(self, tool_name):
        """获取工具路径"""
        if tool_name in self.tools:
            return self.tools[tool_name]['path']
        return None
    
    def is_tool_available(self, tool_name):
        """检查工具是否可用"""
        tool_path = self.get_tool_path(tool_name)
        return tool_path is not None and os.path.exists(tool_path)
    
    def run_tool(self, tool_name, args=[], timeout=60):
        """运行工具"""
        tool_path = self.get_tool_path(tool_name)
        
        if not tool_path:
            return {
                'success': False,
                'error': f'Tool {tool_name} not found'
            }
        
        try:
            # 构建命令
            cmd = [tool_path] + args
            
            # 执行命令
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Command timed out'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def run_tool_async(self, tool_name, args=[], callback=None, timeout=60):
        """异步运行工具"""
        def execute():
            result = self.run_tool(tool_name, args, timeout)
            if callback:
                callback(result)
        
        thread = threading.Thread(target=execute, daemon=True)
        thread.start()
        return thread
    
    def get_tool_info(self, tool_name):
        """获取工具信息"""
        if tool_name in self.tools:
            return self.tools[tool_name]
        return None
    
    def get_available_tools(self):
        """获取可用工具列表"""
        available_tools = []
        for tool_name, info in self.tools.items():
            if self.is_tool_available(tool_name):
                available_tools.append({
                    'name': tool_name,
                    'path': info['path'],
                    'description': info['description']
                })
        return available_tools
    
    def check_dependencies(self, tool_name):
        """检查工具依赖"""
        if tool_name not in self.tools:
            return {'missing': [tool_name]}
        
        info = self.tools[tool_name]
        missing = []
        
        for dep in info['dependencies']:
            if not self.is_tool_available(dep):
                missing.append(dep)
        
        return {
            'missing': missing,
            'available': [dep for dep in info['dependencies'] if self.is_tool_available(dep)]
        }
    
    def install_dependencies(self, tool_name):
        """安装工具依赖"""
        # 这里只是一个示例，实际安装逻辑需要根据平台实现
        # 在Linux上可以使用apt、yum等包管理器
        # 在Windows上可能需要下载安装程序
        # 在Android上需要通过Termux安装
        pass

class CommandExecutor:
    """命令执行器"""
    
    @staticmethod
    def execute(cmd, shell=False, timeout=30):
        """执行命令"""
        try:
            result = subprocess.run(
                cmd,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Command timed out'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def execute_async(cmd, shell=False, callback=None, timeout=30):
        """异步执行命令"""
        def execute():
            result = CommandExecutor.execute(cmd, shell, timeout)
            if callback:
                callback(result)
        
        thread = threading.Thread(target=execute, daemon=True)
        thread.start()
        return thread

# 全局实例
tool_manager = ToolManager()
command_executor = CommandExecutor()
