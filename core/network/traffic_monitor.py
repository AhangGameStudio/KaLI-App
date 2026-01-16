# 网络流量监控模块
# 基于scapy库实现数据包捕获与分析

import threading
import time
from scapy.all import sniff, IP, TCP, UDP, ICMP

class NetworkMonitor:
    def __init__(self):
        self.is_monitoring = False
        self.packet_count = 0
        self.flow_data = {}
        self.packet_history = []
        self.max_history = 1000
        self.monitor_thread = None
    
    def start_monitoring(self, interface=None):
        """开始网络流量监控"""
        self.is_monitoring = True
        self.packet_count = 0
        self.flow_data = {}
        self.packet_history = []
        
        def packet_handler(packet):
            if not self.is_monitoring:
                return
            
            self.packet_count += 1
            
            # 分析数据包
            packet_info = self.analyze_packet(packet)
            
            # 存储数据包信息
            if packet_info:
                self.packet_history.append(packet_info)
                if len(self.packet_history) > self.max_history:
                    self.packet_history.pop(0)
                
                # 更新流量数据
                self.update_flow_data(packet_info)
        
        # 启动监控线程
        self.monitor_thread = threading.Thread(
            target=sniff,
            kwargs={
                'prn': packet_handler,
                'iface': interface,
                'store': 0
            },
            daemon=True
        )
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """停止网络流量监控"""
        self.is_monitoring = False
        if self.monitor_thread:
            # 等待线程结束
            self.monitor_thread.join(timeout=2)
    
    def analyze_packet(self, packet):
        """分析数据包并提取信息"""
        packet_info = {
            'timestamp': time.time(),
            'length': len(packet),
            'protocol': 'Unknown'
        }
        
        if IP in packet:
            packet_info['protocol'] = 'IP'
            packet_info['src'] = packet[IP].src
            packet_info['dst'] = packet[IP].dst
            
            if TCP in packet:
                packet_info['protocol'] = 'TCP'
                packet_info['sport'] = packet[TCP].sport
                packet_info['dport'] = packet[TCP].dport
                packet_info['flags'] = str(packet[TCP].flags)
            elif UDP in packet:
                packet_info['protocol'] = 'UDP'
                packet_info['sport'] = packet[UDP].sport
                packet_info['dport'] = packet[UDP].dport
            elif ICMP in packet:
                packet_info['protocol'] = 'ICMP'
                packet_info['type'] = packet[ICMP].type
                packet_info['code'] = packet[ICMP].code
        
        return packet_info
    
    def update_flow_data(self, packet_info):
        """更新流量数据"""
        flow_key = None
        
        if 'src' in packet_info and 'dst' in packet_info:
            if 'sport' in packet_info and 'dport' in packet_info:
                flow_key = f"{packet_info['src']}:{packet_info['sport']}->{packet_info['dst']}:{packet_info['dport']}"
            else:
                flow_key = f"{packet_info['src']}->{packet_info['dst']}"
        
        if flow_key:
            if flow_key not in self.flow_data:
                self.flow_data[flow_key] = {
                    'count': 0,
                    'bytes': 0,
                    'protocol': packet_info['protocol'],
                    'first_seen': packet_info['timestamp'],
                    'last_seen': packet_info['timestamp']
                }
            
            self.flow_data[flow_key]['count'] += 1
            self.flow_data[flow_key]['bytes'] += packet_info['length']
            self.flow_data[flow_key]['last_seen'] = packet_info['timestamp']
    
    def get_statistics(self):
        """获取网络流量统计信息"""
        stats = {
            'packet_count': self.packet_count,
            'flow_count': len(self.flow_data),
            'active_flows': 0,
            'total_bytes': 0
        }
        
        current_time = time.time()
        for flow, data in self.flow_data.items():
            stats['total_bytes'] += data['bytes']
            # 检查是否为活跃流（最近10秒内有活动）
            if current_time - data['last_seen'] < 10:
                stats['active_flows'] += 1
        
        return stats
    
    def get_recent_packets(self, limit=100):
        """获取最近的数据包"""
        return self.packet_history[-limit:]
    
    def get_top_flows(self, limit=10):
        """获取流量最大的前N个流"""
        sorted_flows = sorted(
            self.flow_data.items(),
            key=lambda x: x[1]['bytes'],
            reverse=True
        )
        return sorted_flows[:limit]

# 示例用法
if __name__ == "__main__":
    monitor = NetworkMonitor()
    print("开始网络流量监控...")
    monitor.start_monitoring()
    
    try:
        while True:
            time.sleep(5)
            stats = monitor.get_statistics()
            print(f"统计信息: 数据包数={stats['packet_count']}, 流数={stats['flow_count']}, 活跃流={stats['active_flows']}")
            
            top_flows = monitor.get_top_flows(5)
            print("流量最大的5个流:")
            for flow, data in top_flows:
                print(f"  {flow}: {data['bytes']} bytes, {data['count']} packets")
    except KeyboardInterrupt:
        print("\n停止监控...")
        monitor.stop_monitoring()