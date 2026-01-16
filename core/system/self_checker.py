# 系统自检模块
# 包含硬件配置检测、系统状态监控、性能指标分析及潜在问题诊断功能

import platform
import psutil
import os
import socket
import wmi
import time
import cpuinfo
from datetime import datetime

class SystemSelfChecker:
    def __init__(self):
        self.wmi_client = None
        self.initialize()
    
    def initialize(self):
        """初始化系统自检模块"""
        try:
            if platform.system() == 'Windows':
                self.wmi_client = wmi.WMI()
        except Exception:
            pass
    
    def get_system_info(self):
        """获取系统基本信息"""
        info = {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'architecture': platform.architecture(),
            'machine': platform.machine(),
            'node': platform.node()
        }
        return info
    
    def get_hardware_info(self):
        """获取硬件配置信息"""
        hardware = {}
        
        # CPU信息
        hardware['cpu'] = self.get_cpu_info()
        
        # 内存信息
        hardware['memory'] = self.get_memory_info()
        
        # 存储信息
        hardware['storage'] = self.get_storage_info()
        
        # 网络信息
        hardware['network'] = self.get_network_info()
        
        # 显卡信息
        hardware['graphics'] = self.get_graphics_info()
        
        # 主板信息
        hardware['motherboard'] = self.get_motherboard_info()
        
        return hardware
    
    def get_cpu_info(self):
        """获取CPU信息"""
        cpu_info = {
            'processor': platform.processor(),
            'cpu_count': psutil.cpu_count(logical=True),
            'cpu_count_physical': psutil.cpu_count(logical=False),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'cpu_freq': {}
        }
        
        try:
            freq = psutil.cpu_freq()
            cpu_info['cpu_freq'] = {
                'current': freq.current,
                'min': freq.min,
                'max': freq.max
            }
        except Exception:
            pass
        
        try:
            cpu_info['details'] = cpuinfo.get_cpu_info()
        except Exception:
            pass
        
        return cpu_info
    
    def get_memory_info(self):
        """获取内存信息"""
        memory = psutil.virtual_memory()
        memory_info = {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'percent': memory.percent
        }
        
        # 获取交换内存信息
        try:
            swap = psutil.swap_memory()
            memory_info['swap'] = {
                'total': swap.total,
                'used': swap.used,
                'free': swap.free,
                'percent': swap.percent
            }
        except Exception:
            pass
        
        return memory_info
    
    def get_storage_info(self):
        """获取存储信息"""
        storage = []
        
        try:
            partitions = psutil.disk_partitions(all=True)
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    storage.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'opts': partition.opts,
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free,
                        'percent': usage.percent
                    })
                except Exception:
                    pass
        except Exception:
            pass
        
        return storage
    
    def get_network_info(self):
        """获取网络信息"""
        network = {
            'hostname': socket.gethostname(),
            'ip_addresses': [],
            'interfaces': []
        }
        
        # 获取IP地址
        try:
            for interface, addrs in psutil.net_if_addrs().items():
                interface_info = {
                    'name': interface,
                    'addresses': []
                }
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        network['ip_addresses'].append(addr.address)
                        interface_info['addresses'].append({
                            'family': 'IPv4',
                            'address': addr.address,
                            'netmask': addr.netmask,
                            'broadcast': addr.broadcast
                        })
                    elif addr.family == socket.AF_INET6:
                        interface_info['addresses'].append({
                            'family': 'IPv6',
                            'address': addr.address,
                            'netmask': addr.netmask
                        })
                network['interfaces'].append(interface_info)
        except Exception:
            pass
        
        # 获取网络统计信息
        try:
            network['stats'] = psutil.net_io_counters()
        except Exception:
            pass
        
        return network
    
    def get_graphics_info(self):
        """获取显卡信息"""
        graphics = []
        
        try:
            if platform.system() == 'Windows' and self.wmi_client:
                for gpu in self.wmi_client.Win32_VideoController():
                    graphics.append({
                        'name': gpu.Name,
                        'adapter_ram': gpu.AdapterRAM,
                        'driver_version': gpu.DriverVersion,
                        'status': gpu.Status
                    })
            elif platform.system() == 'Linux':
                # 尝试从lspci获取显卡信息
                try:
                    import subprocess
                    output = subprocess.check_output(['lspci'], text=True)
                    for line in output.split('\n'):
                        if 'VGA' in line or '3D' in line:
                            graphics.append({'name': line.strip()})
                except Exception:
                    pass
        except Exception:
            pass
        
        return graphics
    
    def get_motherboard_info(self):
        """获取主板信息"""
        motherboard = {}
        
        try:
            if platform.system() == 'Windows' and self.wmi_client:
                for board in self.wmi_client.Win32_BaseBoard():
                    motherboard = {
                        'manufacturer': board.Manufacturer,
                        'product': board.Product,
                        'version': board.Version,
                        'serial_number': board.SerialNumber
                    }
                    break
        except Exception:
            pass
        
        return motherboard
    
    def get_system_status(self):
        """获取系统状态"""
        status = {
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S'),
            'uptime': self.get_uptime(),
            'load_average': {},
            'temperature': {},
            'battery': {}
        }
        
        # 获取负载平均值
        try:
            if hasattr(psutil, 'getloadavg'):
                status['load_average'] = psutil.getloadavg()
        except Exception:
            pass
        
        # 获取温度信息
        try:
            if hasattr(psutil, 'sensors_temperatures'):
                status['temperature'] = psutil.sensors_temperatures()
        except Exception:
            pass
        
        # 获取电池信息
        try:
            if hasattr(psutil, 'sensors_battery'):
                battery = psutil.sensors_battery()
                if battery:
                    status['battery'] = {
                        'percent': battery.percent,
                        'secsleft': battery.secsleft,
                        'power_plugged': battery.power_plugged
                    }
        except Exception:
            pass
        
        return status
    
    def get_uptime(self):
        """获取系统运行时间"""
        uptime_seconds = time.time() - psutil.boot_time()
        uptime = {
            'seconds': uptime_seconds,
            'hours': uptime_seconds / 3600,
            'days': uptime_seconds / (3600 * 24)
        }
        return uptime
    
    def get_performance_metrics(self):
        """获取性能指标"""
        metrics = {
            'cpu': {},
            'memory': {},
            'disk': {},
            'network': {}
        }
        
        # CPU性能
        metrics['cpu']['usage'] = psutil.cpu_percent(interval=1, percpu=True)
        
        # 内存性能
        memory = psutil.virtual_memory()
        metrics['memory']['usage'] = memory.percent
        
        # 磁盘性能
        try:
            metrics['disk']['io_counters'] = psutil.disk_io_counters()
        except Exception:
            pass
        
        # 网络性能
        try:
            metrics['network']['io_counters'] = psutil.net_io_counters()
        except Exception:
            pass
        
        return metrics
    
    def diagnose_issues(self):
        """诊断潜在问题"""
        issues = {
            'critical': [],
            'warning': [],
            'info': []
        }
        
        # 检查CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 90:
            issues['critical'].append(f'CPU使用率过高: {cpu_percent}%')
        elif cpu_percent > 70:
            issues['warning'].append(f'CPU使用率较高: {cpu_percent}%')
        
        # 检查内存使用率
        memory = psutil.virtual_memory()
        if memory.percent > 90:
            issues['critical'].append(f'内存使用率过高: {memory.percent}%')
        elif memory.percent > 70:
            issues['warning'].append(f'内存使用率较高: {memory.percent}%')
        
        # 检查磁盘空间
        try:
            for partition in psutil.disk_partitions(all=True):
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    if usage.percent > 95:
                        issues['critical'].append(f'磁盘空间不足: {partition.mountpoint} ({usage.percent}%)')
                    elif usage.percent > 80:
                        issues['warning'].append(f'磁盘空间紧张: {partition.mountpoint} ({usage.percent}%)')
                except Exception:
                    pass
        except Exception:
            pass
        
        # 检查系统温度
        try:
            if hasattr(psutil, 'sensors_temperatures'):
                temps = psutil.sensors_temperatures()
                for name, entries in temps.items():
                    for entry in entries:
                        if hasattr(entry, 'current') and hasattr(entry, 'high'):
                            if entry.high and entry.current > entry.high:
                                issues['critical'].append(f'温度过高: {name} ({entry.current}°C)')
                            elif entry.current > entry.high * 0.8 if entry.high else False:
                                issues['warning'].append(f'温度较高: {name} ({entry.current}°C)')
        except Exception:
            pass
        
        # 检查电池状态
        try:
            if hasattr(psutil, 'sensors_battery'):
                battery = psutil.sensors_battery()
                if battery and not battery.power_plugged and battery.percent < 10:
                    issues['critical'].append(f'电池电量低: {battery.percent}%')
                elif battery and not battery.power_plugged and battery.percent < 20:
                    issues['warning'].append(f'电池电量较低: {battery.percent}%')
        except Exception:
            pass
        
        # 检查系统启动时间
        uptime_days = (time.time() - psutil.boot_time()) / (3600 * 24)
        if uptime_days > 30:
            issues['info'].append(f'系统已运行 {uptime_days:.1f} 天，建议重启')
        
        return issues
    
    def get_process_info(self, limit=20):
        """获取进程信息"""
        processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    process_info = proc.info
                    processes.append(process_info)
                except Exception:
                    pass
            
            # 按CPU使用率排序
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            processes = processes[:limit]
        except Exception:
            pass
        
        return processes
    
    def get_service_info(self):
        """获取服务信息"""
        services = []
        
        try:
            if platform.system() == 'Windows':
                for service in psutil.win_service_iter():
                    try:
                        service_info = service.as_dict()
                        services.append(service_info)
                    except Exception:
                        pass
            elif platform.system() == 'Linux':
                # 尝试获取systemd服务
                try:
                    import subprocess
                    output = subprocess.check_output(['systemctl', 'list-units', '--type=service', '--state=running'], text=True)
                    for line in output.split('\n')[1:]:
                        if line.strip():
                            parts = line.split()
                            if len(parts) > 3:
                                services.append({
                                    'name': parts[0],
                                    'status': parts[2],
                                    'description': ' '.join(parts[3:])
                                })
                except Exception:
                    pass
        except Exception:
            pass
        
        return services
    
    def generate_report(self):
        """生成完整的系统自检报告"""
        report = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'system_info': self.get_system_info(),
            'hardware_info': self.get_hardware_info(),
            'system_status': self.get_system_status(),
            'performance_metrics': self.get_performance_metrics(),
            'issues': self.diagnose_issues(),
            'top_processes': self.get_process_info(),
            'services': self.get_service_info()
        }
        
        return report

# 全局实例
system_self_checker = SystemSelfChecker()

# 示例用法
if __name__ == "__main__":
    print("正在生成系统自检报告...")
    report = system_self_checker.generate_report()
    print(f"报告生成时间: {report['timestamp']}")
    print(f"系统: {report['system_info']['system']} {report['system_info']['release']}")
    print(f"CPU使用率: {report['hardware_info']['cpu']['cpu_percent']}%")
    print(f"内存使用率: {report['hardware_info']['memory']['percent']}%")
    print(f"发现的问题:")
    for severity, items in report['issues'].items():
        if items:
            print(f"  {severity.upper()}:")
            for item in items:
                print(f"    - {item}")
