#!/bin/bash

SESSION_NAME="music_labeling"
SCRIPT_PATH="python main.py"
LOG_PATH="logs/music_labeling_$(date +%Y%m%d_%H%M%S).log"

# 创建 logs 目录（如果不存在）
mkdir -p logs

# 检查是否已有该 tmux 会话
tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? != 0 ]; then
    echo "🔧 启动 tmux 会话：$SESSION_NAME"
    tmux new -d -s $SESSION_NAME "$SCRIPT_PATH > $LOG_PATH 2>&1"
    echo "✅ 标注任务已在后台运行，日志输出至: $LOG_PATH"
else
    echo "⚠️ 会话 '$SESSION_NAME' 已存在。可以使用以下命令查看："
    echo "    tmux attach -t $SESSION_NAME"
fi
