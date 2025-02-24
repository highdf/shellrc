#!/usr/bin/env zsh

# 配置备份脚本
# 安全备份配置文件到指定目录，包含错误处理和日志输出

# ------ 可配置变量 ------
local BACKUP_DIR="/home/luky/shellrc/config/Update"
local -a backup_items=(
    "$HOME/.config/kitty"
    "$HOME/.config/yazi"
    "$HOME/.zshrc"
    "$HOME/.tmux.conf"
)
# ------------------------

# 初始化日志功能
function log() {
    echo "[$(date +'%Y-%m-%d %T')] $*"
}

# 异常处理函数
function handle_error() {
    log "错误: $1"
    exit 1
}

# 安全检查函数
function validate_directory() {
    [[ -z "$1" ]] && handle_error "目录路径不能为空"
    
    # 防止误删根目录的安全检查
    [[ "$1" == "/" ]] && handle_error "危险！拒绝操作根目录"
    [[ "$1" == "$HOME" ]] && handle_error "危险！拒绝操作用户主目录"
}

# 主备份流程
function main() {
    log "开始配置文件备份流程"

    # 验证备份目录
    validate_directory "$BACKUP_DIR"

    # 清理旧备份（保留目录结构）
    if [[ -d "$BACKUP_DIR" ]]; then
        log "清理旧备份..."
        if rm -rf "${BACKUP_DIR:?}"/*; then
            log "旧备份清理成功"
        else
            handle_error "旧备份清理失败"
        fi
    else
        log "创建备份目录..."
        if mkdir -p "$BACKUP_DIR"; then
            log "备份目录创建成功：$BACKUP_DIR"
        else
            handle_error "无法创建备份目录"
        fi
    fi

    # 执行文件备份
    local item
    for item in $backup_items; do
        log "正在备份：$item"
        
        if [[ ! -e $item ]]; then
            log "警告：文件不存在，跳过 $item"
            continue
        fi
        
        if cp -r "$item" "$BACKUP_DIR/"; then
            log "成功备份：$item"
        else
            handle_error "备份失败：$item"
        fi
    done

    log "所有操作完成！备份保存在：$BACKUP_DIR"
}

# 执行主函数
main
