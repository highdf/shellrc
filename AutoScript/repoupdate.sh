#!/usr/bin/env zsh

# 安全Git推送脚本
# 带错误检测和操作确认机制

# ------ 配置区 ------
local -A REPOS=(
    Algorithm  "$HOME/Algorithm"
    shellrc    "$HOME/shellrc"
)
local BRANCH="main"
local USE_FORCE=false  # 设置为true时才允许强制推送
# --------------------

# 初始化日志功能
function log() {
    echo "[$(date +'%Y-%m-%d %T')] $*"
}

# 异常处理函数
function handle_error() {
    log "错误: $1"
    exit 1
}

# 安全确认提示
function confirm_operation() {
    echo -n "是否继续？[y/N] "
    read -r response
    [[ "$response" =~ ^[Yy]$ ]] || handle_error "用户取消操作"
}

# 仓库操作函数
function push_repo() {
    local repo_name=$1
    local repo_path=$2
    
    log "正在处理仓库: $repo_name"
    
    # 目录存在性检查
    [[ -d "$repo_path" ]] || handle_error "仓库不存在: $repo_path"
    
    # 进入仓库目录
    if ! cd "$repo_path"; then
        handle_error "无法进入目录: $repo_path"
    fi
    
    # 验证Git仓库
    if ! git rev-parse --is-inside-work-tree &> /dev/null; then
        handle_error "不是Git仓库: $repo_path"
    fi
    
    # 执行Git操作
    (
        log "添加所有变更..."
        if ! git add . ; then
            handle_error "git add失败: $repo_name"
        fi
        
        log "提交变更..."
        if ! git commit --amend --no-edit ; then
            handle_error "git commit失败: $repo_name"
        fi
        
        # 构造推送命令
        local push_cmd=(git push)
        $USE_FORCE && push_cmd+=(--force-with-lease)
        
        log "推送变更..."
        if ! $push_cmd origin "$BRANCH"; then
            handle_error "git push失败: $repo_name"
        fi
        
        log "操作成功: $repo_name"
    )
}

# 主执行流程
function main() {
    log "开始Git推送流程"
    
    # 显示操作摘要
    print "即将操作："
    print "分支: \t\t$BRANCH"
    print "强制推送: \t$USE_FORCE"
    print "目标仓库:"
    for name path in ${(kv)REPOS}; do
        print "  - $name \t($path)"
    done
    
    # 安全确认
    confirm_operation
    
    # 遍历处理所有仓库
    for name path in ${(kv)REPOS}; do
        push_repo "$name" "$path" || handle_error "$name处理失败"
    done
    
    log "所有操作完成！"
}

# 执行主流程
main
