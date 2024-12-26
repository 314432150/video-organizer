import tkinter as tk
from tkinter import ttk
from src.core.constants import COLORS

class HeaderFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLORS['BG_COLOR'])
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self,
                        text="视频文件整理工具",
                        font=('Arial', 20, 'bold'),
                        bg=COLORS['BG_COLOR'],
                        fg=COLORS['PRIMARY_LIGHT'])
        title.pack()

        subtitle = tk.Label(self,
                          text="自动整理视频及其相关文件",
                          font=('Arial', 12),
                          bg=COLORS['BG_COLOR'],
                          fg=COLORS['GRAY'])
        subtitle.pack(pady=(5, 0))

class PathFrame(tk.Frame):
    def __init__(self, master, browse_command):
        super().__init__(master, bg=COLORS['BG_COLOR'])
        self.browse_command = browse_command
        self.paths = []  # 存储所有选择的路径
        self.create_widgets()

    def create_widgets(self):
        # 路径列表框
        list_frame = tk.Frame(self, bg=COLORS['BG_COLOR'])
        list_frame.pack(fill='both', expand=True)
        
        # 创建带滚动条的列表框
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.path_listbox = tk.Listbox(
            list_frame,
            font=('Arial', 11),
            bg=COLORS['ENTRY_BG'],
            fg=COLORS['TEXT_COLOR'],
            selectmode='extended',
            relief='flat',
            bd=1,
            height=5
        )
        self.path_listbox.pack(side='left', fill='both', expand=True)
        
        # 配置滚动条
        scrollbar.config(command=self.path_listbox.yview)
        self.path_listbox.config(yscrollcommand=scrollbar.set)
        
        # 按钮框
        button_frame = tk.Frame(self, bg=COLORS['BG_COLOR'])
        button_frame.pack(fill='x', pady=(10, 0))
        
        # 添加按钮
        self.add_button = tk.Button(
            button_frame,
            text="添加目录",
            command=self.browse_command,
            font=('Arial', 11),
            bg=COLORS['PRIMARY'],
            fg=COLORS['TEXT_COLOR'],
            activebackground=COLORS['PRIMARY_DARK'],
            activeforeground=COLORS['TEXT_COLOR'],
            width=10,
            cursor='hand2',
            relief='flat'
        )
        self.add_button.pack(side='left')
        
        # 删除按钮
        self.remove_button = tk.Button(
            button_frame,
            text="删除选中",
            command=self.remove_selected,
            font=('Arial', 11),
            bg=COLORS['PRIMARY'],
            fg=COLORS['TEXT_COLOR'],
            activebackground=COLORS['PRIMARY_DARK'],
            activeforeground=COLORS['TEXT_COLOR'],
            width=10,
            cursor='hand2',
            relief='flat'
        )
        self.remove_button.pack(side='left', padx=(10, 0))
        
        # 清空按钮
        self.clear_button = tk.Button(
            button_frame,
            text="清空列表",
            command=self.clear_paths,
            font=('Arial', 11),
            bg=COLORS['PRIMARY'],
            fg=COLORS['TEXT_COLOR'],
            activebackground=COLORS['PRIMARY_DARK'],
            activeforeground=COLORS['TEXT_COLOR'],
            width=10,
            cursor='hand2',
            relief='flat'
        )
        self.clear_button.pack(side='left', padx=(10, 0))

    def add_path(self, path):
        """添加新路径到列表"""
        if path and path not in self.paths:
            self.paths.append(path)
            self.path_listbox.insert('end', path)

    def remove_selected(self):
        """删除选中的路径"""
        selected = self.path_listbox.curselection()
        for index in reversed(selected):
            self.paths.pop(index)
            self.path_listbox.delete(index)

    def clear_paths(self):
        """清空所有路径"""
        self.paths.clear()
        self.path_listbox.delete(0, 'end')

    def get_paths(self):
        """获取所有路径"""
        return self.paths

class ActionFrame(tk.Frame):
    def __init__(self, master, start_command):
        super().__init__(master, bg=COLORS['BG_COLOR'])
        self.start_command = start_command
        self.create_widgets()

    def create_widgets(self):
        # 创建一个容器来居中按钮
        container = tk.Frame(self, bg=COLORS['BG_COLOR'])
        container.pack(expand=True, fill='both')

        self.start_button = tk.Button(
            container,
            text="开始整理",
            command=self.start_command,
            font=('Arial', 11, 'bold'),
            bg=COLORS['PRIMARY'],
            fg=COLORS['TEXT_COLOR'],
            activebackground=COLORS['PRIMARY_DARK'],
            activeforeground=COLORS['TEXT_COLOR'],
            width=15,
            height=2,  # 增加高度
            cursor='hand2',
            relief='flat'
        )
        # 使用 pack 布局，并设置 expand=True 使按钮居中
        self.start_button.pack(expand=True, pady=20)

    def set_state(self, state):
        """设置按钮状态"""
        self.start_button.config(state=state)

class ProgressFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLORS['BG_COLOR'])
        self.create_widgets()

    def create_widgets(self):
        # 状态标签
        self.status_label = tk.Label(
            self,
            text="准备就绪",
            font=('Arial', 11),
            bg=COLORS['BG_COLOR'],
            fg=COLORS['TEXT_COLOR']
        )
        self.status_label.pack(fill='x', pady=(0, 10))

        # 进度条
        self.progressbar = ttk.Progressbar(
            self,
            style='Custom.TProgressbar',
            mode='determinate'
        )
        self.progressbar.pack(fill='x')

    def update_status(self, message):
        """更新状态信息"""
        self.status_label.config(text=message)
        self.update()

    def update_progress(self, current, total):
        """更新进度条"""
        if total > 0:
            progress = (current / total) * 100
            self.progressbar['value'] = progress
            self.update_status(f"处理进度：{current}/{total}")
        self.update()

    def reset(self):
        """重置进度显示"""
        self.progressbar['value'] = 0
        self.update_status("准备就绪")
        self.update()

class SettingsFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLORS['BG_COLOR'])
        self.create_widgets()

    def create_widgets(self):
        # 并发设置
        concurrency_frame = tk.Frame(self, bg=COLORS['BG_COLOR'])
        concurrency_frame.pack(fill='x')
        
        tk.Label(
            concurrency_frame,
            text="并发数：",
            font=('Arial', 11),
            bg=COLORS['BG_COLOR'],
            fg=COLORS['TEXT_COLOR']
        ).pack(side='left')
        
        self.concurrency_var = tk.StringVar(value="3")
        spinbox = tk.Spinbox(
            concurrency_frame,
            from_=1,
            to=10,
            width=5,
            textvariable=self.concurrency_var,
            font=('Arial', 11),
            bg=COLORS['ENTRY_BG'],
            fg=COLORS['TEXT_COLOR'],
            buttonbackground=COLORS['PRIMARY'],
            relief='flat'
        )
        spinbox.pack(side='left', padx=(5, 0))

    def get_concurrency(self):
        """获取并发数设置"""
        try:
            return int(self.concurrency_var.get())
        except ValueError:
            return 3 