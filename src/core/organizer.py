import os
import shutil
import asyncio
from src.core.constants import SUPPORTED_VIDEO_EXTENSIONS
from src.core.console_logger import ConsoleLogger

class VideoOrganizer:
    @staticmethod
    def get_base_video_name(filename):
        """从文件名中提取基本视频名称"""
        name = os.path.splitext(filename)[0].strip()
        multi_part_indicators = ['-cd', '-a', '-b', '-c', '-1', '-2', '-3', 'part']
        
        for indicator in multi_part_indicators:
            if indicator in name.lower():
                parts = name.split(indicator)
                return parts[0].rstrip('-').strip()
        return name

    @staticmethod
    async def organize_files(folder_path, progress_callback=None):
        """整理指定文件夹中的视频文件"""
        # 重新获取处理后的文件列表
        files = [f for f in os.listdir(folder_path) 
                if os.path.isfile(os.path.join(folder_path, f))]

        video_groups = {}
        for file in files:
            if file.lower().endswith(tuple(ext.lower() for ext in SUPPORTED_VIDEO_EXTENSIONS)):
                base_name = VideoOrganizer.get_base_video_name(file)
                if base_name not in video_groups:
                    video_groups[base_name] = []
                video_groups[base_name].append(file)

        total_steps = len(video_groups)
        processed_steps = 0

        # 如果没有找到视频文件，直接返回 True（视为成功）
        if total_steps == 0:
            await ConsoleLogger.log_start(0)
            if progress_callback:
                progress_callback(0, 0)
            return True

        await ConsoleLogger.log_start(total_steps)

        for base_name, video_files in video_groups.items():
            await ConsoleLogger.log_group_start(base_name, processed_steps + 1, total_steps)
            video_folder = os.path.join(folder_path, base_name.strip())
            
            if not os.path.exists(video_folder):
                await asyncio.to_thread(os.makedirs, video_folder)
                await ConsoleLogger.log_folder_creation(video_folder)
            
            for file in files:
                if (file.startswith(base_name + "-") or
                    file.startswith(base_name + " ") or
                    file == base_name or
                    file.startswith(base_name + ".")):
                    source = os.path.join(folder_path, file)
                    destination = os.path.join(video_folder, file)
                    await ConsoleLogger.log_file_move(file)
                    await asyncio.to_thread(shutil.move, source, destination)
            
            processed_steps += 1
            if progress_callback:
                progress_callback(processed_steps, total_steps)

        await ConsoleLogger.log_completion(total_steps)
        return True  # 处理完成返回 True
        