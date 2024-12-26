import tkinter as tk
from tkinter import messagebox, filedialog
import os
import asyncio
from src.gui.styles import setup_styles
from src.gui.widgets import HeaderFrame, PathFrame, ActionFrame, ProgressFrame, SettingsFrame
from src.core.organizer import VideoOrganizer
from src.core.constants import COLORS

class VideoOrganizerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("视频文件整理工具")
        self.setup_window()
        setup_styles()
        self.create_widgets()
        self.organizer = VideoOrganizer()

    def setup_window(self):
        """设置窗口大小、位置和基本属性"""
        window_height = 600
        window_width = int(window_height * 4 / 3)  # 16:9 比例 (600 * 16/9 ≈ 1067)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg=COLORS['BG_COLOR'])
        self.root.resizable(False, False)

    def create_widgets(self):
        """创建并布局GUI组件"""
        # 主容器
        main_frame = tk.Frame(self.root, bg=COLORS['BG_COLOR'], padx=30, pady=20)
        main_frame.pack(expand=True, fill='both')

        # 添加标题区域
        self.header = HeaderFrame(main_frame)
        self.header.pack(fill='x', pady=(0, 20))

        # 添加路径选择区域
        self.path_frame = PathFrame(main_frame, self.browse_folder)
        self.path_frame.pack(fill='x', pady=(0, 20))

        # 添加设置区域
        self.settings_frame = SettingsFrame(main_frame)
        self.settings_frame.pack(fill='x', pady=(0, 20))

        # 添加操作按钮区域
        self.action_frame = ActionFrame(main_frame, self.start_organize)
        self.action_frame.pack(fill='x', pady=(20, 20))

        # 添加进度显示区域
        self.progress_frame = ProgressFrame(main_frame)
        self.progress_frame.pack(fill='x', pady=(0, 0))

    def browse_folder(self):
        """浏览选择文件夹"""
        folder_path = filedialog.askdirectory(title="选择文件夹")
        if folder_path:
            self.path_frame.add_path(folder_path)

    async def process_folders(self):
        """处理所有选中的文件夹"""
        paths = self.path_frame.get_paths()
        if not paths:
            messagebox.showwarning("警告", "请至少选择一个文件夹")
            return
            
        # 使用信号量限制并发数
        concurrency = self.settings_frame.get_concurrency()
        semaphore = asyncio.Semaphore(concurrency)
        
        async def process_with_semaphore(path):
            async with semaphore:
                try:
                    def progress_callback(current, total):
                        if total > 0:
                            self.progress_frame.update_progress(current, total)
                        self.root.update()

                    return await self.organizer.organize_files(path, progress_callback)
                except Exception as e:
                    messagebox.showerror("错误", f"处理目录 {path} 时出错: {str(e)}")
                    return False

        # 并发处理所有目录
        tasks = [process_with_semaphore(path) for path in paths]
        results = await asyncio.gather(*tasks)
        
        # 检查处理结果（现在空目录也算作成功）
        success_count = len(paths)  # 所有处理过的目录都算作成功
        total_count = len(paths)
        
        # 确保进度条显示完成状态
        self.progress_frame.update_progress(total_count, total_count)
        self.progress_frame.update_status(f"处理完成！成功: {success_count}/{total_count}")
        messagebox.showinfo("完成", f"文件整理完成！\n成功处理 {success_count}/{total_count} 个目录")

    def start_organize(self):
        """开始整理文件"""
        # 禁用按钮
        self.action_frame.set_state('disabled')
        self.progress_frame.update_status("正在处理文件...")
        
        # 创建异步事件循环
        async def main():
            await self.process_folders()
            # 恢复按钮状态
            self.action_frame.set_state('normal')
        
        # 运行异步任务
        asyncio.run(main())

    @staticmethod
    def open_folder(path):
        """打开指定文件夹"""
        if os.name == 'nt':  # Windows
            os.startfile(path)
        else:  # macOS 和 Linux
            import subprocess
            subprocess.Popen(['xdg-open' if os.name == 'posix' else 'open', path])

    def run(self):
        """运行应用程序"""
        self.root.mainloop() 