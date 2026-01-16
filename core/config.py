# 跨平台配置模块
# 提供统一的配置管理和平台检测功能

import os
import sys
import platform

class PlatformConfig:
    """平台配置管理类"""
    
    @staticmethod
    def get_platform():
        """获取当前平台"""
        return platform.system().lower()
    
    @staticmethod
    def is_windows():
        """检查是否为Windows平台"""
        return PlatformConfig.get_platform() == 'windows'
    
    @staticmethod
    def is_linux():
        """检查是否为Linux平台"""
        return PlatformConfig.get_platform() == 'linux'
    
    @staticmethod
    def is_macos():
        """检查是否为macOS平台"""
        return PlatformConfig.get_platform() == 'darwin'
    
    @staticmethod
    def is_android():
        """检查是否为Android平台"""
        return 'ANDROID_ARGUMENT' in os.environ or ('ANDROID_HOME' in os.environ and 'python-for-android' in sys.modules)
    
    @staticmethod
    def get_app_data_dir():
        """获取应用数据目录"""
        platform = PlatformConfig.get_platform()
        
        if platform == 'windows':
            return os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'KaLI-App')
        elif platform == 'linux':
            return os.path.join(os.environ.get('XDG_DATA_HOME', os.path.expanduser('~/.local/share')), 'KaLI-App')
        elif platform == 'darwin':
            return os.path.join(os.path.expanduser('~/Library/Application Support'), 'KaLI-App')
        else:
            return os.path.join(os.path.expanduser('~'), '.KaLI-App')
    
    @staticmethod
    def get_config_dir():
        """获取配置目录"""
        platform = PlatformConfig.get_platform()
        
        if platform == 'windows':
            return os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'KaLI-App', 'config')
        elif platform == 'linux':
            return os.path.join(os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config')), 'KaLI-App')
        elif platform == 'darwin':
            return os.path.join(os.path.expanduser('~/Library/Preferences'), 'KaLI-App')
        else:
            return os.path.join(os.path.expanduser('~'), '.KaLI-App', 'config')
    
    @staticmethod
    def get_cache_dir():
        """获取缓存目录"""
        platform = PlatformConfig.get_platform()
        
        if platform == 'windows':
            return os.path.join(os.environ.get('TEMP', os.path.expanduser('~')), 'KaLI-App', 'cache')
        elif platform == 'linux':
            return os.path.join(os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~/.cache')), 'KaLI-App')
        elif platform == 'darwin':
            return os.path.join(os.path.expanduser('~/Library/Caches'), 'KaLI-App')
        else:
            return os.path.join(os.path.expanduser('~'), '.KaLI-App', 'cache')
    
    @staticmethod
    def ensure_directories():
        """确保必要的目录存在"""
        dirs = [
            PlatformConfig.get_app_data_dir(),
            PlatformConfig.get_config_dir(),
            PlatformConfig.get_cache_dir()
        ]
        
        for directory in dirs:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory, exist_ok=True)
                except Exception:
                    pass
    
    @staticmethod
    def get_tool_path(tool_name):
        """获取工具路径"""
        # 优先使用相对路径
        tool_path = os.path.join(os.path.dirname(__file__), '..', '..', 'tools', tool_name)
        tool_path = os.path.abspath(tool_path)
        
        if os.path.exists(tool_path):
            return tool_path
        
        # 尝试使用系统路径
        for path in os.environ.get('PATH', '').split(os.pathsep):
            system_tool_path = os.path.join(path, tool_name)
            if os.path.exists(system_tool_path):
                return system_tool_path
        
        return None

class AppConfig:
    """应用配置管理类"""
    
    def __init__(self):
        self.config = {
            'app_name': 'KaLI-App',
            'version': '1.0.0',
            'author': 'AhangGameStudio',
            'description': 'Cross-platform security toolkit',
            'debug': False,
            'log_level': 'INFO',
            'timeout': 30,
            'max_history': 1000,
            'wordlist_path': None,
            'plugins': []
        }
        
        # 加载配置文件
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        config_dir = PlatformConfig.get_config_dir()
        config_file = os.path.join(config_dir, 'config.json')
        
        if os.path.exists(config_file):
            try:
                import json
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    self.config.update(user_config)
            except Exception:
                pass
    
    def save_config(self):
        """保存配置文件"""
        config_dir = PlatformConfig.get_config_dir()
        config_file = os.path.join(config_dir, 'config.json')
        
        try:
            import json
            os.makedirs(config_dir, exist_ok=True)
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def get(self, key, default=None):
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """设置配置值"""
        self.config[key] = value
        self.save_config()
    
    def get_wordlist_path(self):
        """获取字典文件路径"""
        if self.config['wordlist_path'] and os.path.exists(self.config['wordlist_path']):
            return self.config['wordlist_path']
        
        # 尝试使用内置字典
        wordlist_path = os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'wifite2', 'wordlist-top4800-probable.txt')
        wordlist_path = os.path.abspath(wordlist_path)
        
        if os.path.exists(wordlist_path):
            return wordlist_path
        
        return None
    
    def get_plugins(self):
        """获取插件列表"""
        return self.config['plugins']
    
    def add_plugin(self, plugin_name):
        """添加插件"""
        if plugin_name not in self.config['plugins']:
            self.config['plugins'].append(plugin_name)
            self.save_config()
    
    def remove_plugin(self, plugin_name):
        """移除插件"""
        if plugin_name in self.config['plugins']:
            self.config['plugins'].remove(plugin_name)
            self.save_config()

# 全局配置实例
platform_config = PlatformConfig()
app_config = AppConfig()

# 确保目录结构存在
platform_config.ensure_directories()
