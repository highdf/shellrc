#!/usr/bin/zsh

# 获取当前小时数
current_hour=$(date +"%H")

# 定义日间和夜间的时间范围
morning_start=6      # 日间的开始时间（例如早上6点）
evening_end=17        # 夜间的结束时间（例如晚上6点）

if (( current_hour >= morning_start && current_hour < evening_end )); then
    theme_file="$HOME/.config/kitty/Catppuccin-Latte.conf"
else
    theme_file="$HOME/.config/kitty/Catppuccin-Mocha.conf"
fi

# if (( current_hour >= morning_start && current_hour < evening_end )); then
#     theme_file="$HOME/.config/kitty/Tokyo_Night_Day.conf"
# else
#     theme_file="$HOME/.config/kitty/Tokyo_Night_Moon.conf"
# fi

# 将选定的主题文件复制到 kitty 默认配置文件位置
cp "$theme_file" "$HOME/.config/kitty/theme.conf"

kitty @ load-config
