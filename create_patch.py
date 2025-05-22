#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chromium指纹补丁创建工具

该脚本用于简化创建新的指纹补丁的过程，支持以下功能：
1. 备份原始文件
2. 打开编辑器修改文件
3. 生成补丁文件

使用方法：
  python create_patch.py --category=<指纹类别> --file=<文件路径> --mode=<补丁模式> --name=<补丁名称>

示例：
  python create_patch.py --category=language --file=third_party/blink/renderer/core/frame/navigator_language.cc --mode=custom --name=french_language
"""

import argparse
import os
import subprocess
import sys
import tempfile
import shutil

# 全局配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')
PATCHES_DIR = os.path.join(BASE_DIR, 'patches')
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')

# 指纹类别
FINGERPRINT_CATEGORIES = [
    'language', 'ui_language', 'timezone', 'geolocation', 'screen_resolution',
    'display_zoom', 'screen_size', 'color_depth', 'touch_points', 'canvas',
    'canvas_font', 'css_font', 'webrtc', 'webgl'
]

def backup_file(file_path):
    """备份原始文件"""
    rel_path = os.path.relpath(file_path, SRC_DIR)
    backup_path = os.path.join(BACKUP_DIR, rel_path)
    
    # 确保备份目录存在
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    
    # 备份文件
    shutil.copy2(file_path, backup_path)
    print(f"已备份文件: {rel_path} 到 {backup_path}")
    
    return backup_path

def open_editor(file_path):
    """打开编辑器修改文件"""
    if os.name == 'nt':  # Windows
        os.startfile(file_path)
    elif os.name == 'posix':  # Linux/Mac
        editor = os.environ.get('EDITOR', 'nano')
        subprocess.call([editor, file_path])
    else:
        print(f"请手动打开文件进行编辑: {file_path}")
    
    input("\n请在编辑器中修改文件，完成后按回车键继续...")

def generate_patch(original_file, modified_file, patch_name, category, mode):
    """生成补丁文件"""
    rel_path = os.path.relpath(modified_file, SRC_DIR)
    patch_dir = os.path.join(PATCHES_DIR, category)
    os.makedirs(patch_dir, exist_ok=True)
    
    patch_file = os.path.join(patch_dir, f"{mode}_{patch_name}_{os.path.basename(modified_file)}.patch")
    
    try:
        # 使用git diff生成补丁
        cmd = ["git", "diff", "--no-index", original_file, modified_file]
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
        
        # 保存补丁文件
        with open(patch_file, "w", encoding="utf-8") as f:
            # 修改补丁文件中的路径，使其相对于src目录
            patch_content = result.stdout.replace(original_file, f"a/{rel_path}").replace(modified_file, f"b/{rel_path}")
            f.write(patch_content)
        
        print(f"已生成补丁: {patch_file}")
        return patch_file
    except Exception as e:
        print(f"生成补丁失败: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Chromium指纹补丁创建工具")
    
    parser.add_argument("--category", required=True, choices=FINGERPRINT_CATEGORIES, help="指纹类别")
    parser.add_argument("--file", required=True, help="要修改的文件路径（相对于src目录）")
    parser.add_argument("--mode", required=True, help="补丁模式（例如：custom, random, noise）")
    parser.add_argument("--name", required=True, help="补丁名称")
    
    args = parser.parse_args()
    
    # 构建完整的文件路径
    target_file = os.path.join(SRC_DIR, args.file)
    if not os.path.exists(target_file):
        print(f"错误: 文件不存在: {target_file}")
        return 1
    
    # 备份原始文件
    backup_path = backup_file(target_file)
    
    # 创建临时工作副本
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(target_file)[1]) as temp_file:
        temp_path = temp_file.name
    
    # 复制原始文件到临时文件
    shutil.copy2(target_file, temp_path)
    
    # 打开编辑器修改临时文件
    print(f"\n正在打开编辑器，请修改文件...")
    open_editor(temp_path)
    
    # 检查文件是否被修改
    with open(backup_path, "rb") as f1, open(temp_path, "rb") as f2:
        if f1.read() == f2.read():
            print("警告: 文件未被修改，不生成补丁")
            os.unlink(temp_path)
            return 1
    
    # 生成补丁
    patch_file = generate_patch(backup_path, temp_path, args.name, args.category, args.mode)
    
    # 清理临时文件
    os.unlink(temp_path)
    
    if patch_file:
        print(f"\n补丁创建成功！")
        print(f"补丁文件: {patch_file}")
        print(f"\n您可以使用以下命令应用此补丁:")
        print(f"python patch_manager.py apply --config=<config_file>")
        print(f"\n确保您的配置文件中包含以下设置:")
        print(f'  "{args.category}": {{')
        print(f'    "enabled": true,')
        print(f'    "mode": "{args.mode}",')
        print(f'    "params": {{}}')
        print(f'  }}')
    
    return 0 if patch_file else 1

if __name__ == "__main__":
    sys.exit(main())