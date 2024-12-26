# Video Organizer

一个用于自动整理视频文件的工具，支持命令行和图形界面。

## 功能特点

- 自动识别视频文件组并创建文件夹
- 支持多目录并发处理
- 命令行和图形界面双模式
- 深色主题 UI
- 异步处理，响应迅速
- 自动日志记录

## 使用方法

### 命令行模式

```bash
# 处理单个目录
python src/cli/main.py /path/to/videos

# 处理多个目录
python src/cli/main.py /path1 /path2 /path3

# 设置并发数（默认为3）
python src/cli/main.py --concurrency 5 /path/to/videos
```

### 图形界面模式

```bash
python src/gui/main.py
```

## Docker 支持

```bash
# 构建镜像
cd docker
docker-compose build

# 运行（处理单个目录）
docker-compose run --rm video-organizer /media/videos

# 运行（处理多个目录）
docker-compose run --rm video-organizer /media/av /media/movies /media/sv

# 设置并发数
docker-compose run --rm video-organizer --concurrency 5 /media/videos
```

## 支持的视频格式

```python:src/core/constants.py
startLine: 2
endLine: 15
```

## 功能说明

1. **自动识别视频组**
   - 识别同名视频文件
   - 支持多种分集标识（-cd, -1, part 等）
   - 自动处理文件名空格

2. **文件整理**
   - 创建以视频名称命名的文件夹
   - 移动相关文件到对应文件夹
   - 保持原始文件名

3. **进度显示**
   - 命令行模式实时输出
   - GUI 模式进度条显示
   - 详细的操作日志

4. **错误处理**
   - 文件冲突自动处理
   - 详细的错误提示
   - 操作日志记录

## 开发环境

- Python 3.11+
- tkinter (GUI)
- asyncio (异步处理)

## 日志记录

所有操作都会记录在 `logs/organizer.log` 文件中，包括：
- 文件移动
- 文件夹创建
- 文件重命名
- 错误信息

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

本项目采用 MIT 许可证