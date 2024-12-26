import asyncio
import os
from datetime import datetime

class ConsoleLogger:
    _print_lock = asyncio.Lock()
    _log_file = "logs/organizer.log"
    
    @staticmethod
    async def _ensure_log_directory():
        """确保日志目录存在"""
        os.makedirs(os.path.dirname(ConsoleLogger._log_file), exist_ok=True)
    
    @staticmethod
    async def _safe_print(message):
        """异步安全的打印函数，同时输出到控制台和日志文件"""
        async with ConsoleLogger._print_lock:
            # 打印到控制台
            print(message)
            
            # 写入日志文件
            await ConsoleLogger._ensure_log_directory()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{timestamp}] {message}\n"
            
            # 使用 asyncio.to_thread 进行异步文件写入
            await asyncio.to_thread(
                lambda: open(ConsoleLogger._log_file, 'a', encoding='utf-8').write(log_message)
            )

    @staticmethod
    async def log_start(total_steps):
        await ConsoleLogger._safe_print(f"找到 {total_steps} 个视频组需要处理...")

    @staticmethod
    async def log_group_start(group_name, current_step, total_steps):
        await ConsoleLogger._safe_print(f"处理视频组 [{current_step}/{total_steps}]: {group_name}")

    @staticmethod
    async def log_folder_creation(folder_path):
        await ConsoleLogger._safe_print(f"创建文件夹: {folder_path}")

    @staticmethod
    async def log_file_move(file_name):
        await ConsoleLogger._safe_print(f"移动文件: {file_name}")

    @staticmethod
    async def log_completion(total_steps):
        await ConsoleLogger._safe_print(f"整理完成! 共处理了 {total_steps} 个视频组。")

    @staticmethod
    async def log_file_rename(old_name, new_name):
        await ConsoleLogger._safe_print(f"重命名文件: {old_name} -> {new_name}") 