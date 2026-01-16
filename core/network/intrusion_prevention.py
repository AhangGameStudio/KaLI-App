# 入侵防御模块
# 实现异常连接检测与阻止

import time
import threading
from collections import defaultdict, deque

class IntrusionPrevention:
    def __init__(self):
        self.connection_history = defaultdict(lambda: deque(maxlen=100))
        self.blocked_ips = set()
        self.rules = self.load_rules()
        self.is_running = False
        self.monitor_thread = None
    
    def load_rules(self):
        """加载入侵检测规则"""
        return [
            {
                'name': '端口扫描检测',
                'threshold': 10,  # 10秒内尝试连接超过10个不同端口
                'time_window': 10,
                'action': 'block',
                'severity': 'high'
            },
            {
                'name': '连接频率检测',
                'threshold': 50,  # 5秒内超过50个连接
                'time_window': 5,
                'action': 'block',
                'severity': 'medium'
            },
            {
                'name': '异常协议检测',
                'pattern': lambda conn: conn.get('protocol') == 'ICMP' and conn.get('type') == 8,  # ICMP Echo Request
                'threshold': 20,  # 10秒内超过20个ICMP请求
                'time_window': 10,
                'action': 'block',
                'severity': 'medium'
            }
        ]
    
    def start_monitoring(self):
        """开始入侵防御监控"""
        self.is_running = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True
        )
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """停止入侵防御监控"""
        self.is_running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
    
    def _monitoring_loop(self):
        """监控循环"""
        while self.is_running:
            time.sleep(1)
            self.detect_intrusions()
    
    def add_connection(self, connection_info):
        """添加连接信息"""
        src_ip = connection_info.get('src')
        if not src_ip:
            return
        
        # 检查是否已被阻止
        if src_ip in self.blocked_ips:
            return {'status': 'blocked', 'reason': 'IP已被阻止'}
        
        # 记录连接
        timestamp = time.time()
        connection_info['timestamp'] = timestamp
        self.connection_history[src_ip].append(connection_info)
        
        # 实时检测
        alerts = self.check_rules(src_ip)
        if alerts:
            for alert in alerts:
                if alert['action'] == 'block':
                    self.block_ip(src_ip, alert['rule'])
        
        return {'status': 'allowed'}
    
    def check_rules(self, src_ip):
        """检查规则"""
        alerts = []
        connections = self.connection_history[src_ip]
        current_time = time.time()
        
        for rule in self.rules:
            if 'threshold' in rule:
                # 基于阈值的规则
                time_window = rule['time_window']
                threshold = rule['threshold']
                
                # 统计时间窗口内的连接
                recent_connections = [
                    conn for conn in connections
                    if current_time - conn['timestamp'] <= time_window
                ]
                
                if 'pattern' in rule:
                    # 基于模式的规则
                    matching_connections = [
                        conn for conn in recent_connections
                        if rule['pattern'](conn)
                    ]
                    if len(matching_connections) > threshold:
                        alerts.append({
                            'rule': rule['name'],
                            'action': rule['action'],
                            'severity': rule['severity'],
                            'count': len(matching_connections)
                        })
                else:
                    # 基于端口扫描的规则
                    unique_ports = set()
                    for conn in recent_connections:
                        if 'dport' in conn:
                            unique_ports.add(conn['dport'])
                    
                    if len(unique_ports) > threshold:
                        alerts.append({
                            'rule': rule['name'],
                            'action': rule['action'],
                            'severity': rule['severity'],
                            'count': len(unique_ports)
                        })
        
        return alerts
    
    def detect_intrusions(self):
        """检测入侵行为"""
        for src_ip in list(self.connection_history.keys()):
            alerts = self.check_rules(src_ip)
            if alerts:
                for alert in alerts:
                    if alert['action'] == 'block':
                        self.block_ip(src_ip, alert['rule'])
    
    def block_ip(self, ip, reason):
        """阻止IP"""
        self.blocked_ips.add(ip)
        print(f"阻止IP: {ip}, 原因: {reason}")
    
    def unblock_ip(self, ip):
        """解除IP阻止"""
        if ip in self.blocked_ips:
            self.blocked_ips.remove(ip)
            print(f"解除阻止IP: {ip}")
    
    def get_blocked_ips(self):
        """获取被阻止的IP列表"""
        return list(self.blocked_ips)
    
    def get_alert_history(self, limit=50):
        """获取告警历史"""
        # 这里可以实现告警历史记录
        return []
    
    def get_statistics(self):
        """获取统计信息"""
        return {
            'blocked_ips': len(self.blocked_ips),
            'monitored_ips': len(self.connection_history),
            'rules_count': len(self.rules)
        }

# 示例用法
if __name__ == "__main__":
    ips = IntrusionPrevention()
    print("开始入侵防御监控...")
    ips.start_monitoring()
    
    # 模拟一些连接
    test_connections = [
        {'src': '192.168.1.100', 'dst': '192.168.1.1', 'dport': 22, 'protocol': 'TCP'},
        {'src': '192.168.1.100', 'dst': '192.168.1.1', 'dport': 80, 'protocol': 'TCP'},
        {'src': '192.168.1.100', 'dst': '192.168.1.1', 'dport': 443, 'protocol': 'TCP'},
        {'src': '192.168.1.100', 'dst': '192.168.1.1', 'dport': 3389, 'protocol': 'TCP'},
        {'src': '192.168.1.100', 'dst': '192.168.1.1', 'dport': 8080, 'protocol': 'TCP'},
    ]
    
    for conn in test_connections:
        ips.add_connection(conn)
    
    try:
        while True:
            time.sleep(2)
            stats = ips.get_statistics()
            print(f"统计信息: 阻止IP数={stats['blocked_ips']}, 监控IP数={stats['monitored_ips']}")
            print(f"被阻止的IP: {ips.get_blocked_ips()}")
    except KeyboardInterrupt:
        print("\n停止入侵防御监控...")
        ips.stop_monitoring()