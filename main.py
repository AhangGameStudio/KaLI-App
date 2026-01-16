import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import random
import threading
import time
from data import KALI_TOOLS

# Matrix Theme Colors
COLOR_BG = "#000000"
COLOR_FG = "#00FF41"  # Matrix Green
COLOR_HL = "#008F11"  # Darker Green
COLOR_TXT = "#003B00" # Very Dark Green for backgrounds
FONT_MAIN = ("Consolas", 10)
FONT_HEADER = ("Consolas", 14, "bold")
FONT_TITLE = ("Consolas", 20, "bold")

class MatrixButton(tk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            bg=COLOR_BG, 
            fg=COLOR_FG, 
            activebackground=COLOR_HL, 
            activeforeground=COLOR_BG,
            bd=1,
            relief="solid",
            font=FONT_MAIN
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['bg'] = COLOR_HL
        self['fg'] = COLOR_BG

    def on_leave(self, e):
        self['bg'] = COLOR_BG
        self['fg'] = COLOR_FG

class MatrixKaliApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KALI LINUX MATRIX LAUNCHER")
        self.root.geometry("1000x700")
        self.root.configure(bg=COLOR_BG)
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", 
                        background=COLOR_BG, 
                        foreground=COLOR_FG, 
                        fieldbackground=COLOR_BG,
                        font=FONT_MAIN)
        style.configure("Treeview.Heading", 
                        background=COLOR_TXT, 
                        foreground=COLOR_FG, 
                        font=FONT_HEADER)
        style.map("Treeview", 
                  background=[('selected', COLOR_HL)], 
                  foreground=[('selected', COLOR_BG)])

        # Setup UI
        self.setup_header()
        self.setup_main_area()
        self.setup_footer()
        
        # Select first category by default
        self.cat_listbox.select_set(0)
        self.on_category_select(None)

    def setup_header(self):
        header_frame = tk.Frame(self.root, bg=COLOR_BG, bd=2, relief="solid")
        header_frame.pack(fill="x", padx=5, pady=5)
        
        title_label = tk.Label(header_frame, text="SYSTEM STATUS: ONLINE // USER: NEO", 
                               bg=COLOR_BG, fg=COLOR_FG, font=FONT_TITLE)
        title_label.pack(pady=10)
        
        self.matrix_canvas = tk.Canvas(header_frame, height=40, bg=COLOR_BG, highlightthickness=0)
        self.matrix_canvas.pack(fill="x")
        self.start_matrix_effect()

    def setup_main_area(self):
        main_frame = tk.Frame(self.root, bg=COLOR_BG)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Left: Categories
        left_frame = tk.Frame(main_frame, bg=COLOR_BG, width=250)
        left_frame.pack(side="left", fill="y", padx=(0, 5))
        
        tk.Label(left_frame, text="[ CATEGORIES ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(fill="x", pady=5)
        
        self.cat_listbox = tk.Listbox(left_frame, bg=COLOR_BG, fg=COLOR_FG, 
                                      selectbackground=COLOR_HL, selectforeground=COLOR_BG,
                                      font=FONT_MAIN, bd=1, relief="solid")
        self.cat_listbox.pack(fill="both", expand=True)
        self.cat_listbox.bind("<<ListboxSelect>>", self.on_category_select)
        
        for cat in KALI_TOOLS.keys():
            self.cat_listbox.insert(tk.END, cat)

        # Middle: Tools List
        middle_frame = tk.Frame(main_frame, bg=COLOR_BG)
        middle_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(middle_frame, text="[ TOOLS ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(fill="x", pady=5)
        
        columns = ("name", "cmd")
        self.tool_tree = ttk.Treeview(middle_frame, columns=columns, show="headings")
        self.tool_tree.heading("name", text="TOOL NAME")
        self.tool_tree.heading("cmd", text="COMMAND")
        self.tool_tree.column("name", width=150)
        self.tool_tree.column("cmd", width=100)
        self.tool_tree.pack(fill="both", expand=True)
        self.tool_tree.bind("<<TreeviewSelect>>", self.on_tool_select)

        # Right: Details & Action
        right_frame = tk.Frame(main_frame, bg=COLOR_BG, width=300)
        right_frame.pack(side="right", fill="y", padx=(5, 0))
        
        tk.Label(right_frame, text="[ INTEL ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(fill="x", pady=5)
        
        self.desc_text = tk.Text(right_frame, bg=COLOR_BG, fg=COLOR_FG, font=FONT_MAIN, 
                                 height=15, width=30, wrap="word", bd=1, relief="solid")
        self.desc_text.pack(fill="x", pady=5)
        self.desc_text.insert("1.0", "Select a tool to analyze...")
        self.desc_text.config(state="disabled")
        
        # Execution Panel
        tk.Label(right_frame, text="[ EXECUTION ]", bg=COLOR_BG, fg=COLOR_FG, font=FONT_HEADER).pack(fill="x", pady=(20, 5))
        
        self.wsl_var = tk.BooleanVar(value=True)
        wsl_check = tk.Checkbutton(right_frame, text="USE WSL LAYER", variable=self.wsl_var, 
                                   bg=COLOR_BG, fg=COLOR_FG, selectcolor="black", activebackground=COLOR_BG, activeforeground=COLOR_FG, font=FONT_MAIN)
        wsl_check.pack(anchor="w")

        self.cmd_entry = tk.Entry(right_frame, bg=COLOR_BG, fg=COLOR_FG, insertbackground=COLOR_FG, font=FONT_MAIN, bd=1, relief="solid")
        self.cmd_entry.pack(fill="x", pady=10)
        
        self.run_btn = MatrixButton(right_frame, text="INITIATE SEQUENCE", command=self.run_tool)
        self.run_btn.pack(fill="x", pady=5)
        
        self.output_text = tk.Text(right_frame, bg=COLOR_BG, fg=COLOR_FG, font=FONT_MAIN,
                                   height=10, width=30, bd=1, relief="solid")
        self.output_text.pack(fill="both", expand=True, pady=5)

    def setup_footer(self):
        footer = tk.Label(self.root, text="CONNECTED TO MAINFRAME // SECURE CONNECTION", 
                          bg=COLOR_BG, fg=COLOR_HL, font=("Consolas", 8))
        footer.pack(side="bottom", fill="x")

    def start_matrix_effect(self):
        width = 1000
        self.drops = [random.randint(-100, 0) for _ in range(int(width/10))]
        self.update_matrix()

    def update_matrix(self):
        self.matrix_canvas.delete("all")
        for i, y in enumerate(self.drops):
            char = random.choice("0123456789ABCDEF")
            x = i * 10
            # Draw trail
            for j in range(5):
                color = "#005500" if j < 4 else "#00FF41"
                self.matrix_canvas.create_text(x, y - (j*10), text=char, fill=color, font=("Courier", 8))
            
            self.drops[i] += 10
            if self.drops[i] > 50:
                self.drops[i] = random.randint(-50, 0)
        
        self.root.after(100, self.update_matrix)

    def on_category_select(self, event):
        selection = self.cat_listbox.curselection()
        if not selection:
            return
        
        cat = self.cat_listbox.get(selection[0])
        
        # Clear tree
        for item in self.tool_tree.get_children():
            self.tool_tree.delete(item)
            
        # Populate tree
        for tool in KALI_TOOLS.get(cat, []):
            self.tool_tree.insert("", "end", values=(tool["name"], tool["cmd"]))

    def on_tool_select(self, event):
        selection = self.tool_tree.selection()
        if not selection:
            return
            
        item = self.tool_tree.item(selection[0])
        tool_name = item['values'][0]
        tool_cmd = item['values'][1]
        
        # Find description
        desc = ""
        for cat in KALI_TOOLS.values():
            for t in cat:
                if t["name"] == tool_name:
                    desc = t["desc"]
                    break
        
        self.desc_text.config(state="normal")
        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert("1.0", f"TARGET: {tool_name}\n\nPROTOCOL: {tool_cmd}\n\nDATA: {desc}")
        self.desc_text.config(state="disabled")
        
        self.cmd_entry.delete(0, tk.END)
        self.cmd_entry.insert(0, f"{tool_cmd} --help")

    def run_tool(self):
        cmd = self.cmd_entry.get()
        if not cmd:
            return
            
        use_wsl = self.wsl_var.get()
        
        self.log_output(f"> INITIALIZING {cmd}...")
        
        def execute():
            try:
                final_cmd = cmd
                if use_wsl:
                    final_cmd = f"wsl {cmd}"
                
                # Using shell=True for windows to run wsl command
                process = subprocess.Popen(final_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate()
                
                if stdout:
                    self.log_output(stdout)
                if stderr:
                    self.log_output(f"ERROR/WARNING:\n{stderr}")
                
                self.log_output("> SEQUENCE COMPLETE.")
            except Exception as e:
                self.log_output(f"> SYSTEM FAILURE: {str(e)}")

        threading.Thread(target=execute, daemon=True).start()

    def log_output(self, text):
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixKaliApp(root)
    root.mainloop()
