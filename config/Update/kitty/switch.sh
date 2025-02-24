#!/usr/bin/zsh

# 获取当前小时数
current_hour=$(date +"%H")

# 定义日间和夜间的时间范围
morning_start=6      # 日间的开始时间（例如早上6点）
evening_end=17        # 夜间的结束时间（例如晚上6点）

# if (( current_hour >= morning_start && current_hour < evening_end )); then
    # theme_file="$HOME/.config/kitty/theme/Catppuccin-Latte.conf"
    # /usr/bin/plasma-apply-colorscheme BreezeLight
# else
    # theme_file="$HOME/.config/kitty/theme/Catppuccin-Mocha.conf"
    # /usr/bin/plasma-apply-colorscheme BreezeDark
# fi

if (( current_hour >= morning_start && current_hour < evening_end )); then
    theme_file="$HOME/.config/kitty/theme/Tokyo_Night_Day.conf"
    /usr/bin/plasma-apply-colorscheme BreezeLight
else
    theme_file="$HOME/.config/kitty/theme/Tokyo_Night_Moon.conf"
    /usr/bin/plasma-apply-colorscheme BreezeDark
fi

# 将选定的主题文件复制到 kitty 默认配置文件位置
cp "$theme_file" "$HOME/.config/kitty/theme/theme.conf"

kitty @ load-config
