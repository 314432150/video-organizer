# 使用官方 Python 基础镜像
FROM python:3.11-slim

# 安装 cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY src/ /app/src/
COPY scripts/ /app/scripts/

# 创建日志目录
RUN mkdir -p logs

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV TZ=Asia/Shanghai

# 设置启动脚本权限
RUN chmod +x /app/scripts/start.sh

# 创建 cron 任务文件（内容将在运行时填充）
RUN touch /etc/cron.d/video-organizer
RUN chmod 0644 /etc/cron.d/video-organizer

# 设置入口点
ENTRYPOINT ["/app/scripts/start.sh"] 