#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chromium指纹补丁构建集成脚本

该脚本用于在Chromium构建过程中自动应用和还原指纹补丁，支持以下功能：
1. 应用指定的指纹配置
2. 执行Chromium构建命令
3. 构建完成后还原补丁

使用方法：
  python build_with_patches.py --config=<config_file> --build-args="<构建参数>"
  python build_with_patches.py --random --build-args="<构建参数>"
"""

import argparse
import os
import subprocess
import sys
import time

# 全局配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATCH_MANAGER = os.path.join(BASE_DIR, 'patch_manager.py')

def run_command(cmd, cwd=None):
    """运行命令并实时输出结果"""
    print(f"执行命令: {' '.join(cmd)}")
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=cwd or BASE_DIR
    )
    
    # 实时输出命令执行结果
    for line in process.stdout:
        print(line, end='')
    
    # 等待命令执行完成
    return_code = process.wait()
    if return_code != 0:
        print(f"命令执行失败，返回码: {return_code}")
        return False
    
    return True

def apply_patches(config_file=None, random=False):
    """应用指纹补丁"""
    cmd = [sys.executable, PATCH_MANAGER, 'apply']
    
    if config_file:
        cmd.extend(['--config', config_file])
    elif random:
        cmd.append('--random')
    else:
        print("错误: 必须指定配置文件或使用随机模式")
        return False
    
    return run_command(cmd)

def restore_patches():
    """还原指纹补丁"""
    cmd = [sys.executable, PATCH_MANAGER, 'restore']
    return run_command(cmd)

def build_chromium(build_args):
    """执行Chromium构建命令"""
    # 解析构建参数
    build_cmd = build_args.split()
    
    # 检查是否是Windows平台
    if os.name == 'nt':
        # 在Windows上，通常使用ninja进行构建
        if not build_cmd or build_cmd[0].lower() not in ['ninja', 'autoninja']:
            print("警告: 在Windows平台上，推荐使用ninja或autoninja进行构建")
    
    # 执行构建命令
    return run_command(build_cmd, cwd=os.path.join(BASE_DIR, 'src'))

def main():
    parser = argparse.ArgumentParser(description="Chromium指纹补丁构建集成脚本")
    
    # 补丁配置参数
    patch_group = parser.add_mutually_exclusive_group(required=True)
    patch_group.add_argument("--config", help="指纹配置文件路径")
    patch_group.add_argument("--random", action="store_true", help="使用随机指纹配置")
    
    # 构建参数
    parser.add_argument("--build-args", required=True, help="Chromium构建命令及参数")
    parser.add_argument("--skip-restore", action="store_true", help="跳过还原补丁步骤")
    
    args = parser.parse_args()
    
    # 确保补丁管理系统目录结构已创建
    if not os.path.exists(os.path.join(BASE_DIR, 'patches')):
        print("初始化补丁管理系统目录结构...")
        if not run_command([sys.executable, PATCH_MANAGER, 'create_structure']):
            return 1
    
    # 应用补丁
    print("\n===== 应用指纹补丁 =====")
    if not apply_patches(args.config, args.random):
        print("应用补丁失败，中止构建")
        return 1
    
    try:
        # 执行构建
        print("\n===== 开始构建Chromium =====")
        build_start_time = time.time()
        build_success = build_chromium(args.build_args)
        build_end_time = time.time()
        build_duration = build_end_time - build_start_time
        
        if build_success:
            print(f"\n构建成功！耗时: {build_duration:.2f}秒 ({build_duration/60:.2f}分钟)")
        else:
            print("\n构建失败！")
    finally:
        # 无论构建是否成功，都尝试还原补丁
        if not args.skip_restore:
            print("\n===== 还原指纹补丁 =====")
            restore_patches()
    
    return 0 if build_success else 1

if __name__ == "__main__":
    sys.exit(main())