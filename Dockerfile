# 使用官方 Python 基础镜像
FROM python:3.11-slim

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

# 设置入口点
ENTRYPOINT ["/app/scripts/start.sh"] 