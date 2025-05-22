#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chromium指纹补丁管理系统初始化脚本

该脚本用于快速初始化补丁管理系统的目录结构和示例文件，包括：
1. 创建必要的目录结构
2. 创建示例补丁文件
3. 设置环境变量

使用方法：
  python setup_patch_system.py
"""

import os
import sys
import subprocess
import shutil

# 全局配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATCH_MANAGER = os.path.join(BASE_DIR, 'patch_manager.py')

def run_command(cmd):
    """运行命令并返回结果"""
    print(f"执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"命令执行失败: {result.stderr}")
        return False
    return True

def create_example_patches():
    """创建一些示例补丁文件"""
    # 确保patches目录存在
    patches_dir = os.path.join(BASE_DIR, 'patches')
    if not os.path.exists(patches_dir):
        os.makedirs(patches_dir)
    
    # 为每个指纹类别创建目录
    categories = [
        'language', 'ui_language', 'timezone', 'geolocation', 'screen_resolution',
        'display_zoom', 'screen_size', 'color_depth', 'touch_points', 'canvas',
        'canvas_font', 'css_font', 'webrtc', 'webgl'
    ]
    
    for category in categories:
        category_dir = os.path.join(patches_dir, category)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
            print(f"创建目录: {category_dir}")
    
    print("示例补丁目录结构创建完成")

def setup_environment():
    """设置环境变量"""
    # 创建一个示例配置文件
    configs_dir = os.path.join(BASE_DIR, 'configs')
    if not os.path.exists(configs_dir):
        os.makedirs(configs_dir)
    
    # 检查是否已存在template.json
    template_path = os.path.join(configs_dir, 'template.json')
    if not os.path.exists(template_path):
        print("未找到配置模板，将通过patch_manager.py生成")
        run_command([sys.executable, PATCH_MANAGER, 'template'])
    
    # 设置环境变量示例（仅打印说明，不实际设置）
    print("\n要使用指纹配置，请设置以下环境变量：")
    print(f"CHROMIUM_FINGERPRINT_CONFIG={os.path.join(configs_dir, '<your_config_file.json>')}")
    print("\n在Windows中，可以使用以下命令设置环境变量：")
    print(f"set CHROMIUM_FINGERPRINT_CONFIG={os.path.join(configs_dir, 'template.json')}")
    print("\n在Linux/Mac中，可以使用以下命令设置环境变量：")
    print(f"export CHROMIUM_FINGERPRINT_CONFIG={os.path.join(configs_dir, 'template.json')}")

def create_backups_dir():
    """创建备份目录"""
    backups_dir = os.path.join(BASE_DIR, 'backups')
    if not os.path.exists(backups_dir):
        os.makedirs(backups_dir)
        print(f"创建备份目录: {backups_dir}")

def main():
    print("===== 初始化Chromium指纹补丁管理系统 =====")
    
    # 检查patch_manager.py是否存在
    if not os.path.exists(PATCH_MANAGER):
        print(f"错误: 未找到补丁管理脚本 {PATCH_MANAGER}")
        return 1
    
    # 创建目录结构
    print("\n1. 创建补丁管理系统目录结构...")
    run_command([sys.executable, PATCH_MANAGER, 'create_structure'])
    
    # 创建示例补丁
    print("\n2. 创建示例补丁目录...")
    create_example_patches()
    
    # 创建备份目录
    print("\n3. 创建备份目录...")
    create_backups_dir()
    
    # 设置环境变量
    print("\n4. 设置环境变量...")
    setup_environment()
    
    print("\n===== 初始化完成 =====")
    print("\n现在您可以使用以下命令来管理补丁：")
    print(f"1. 应用随机指纹补丁: python {PATCH_MANAGER} apply --random")
    print(f"2. 应用指定配置文件的补丁: python {PATCH_MANAGER} apply --config=<config_file>")
    print(f"3. 还原已应用的补丁: python {PATCH_MANAGER} restore")
    print(f"4. 使用补丁构建Chromium: python {os.path.join(BASE_DIR, 'build_with_patches.py')} --random --build-args=\"ninja -C out/Default chrome\"")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())