#!/bin/bash
# 设置默认值
CONCURRENCY=${CONCURRENCY:-3}
FOLDER_PATHS=${FOLDER_PATHS:-/media/av /media/movies /media/sv}

# 执行任务
cd /app

# 使用数组展开传递参数
python src/cli/main.py --concurrency ${CONCURRENCY} ${FOLDER_PATHS}