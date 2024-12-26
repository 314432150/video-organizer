import argparse
import sys
import asyncio
from src.core.organizer import VideoOrganizer
from src.core.console_logger import ConsoleLogger

async def process_folder(folder_path):
    """处理单个文件夹"""
    try:
        await ConsoleLogger._safe_print(f"开始处理目录: {folder_path}")
        result = await VideoOrganizer.organize_files(folder_path)
        
        if not result:
            await ConsoleLogger._safe_print(f"目录 {folder_path} 中未找到视频文件")
        return result
            
    except Exception as e:
        await ConsoleLogger._safe_print(f"处理目录 {folder_path} 时出错: {str(e)}")
        return False

async def main():
    parser = argparse.ArgumentParser(description='视频文件自动整理工具')
    parser.add_argument('folder_paths', nargs='+', help='需要整理的文件夹路径，可以指定多个路径')
    parser.add_argument('--concurrency', type=int, default=3, help='同时处理的最大目录数（默认为3）')
    args = parser.parse_args()

    # 使用信号量限制并发数
    semaphore = asyncio.Semaphore(args.concurrency)
    
    async def process_with_semaphore(path):
        async with semaphore:
            return await process_folder(path)

    # 并发处理所有目录
    tasks = [process_with_semaphore(path) for path in args.folder_paths]
    results = await asyncio.gather(*tasks)
    
    # 检查处理结果
    success_count = sum(1 for r in results if r)
    total_count = len(args.folder_paths)
    
    await ConsoleLogger._safe_print(f"处理完成！成功: {success_count}/{total_count}")
    
    # 如果有处理失败的目录，返回非零状态码
    if success_count != total_count:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 
    