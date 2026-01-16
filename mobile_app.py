import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex, platform
from kivy.core.clipboard import Clipboard
from kivy.uix.popup import Popup
import random
import os
from data import KALI_TOOLS
from core.network import network_security
from core.wireless import scanner, cracker

# 配置 Kivy
kivy.require('2.1.0')

# 颜色定义
COLOR_BG = "#000000"
COLOR_FG = "#00FF41"  # Matrix Green
COLOR_HL = "#008F11"  # Darker Green
COLOR_TXT = "#E0FFE0" # Light Green for text

# 字体处理
def get_font_name():
    """尝试获取系统中文字体"""
    if platform == 'win':
        # Windows 下尝试使用微软雅黑
        font_path = os.path.join(os.environ['WINDIR'], 'Fonts', 'msyh.ttc')
        if os.path.exists(font_path):
            return font_path
    elif platform == 'android':
        return 'DroidSansFallback.ttf'
    # Linux/Mac 或其他情况使用默认
    return 'Roboto'

FONT_NAME = get_font_name()

class MatrixBackground(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drops = []
        with self.canvas.before:
            Color(0, 0, 0, 1)  # Black background
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # 数字雨效果只在主页启用，避免性能消耗
        self.is_raining = False
        self.canvas_labels = []

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class MatrixButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 1)
        self.color = get_color_from_hex(COLOR_FG)
        self.font_name = FONT_NAME
        self.font_size = '18sp'
        self.bold = True
        self.background_normal = ''
        self.background_down = ''
        self.border_color = get_color_from_hex(COLOR_FG)
        
    def on_press(self):
        self.color = get_color_from_hex(COLOR_BG)
        self.background_color = get_color_from_hex(COLOR_FG)

    def on_release(self):
        self.color = get_color_from_hex(COLOR_FG)
        self.background_color = (0, 0, 0, 1)

class MatrixLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = get_color_from_hex(COLOR_FG)
        self.font_name = FONT_NAME

# --- Screens ---

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # 标题
        title = MatrixLabel(text="KALI LINUX\nMATRIX SYSTEM", 
                            font_size='32sp', 
                            halign='center',
                            size_hint=(1, 0.4))
        layout.add_widget(title)
        
        # 进入按钮
        btn = MatrixButton(text="[ 进入系统 / ENTER ]", size_hint=(1, 0.15))
        btn.bind(on_release=self.go_categories)
        layout.add_widget(btn)
        
        # 网络安全监控按钮
        security_btn = MatrixButton(text="[ 网络安全监控 ]", size_hint=(1, 0.15))
        security_btn.bind(on_release=self.go_security)
        layout.add_widget(security_btn)
        
        # WIFI扫描按钮
        wifi_btn = MatrixButton(text="[ WIFI扫描与破解 ]", size_hint=(1, 0.15))
        wifi_btn.bind(on_release=self.go_wifi)
        layout.add_widget(wifi_btn)
        
        # 漏洞挖掘按钮
        vuln_btn = MatrixButton(text="[ 漏洞挖掘工具 ]", size_hint=(1, 0.15))
        vuln_btn.bind(on_release=self.go_vulnerability)
        layout.add_widget(vuln_btn)
        
        # 底部留白
        layout.add_widget(Label(size_hint=(1, 0.1)))
        
        self.add_widget(layout)

    def go_categories(self, instance):
        self.manager.current = 'categories'
    
    def go_security(self, instance):
        self.manager.current = 'security'
    
    def go_wifi(self, instance):
        self.manager.current = 'wifi'
    
    def go_vulnerability(self, instance):
        self.manager.current = 'vulnerability'

class CategoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical')
        
        # Header
        header = MatrixLabel(text="[ 工具分类 ]", size_hint=(1, 0.1), font_size='20sp')
        root.add_widget(header)
        
        # List
        scroll = ScrollView()
        grid = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=10)
        grid.bind(minimum_height=grid.setter('height'))
        
        for category in KALI_TOOLS.keys():
            btn = MatrixButton(text=category, size_hint_y=None, height=60)
            btn.bind(on_release=lambda x, cat=category: self.open_category(cat))
            grid.add_widget(btn)
            
        scroll.add_widget(grid)
        root.add_widget(scroll)
        
        # Back Button
        back = MatrixButton(text="< 返回 / BACK", size_hint=(1, 0.1))
        back.bind(on_release=self.go_back)
        root.add_widget(back)
        
        self.add_widget(root)

    def open_category(self, category):
        # 传递数据给下一个屏幕
        tool_screen = self.manager.get_screen('tools')
        tool_screen.update_tools(category)
        self.manager.current = 'tools'

    def go_back(self, instance):
        self.manager.current = 'home'

class WifiScannerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(self.layout)
        
        # 标题
        title = MatrixLabel(text="WIFI扫描与破解", font_size='24sp', size_hint=(1, 0.15), bold=True, halign='center')
        self.layout.add_widget(title)
        
        # 接口选择
        interface_frame = BoxLayout(orientation='vertical', size_hint=(1, 0.2), spacing=5)
        interface_label = MatrixLabel(text="网络接口:", font_size='18sp', size_hint=(1, 0.5))
        interface_frame.add_widget(interface_label)
        
        self.interface_list = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.interface_list.bind(minimum_height=self.interface_list.setter('height'))
        
        interface_scroll = ScrollView(size_hint=(1, 0.5))
        interface_scroll.add_widget(self.interface_list)
        interface_frame.add_widget(interface_scroll)
        self.layout.add_widget(interface_frame)
        
        # 扫描结果
        result_frame = BoxLayout(orientation='vertical', size_hint=(1, 0.4), spacing=5)
        result_label = MatrixLabel(text="扫描结果:", font_size='18sp', size_hint=(1, 0.2))
        result_frame.add_widget(result_label)
        
        result_scroll = ScrollView(size_hint=(1, 0.8))
        self.result_list = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=5)
        self.result_list.bind(minimum_height=self.result_list.setter('height'))
        result_scroll.add_widget(self.result_list)
        result_frame.add_widget(result_scroll)
        self.layout.add_widget(result_frame)
        
        # 控制按钮
        control_frame = BoxLayout(size_hint=(1, 0.15), spacing=10)
        self.scan_btn = MatrixButton(text="开始扫描")
        self.scan_btn.bind(on_release=self.start_scan)
        control_frame.add_widget(self.scan_btn)
        
        self.crack_btn = MatrixButton(text="尝试破解", disabled=True)
        self.crack_btn.bind(on_release=self.start_crack)
        control_frame.add_widget(self.crack_btn)
        self.layout.add_widget(control_frame)
        
        # 底部按钮
        bottom_frame = BoxLayout(size_hint=(1, 0.1), spacing=10)
        refresh_btn = MatrixButton(text="刷新接口")
        refresh_btn.bind(on_release=self.refresh_interfaces)
        bottom_frame.add_widget(refresh_btn)
        
        back_btn = MatrixButton(text="< 返回 / BACK")
        back_btn.bind(on_release=self.go_back)
        bottom_frame.add_widget(back_btn)
        self.layout.add_widget(bottom_frame)
        
        # 初始化
        self.selected_interface = None
        self.selected_network = None
        self.wifi_scanner = scanner.WifiScanner()
        self.wifi_cracker = cracker.WifiCracker()
        
        # 刷新接口列表
        self.refresh_interfaces(None)
    
    def refresh_interfaces(self, instance):
        """刷新网络接口列表"""
        self.interface_list.clear_widgets()
        
        try:
            interfaces = self.wifi_scanner.get_interface_info()
            if interfaces:
                for interface in interfaces:
                    name = interface.get('name', 'Unknown')
                    state = interface.get('state', 'Unknown')
                    btn = MatrixButton(text=f"{name} ({state})", size_hint_y=None, height=50)
                    btn.bind(on_release=lambda x, iface=name: self.select_interface(iface))
                    self.interface_list.add_widget(btn)
            else:
                self.interface_list.add_widget(MatrixLabel(text="未检测到网络接口", size_hint_y=None, height=50))
        except Exception as e:
            self.interface_list.add_widget(MatrixLabel(text=f"获取接口失败: {str(e)}", size_hint_y=None, height=50))
    
    def select_interface(self, interface):
        """选择网络接口"""
        self.selected_interface = interface
        self.show_popup("提示", f"已选择接口: {interface}")
    
    def start_scan(self, instance):
        """开始WIFI扫描"""
        def execute_scan():
            try:
                self.scan_btn.disabled = True
                self.result_list.clear_widgets()
                self.result_list.add_widget(MatrixLabel(text="正在扫描网络...", size_hint_y=None, height=50))
                
                # 执行扫描
                results = self.wifi_scanner.scan(self.selected_interface)
                
                # 显示结果
                self.result_list.clear_widgets()
                
                if results:
                    for network in results:
                        ssid = network.get('ssid', 'Unknown')
                        bssid = network.get('bssid', 'N/A')
                        signal = network.get('signal', 'N/A')
                        channel = network.get('channel', 'N/A')
                        encryption = network.get('encryption', 'N/A')
                        
                        network_info = f"SSID: {ssid}\nBSSID: {bssid}\nSignal: {signal}\nChannel: {channel}\nEncryption: {encryption}"
                        
                        btn = MatrixButton(text=ssid, size_hint_y=None, height=80)
                        btn.bind(on_release=lambda x, net=network: self.select_network(net))
                        self.result_list.add_widget(btn)
                else:
                    self.result_list.add_widget(MatrixLabel(text="未发现网络", size_hint_y=None, height=50))
                
                self.scan_btn.disabled = False
            except Exception as e:
                self.result_list.clear_widgets()
                self.result_list.add_widget(MatrixLabel(text=f"扫描失败: {str(e)}", size_hint_y=None, height=50))
                self.scan_btn.disabled = False
        
        import threading
        threading.Thread(target=execute_scan, daemon=True).start()
    
    def select_network(self, network):
        """选择网络"""
        self.selected_network = network
        self.crack_btn.disabled = False
        
        ssid = network.get('ssid', 'Unknown')
        self.show_popup("提示", f"已选择网络: {ssid}")
    
    def start_crack(self, instance):
        """开始破解"""
        if not self.selected_network:
            self.show_popup("错误", "请先选择一个网络")
            return
        
        def execute_crack():
            try:
                self.crack_btn.disabled = True
                self.result_list.clear_widgets()
                self.result_list.add_widget(MatrixLabel(text="正在尝试破解...", size_hint_y=None, height=50))
                
                # 执行破解
                result = self.wifi_cracker.crack(self.selected_network, self.selected_interface)
                
                # 显示结果
                self.result_list.clear_widgets()
                
                if result.get('success'):
                    password = result.get('password', 'Unknown')
                    self.result_list.add_widget(MatrixLabel(text=f"破解成功!\n密码: {password}", size_hint_y=None, height=100))
                else:
                    error = result.get('error', '未知错误')
                    self.result_list.add_widget(MatrixLabel(text=f"破解失败: {error}", size_hint_y=None, height=100))
                
                self.crack_btn.disabled = False
            except Exception as e:
                self.result_list.clear_widgets()
                self.result_list.add_widget(MatrixLabel(text=f"破解失败: {str(e)}", size_hint_y=None, height=50))
                self.crack_btn.disabled = False
        
        import threading
        threading.Thread(target=execute_crack, daemon=True).start()
    
    def show_popup(self, title, content):
        popup = Popup(title=title,
                      content=Label(text=content, font_name=FONT_NAME),
                      size_hint=(0.8, 0.4),
                      title_font=FONT_NAME)
        popup.open()
    
    def go_back(self, instance):
        self.manager.current = 'home'

class VulnerabilityMiningScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(self.layout)
        
        # 标题
        title = MatrixLabel(text="漏洞挖掘工具", font_size='24sp', size_hint=(1, 0.15), bold=True, halign='center')
        self.layout.add_widget(title)
        
        # 应用路径输入
        path_frame = BoxLayout(orientation='vertical', size_hint=(1, 0.2), spacing=5)
        path_label = MatrixLabel(text="应用路径:", font_size='18sp', size_hint=(1, 0.4))
        path_frame.add_widget(path_label)
        
        self.path_input = kivy.uix.textinput.TextInput(
            text='.', 
            size_hint=(1, 0.6),
            background_color=(0, 0, 0, 1),
            foreground_color=get_color_from_hex(COLOR_FG),
            font_name=FONT_NAME,
            font_size='16sp'
        )
        path_frame.add_widget(self.path_input)
        self.layout.add_widget(path_frame)
        
        # 分析结果
        result_frame = BoxLayout(orientation='vertical', size_hint=(1, 0.4), spacing=5)
        result_label = MatrixLabel(text="分析结果:", font_size='18sp', size_hint=(1, 0.2))
        result_frame.add_widget(result_label)
        
        result_scroll = ScrollView(size_hint=(1, 0.8))
        self.result_text = MatrixLabel(text="分析结果将显示在这里...", size_hint_y=None, halign='left', valign='top')
        self.result_text.bind(texture_size=self.result_text.setter('size'))
        self.result_text.bind(width=lambda *x: self.result_text.setter('text_size')(self.result_text, (self.result_text.width, None)))
        result_scroll.add_widget(self.result_text)
        result_frame.add_widget(result_scroll)
        self.layout.add_widget(result_frame)
        
        # 控制按钮
        control_frame = BoxLayout(size_hint=(1, 0.15), spacing=10)
        self.analyze_btn = MatrixButton(text="开始分析")
        self.analyze_btn.bind(on_release=self.start_analysis)
        control_frame.add_widget(self.analyze_btn)
        
        self.report_btn = MatrixButton(text="生成报告", disabled=True)
        self.report_btn.bind(on_release=self.generate_report)
        control_frame.add_widget(self.report_btn)
        self.layout.add_widget(control_frame)
        
        # 底部按钮
        bottom_frame = BoxLayout(size_hint=(1, 0.1), spacing=10)
        self.clear_btn = MatrixButton(text="清空结果")
        self.clear_btn.bind(on_release=self.clear_results)
        bottom_frame.add_widget(self.clear_btn)
        
        back_btn = MatrixButton(text="< 返回 / BACK")
        back_btn.bind(on_release=self.go_back)
        bottom_frame.add_widget(back_btn)
        self.layout.add_widget(bottom_frame)
        
        # 初始化
        from core.security import VulnerabilityMiner
        self.vuln_miner = VulnerabilityMiner()
        self.analysis_results = None
    
    def start_analysis(self, instance):
        """开始漏洞分析"""
        def execute_analysis():
            try:
                self.analyze_btn.disabled = True
                self.result_text.text = "正在分析应用程序...\n\n"
                
                # 获取应用路径
                app_path = self.path_input.text
                
                # 执行分析
                self.analysis_results = self.vuln_miner.analyze_app(app_path)
                
                # 显示结果摘要
                summary = self.analysis_results['summary']
                result_text = f"分析完成！\n\n"
                result_text += f"发现漏洞总数: {summary['total']}\n"
                result_text += f"严重程度分布:\n"
                result_text += f"  严重: {summary['critical']}\n"
                result_text += f"  高: {summary['high']}\n"
                result_text += f"  中: {summary['medium']}\n"
                result_text += f"  低: {summary['low']}\n\n"
                
                # 显示详细漏洞
                vulnerabilities = self.analysis_results['vulnerabilities']
                if vulnerabilities:
                    result_text += "发现的漏洞:\n"
                    result_text += "----------------\n"
                    for i, vuln in enumerate(vulnerabilities, 1):
                        result_text += f"{i}. [{vuln['severity'].upper()}] {vuln['description']}\n"
                        result_text += f"   位置: {vuln.get('location', 'Unknown')}\n"
                        if 'line' in vuln:
                            result_text += f"   行号: {vuln['line']}\n"
                        result_text += f"   修复建议: {vuln.get('fix', 'Unknown')}\n\n"
                else:
                    result_text += "未发现漏洞！\n"
                
                self.result_text.text = result_text
                self.report_btn.disabled = False
                
            except Exception as e:
                self.result_text.text = f"分析失败: {str(e)}\n\n"
            finally:
                self.analyze_btn.disabled = False
        
        import threading
        threading.Thread(target=execute_analysis, daemon=True).start()
    
    def generate_report(self, instance):
        """生成分析报告"""
        if not self.analysis_results:
            self.show_popup("错误", "请先执行分析")
            return
        
        try:
            report = self.vuln_miner.generate_report(self.analysis_results)
            
            # 保存报告到文件
            import os
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = f"vulnerability_report_{timestamp}.txt"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            self.show_popup("成功", f"报告已生成:\n{report_file}")
            
        except Exception as e:
            self.show_popup("错误", f"生成报告失败: {str(e)}")
    
    def clear_results(self, instance):
        """清空分析结果"""
        self.result_text.text = "分析结果将显示在这里..."
        self.analysis_results = None
        self.report_btn.disabled = True
    
    def show_popup(self, title, content):
        popup = Popup(title=title,
                      content=Label(text=content, font_name=FONT_NAME),
                      size_hint=(0.8, 0.4),
                      title_font=FONT_NAME)
        popup.open()
    
    def go_back(self, instance):
        self.manager.current = 'home'

class ToolListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)
        
        self.header = MatrixLabel(text="[ 工具列表 ]", size_hint=(1, 0.1), font_size='20sp')
        self.layout.add_widget(self.header)
        
        self.scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=10)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)
        self.layout.add_widget(self.scroll)
        
        back = MatrixButton(text="< 返回 / BACK", size_hint=(1, 0.1))
        back.bind(on_release=self.go_back)
        self.layout.add_widget(back)

    def update_tools(self, category):
        self.header.text = f"[ {category.split('(')[0]} ]" # 简化标题
        self.grid.clear_widgets()
        
        tools = KALI_TOOLS.get(category, [])
        for tool in tools:
            btn = MatrixButton(text=tool['name'], size_hint_y=None, height=60)
            btn.bind(on_release=lambda x, t=tool: self.open_tool(t))
            self.grid.add_widget(btn)

    def open_tool(self, tool):
        detail_screen = self.manager.get_screen('detail')
        detail_screen.update_detail(tool)
        self.manager.current = 'detail'

    def go_back(self, instance):
        self.manager.current = 'categories'

class ToolDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(self.layout)
        
        self.tool_name = MatrixLabel(text="", font_size='24sp', size_hint=(1, 0.15), bold=True)
        self.layout.add_widget(self.tool_name)
        
        self.tool_cmd = MatrixLabel(text="", font_size='18sp', size_hint=(1, 0.1))
        self.layout.add_widget(self.tool_cmd)
        
        # 描述框
        desc_scroll = ScrollView(size_hint=(1, 0.45))
        self.tool_desc = MatrixLabel(text="", size_hint_y=None, halign='left', valign='top')
        self.tool_desc.bind(texture_size=self.tool_desc.setter('size'))
        self.tool_desc.bind(width=lambda *x: self.tool_desc.setter('text_size')(self.tool_desc, (self.tool_desc.width, None)))
        desc_scroll.add_widget(self.tool_desc)
        self.layout.add_widget(desc_scroll)
        
        # 按钮区
        btn_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        
        copy_btn = MatrixButton(text="复制命令")
        copy_btn.bind(on_release=self.copy_command)
        btn_layout.add_widget(copy_btn)
        
        # 只有在 Android 上才显示运行（虽然这里无法真正运行，但可以做个样子）
        # 或者显示“执行说明”
        run_btn = MatrixButton(text="尝试运行")
        run_btn.bind(on_release=self.run_command)
        btn_layout.add_widget(run_btn)
        
        self.layout.add_widget(btn_layout)
        
        back = MatrixButton(text="< 返回 / BACK", size_hint=(1, 0.1))
        back.bind(on_release=self.go_back)
        self.layout.add_widget(back)
        
        self.current_cmd = ""

    def update_detail(self, tool):
        self.tool_name.text = tool['name']
        self.current_cmd = tool['cmd']
        self.tool_cmd.text = f"命令: {self.current_cmd}"
        self.tool_desc.text = tool['desc']

    def copy_command(self, instance):
        Clipboard.copy(self.current_cmd)
        self.show_popup("提示", "命令已复制到剪贴板")

    def run_command(self, instance):
        # 移动端通常无法直接运行这些命令，除非在 Termux 环境
        msg = "此功能需要 Root 权限或 Termux 环境。\n命令已复制，请在终端中粘贴运行。"
        Clipboard.copy(self.current_cmd)
        self.show_popup("运行说明", msg)

    def show_popup(self, title, content):
        popup = Popup(title=title,
                      content=Label(text=content, font_name=FONT_NAME),
                      size_hint=(0.8, 0.4),
                      title_font=FONT_NAME)
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'tools'

class SecurityScreen(Screen):
    # Define status_var as a class property
    status_var = kivy.properties.StringProperty("INITIALIZING")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(self.layout)
        
        # 标题
        title = MatrixLabel(text="网络安全监控", font_size='24sp', size_hint=(1, 0.15), bold=True, halign='center')
        self.layout.add_widget(title)
        
        # 安全状态
        status_frame = BoxLayout(orientation='vertical', size_hint=(1, 0.2), spacing=5)
        status_label = MatrixLabel(text="安全状态:", font_size='18sp', size_hint=(1, 0.5))
        status_frame.add_widget(status_label)
        
        status_value = MatrixLabel(textvariable=self.status_var, font_size='16sp', size_hint=(1, 0.5))
        status_frame.add_widget(status_value)
        self.layout.add_widget(status_frame)
        
        # 控制按钮
        control_frame = BoxLayout(size_hint=(1, 0.15), spacing=10)
        self.start_btn = MatrixButton(text="开始监控")
        self.start_btn.bind(on_release=self.start_monitoring)
        control_frame.add_widget(self.start_btn)
        
        self.stop_btn = MatrixButton(text="停止监控", disabled=True)
        self.stop_btn.bind(on_release=self.stop_monitoring)
        control_frame.add_widget(self.stop_btn)
        self.layout.add_widget(control_frame)
        
        # 网络统计
        stats_frame = BoxLayout(orientation='vertical', size_hint=(1, 0.3), spacing=5)
        stats_label = MatrixLabel(text="网络统计:", font_size='18sp', size_hint=(1, 0.3))
        stats_frame.add_widget(stats_label)
        
        self.stats_text = MatrixLabel(text="初始化中...", size_hint_y=None, halign='left', valign='top')
        self.stats_text.bind(texture_size=self.stats_text.setter('size'))
        self.stats_text.bind(width=lambda *x: self.stats_text.setter('text_size')(self.stats_text, (self.stats_text.width, None)))
        
        stats_scroll = ScrollView(size_hint=(1, 0.7))
        stats_scroll.add_widget(self.stats_text)
        stats_frame.add_widget(stats_scroll)
        self.layout.add_widget(stats_frame)
        
        # 底部按钮
        bottom_frame = BoxLayout(size_hint=(1, 0.15), spacing=10)
        self.update_btn = MatrixButton(text="更新状态")
        self.update_btn.bind(on_release=self.update_status)
        bottom_frame.add_widget(self.update_btn)
        
        back_btn = MatrixButton(text="返回")
        back_btn.bind(on_release=self.go_back)
        bottom_frame.add_widget(back_btn)
        self.layout.add_widget(bottom_frame)
        
        # 初始化安全模块
        try:
            network_security.initialize()
            self.status_var = "READY"
        except Exception as e:
            self.status_var = f"ERROR: {str(e)}"

    def start_monitoring(self, instance):
        try:
            network_security.start_monitoring()
            self.status_var = "MONITORING"
            self.start_btn.disabled = True
            self.stop_btn.disabled = False
            self.show_popup("提示", "网络安全监控已启动")
        except Exception as e:
            self.show_popup("错误", f"启动监控失败: {str(e)}")

    def stop_monitoring(self, instance):
        try:
            network_security.stop_monitoring()
            self.status_var = "STOPPED"
            self.start_btn.disabled = False
            self.stop_btn.disabled = True
            self.show_popup("提示", "网络安全监控已停止")
        except Exception as e:
            self.show_popup("错误", f"停止监控失败: {str(e)}")

    def update_status(self, instance):
        try:
            status = network_security.get_security_status()
            stats = status['network']
            
            stats_text = f"状态: {status['status']}\n"
            stats_text += f"数据包数: {stats['packet_count']}\n"
            stats_text += f"流数: {stats['flow_count']}\n"
            stats_text += f"活跃流: {stats['active_flows']}\n"
            stats_text += f"阻止IP数: {len(status['security']['blocked_ip_list'])}\n"
            
            self.stats_text.text = stats_text
        except Exception as e:
            self.stats_text.text = f"更新状态失败: {str(e)}"

    def show_popup(self, title, content):
        popup = Popup(title=title,
                      content=Label(text=content, font_name=FONT_NAME),
                      size_hint=(0.8, 0.4),
                      title_font=FONT_NAME)
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'home'

class MatrixApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(CategoryScreen(name='categories'))
        sm.add_widget(ToolListScreen(name='tools'))
        sm.add_widget(ToolDetailScreen(name='detail'))
        sm.add_widget(SecurityScreen(name='security'))
        sm.add_widget(WifiScannerScreen(name='wifi'))
        sm.add_widget(VulnerabilityMiningScreen(name='vulnerability'))
        return sm

if __name__ == '__main__':
    MatrixApp().run()
