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
        
        # 底部留白
        layout.add_widget(Label(size_hint=(1, 0.45)))
        
        self.add_widget(layout)

    def go_categories(self, instance):
        self.manager.current = 'categories'

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

class MatrixApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(CategoryScreen(name='categories'))
        sm.add_widget(ToolListScreen(name='tools'))
        sm.add_widget(ToolDetailScreen(name='detail'))
        return sm

if __name__ == '__main__':
    MatrixApp().run()
