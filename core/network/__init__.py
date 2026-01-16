# 网络安全模块主文件
# 整合流量监控、恶意软件检测和入侵防御功能

from .traffic_monitor import NetworkMonitor
from .malware_detector import MalwareDetector
from .intrusion_prevention import IntrusionPrevention
from .vulnerability_scanner import VulnerabilityScanner

class NetworkSecurity:
    def __init__(self):
        self.traffic_monitor = NetworkMonitor()
        self.malware_detector = MalwareDetector()
        self.intrusion_prevention = IntrusionPrevention()
        self.vulnerability_scanner = VulnerabilityScanner()
        self.is_initialized = False
    
    def initialize(self):
        """初始化网络安全模块"""
        if not self.is_initialized:
            # 加载特征数据库
            self.malware_detector.load_signature_db()
            self.is_initialized = True
    
    def start_monitoring(self, interface=None):
        """开始所有监控功能"""
        self.initialize()
        self.traffic_monitor.start_monitoring(interface)
        self.intrusion_prevention.start_monitoring()
    
    def stop_monitoring(self):
        """停止所有监控功能"""
        self.traffic_monitor.stop_monitoring()
        self.intrusion_prevention.stop_monitoring()
    
    def get_network_statistics(self):
        """获取网络统计信息"""
        return self.traffic_monitor.get_statistics()
    
    def get_recent_packets(self, limit=100):
        """获取最近的数据包"""
        return self.traffic_monitor.get_recent_packets(limit)
    
    def get_top_flows(self, limit=10):
        """获取流量最大的前N个流"""
        return self.traffic_monitor.get_top_flows(limit)
    
    def scan_file(self, file_path):
        """扫描单个文件"""
        return self.malware_detector.scan_file(file_path)
    
    def scan_directory(self, directory, recursive=True):
        """扫描目录"""
        return self.malware_detector.scan_directory(directory, recursive)
    
    def analyze_process(self, process_info):
        """分析进程行为"""
        return self.malware_detector.analyze_process(process_info)
    
    def add_connection(self, connection_info):
        """添加连接信息（用于入侵检测）"""
        return self.intrusion_prevention.add_connection(connection_info)
    
    def get_blocked_ips(self):
        """获取被阻止的IP列表"""
        return self.intrusion_prevention.get_blocked_ips()
    
    def unblock_ip(self, ip):
        """解除IP阻止"""
        return self.intrusion_prevention.unblock_ip(ip)
    
    def get_security_status(self):
        """获取整体安全状态"""
        network_stats = self.get_network_statistics()
        blocked_ips = self.get_blocked_ips()
        
        status = {
            'network': {
                'packet_count': network_stats['packet_count'],
                'flow_count': network_stats['flow_count'],
                'active_flows': network_stats['active_flows']
            },
            'security': {
                'blocked_ips': len(blocked_ips),
                'blocked_ip_list': blocked_ips
            },
            'status': 'normal'  # 默认状态
        }
        
        # 根据数据判断状态
        if len(blocked_ips) > 5:
            status['status'] = 'critical'
        elif network_stats['active_flows'] > 100:
            status['status'] = 'warning'
        
        return status
    
    def scan_system_vulnerabilities(self):
        """扫描系统漏洞"""
        return self.vulnerability_scanner.scan_system()
    
    def scan_network_vulnerabilities(self, target=None):
        """扫描网络漏洞"""
        return self.vulnerability_scanner.scan_network(target)
    
    def generate_vulnerability_report(self, scan_results):
        """生成漏洞扫描报告"""
        return self.vulnerability_scanner.generate_report(scan_results)

# 全局实例
network_security = NetworkSecurity()

# 示例用法
if __name__ == "__main__":
    print("初始化网络安全模块...")
    network_security.initialize()
    
    print("开始监控...")
    network_security.start_monitoring()
    
    try:
        import time
        while True:
            time.sleep(5)
            status = network_security.get_security_status()
            print(f"安全状态: {status['status']}")
            print(f"网络统计: 数据包={status['network']['packet_count']}, 流数={status['network']['flow_count']}")
            print(f"安全统计: 阻止IP数={status['security']['blocked_ips']}")
    except KeyboardInterrupt:
        print("\n停止监控...")
        network_security.stop_monitoring()