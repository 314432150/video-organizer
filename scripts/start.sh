#!/bin/bash

# 获取传入的参数
ARGS="$@"

# 创建 cron 任务
echo "16 52 * * * python /app/src/cli/main.py $ARGS >> /app/logs/cron.log 2>&1" > /etc/cron.d/video-organizer

# 启动 cron 服务
cron

# 保持容器运行并输出日志
tail -f /app/logs/cron.log 