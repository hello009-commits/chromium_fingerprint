#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chromium指纹补丁管理系统

该脚本用于管理Chromium源码的指纹修改补丁，支持以下功能：
1. 创建补丁目录结构
2. 根据JSON配置文件应用指纹修改补丁
3. 还原已应用的补丁
4. 生成新的补丁

使用方法：
  python patch_manager.py create_structure  # 创建补丁目录结构
  python patch_manager.py apply --config=<config_file>  # 应用补丁
  python patch_manager.py restore  # 还原补丁
  python patch_manager.py generate --name=<patch_name> --files=<file_list>  # 生成新补丁
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import uuid
from datetime import datetime

# 全局配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')
PATCHES_DIR = os.path.join(BASE_DIR, 'patches')
CONFIG_DIR = os.path.join(BASE_DIR, 'configs')
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')

# 指纹类别
FINGERPRINT_CATEGORIES = [
    'language',           # 浏览器语言
    'ui_language',       # 浏览器界面语言
    'timezone',          # 时区
    'geolocation',       # 地理位置
    'screen_resolution', # 屏幕分辨率
    'display_zoom',      # 显示缩放比例
    'screen_size',       # 可用屏幕尺寸
    'color_depth',       # 颜色深度
    'touch_points',      # 最大触控点
    'canvas',            # canvas画布指纹
    'canvas_font',       # canvas字体指纹
    'css_font',          # css字体指纹
    'webrtc',            # WebRTC
    'webgl',             # WebGL图像
    'webgpu',            # WebGPU
    'audio_context',     # AudioContext
    'client_rects',      # ClientRects
    'ssl_tls',           # SSL TLS
    'hardware_concurrency', # 硬件并发数
    'storage_quota',     # 硬盘数量
    'device_memory',     # 设备内存
    'battery',           # 电池
    'port_scan_protection', # 端口扫描保护
    'console_output',    # 禁用控制台输出
    'do_not_track',      # Do Not Track
    'user_agent',        # User-Agent
    'plugins',           # Plugins
    'mime_types',        # MimeTypes
    'navigator_properties', # Navigator附加属性
    'device_pixel_ratio', # 设备像素比
    'webdriver_detection', # WebDriver检测
    'tls_client_hello',  # TLS ClientHello
    'cdp_protection',    # CDP连接保护
    'ip_address',        # IP地址
    'media_devices',     # 媒体设备指纹
    'speech_voices',     # SpeechVoices
    'local_storage',     # localStorage
    'proxy',             # Proxy代理
    'dns',               # DNS域名系统
    'indexed_db',        # IndexedDB
]

# 补丁文件路径映射
PATCH_FILE_MAPPINGS = {
    'language': [
        'third_party/blink/renderer/core/frame/navigator_language.cc',
        'ui/base/l10n/l10n_util.cc',
        'net/http/http_request_headers.cc',
        'chrome/app/chrome_main_delegate.cc',
        'chrome/browser/chrome_content_browser_client.cc'
    ],
    'ui_language': [
        'content/public/common/content_constants.cc',
        'ui/base/l10n/l10n_util.cc',
        'chrome/browser/browser_process_impl.cc',
        'ui/base/resource/resource_bundle.cc'
    ],
    'timezone': [
        'content/browser/renderer_host/render_process_host_impl.cc',
        'services/device/time_zone_monitor/time_zone_monitor.cc',
        'third_party/blink/renderer/core/timing/performance.cc',
        'base/time/time.cc'
    ],
    'geolocation': [
        'content/browser/geolocation/geolocation_service_impl.cc',
        'third_party/blink/renderer/modules/geolocation/geolocation.cc',
        'services/device/geolocation/geolocation_provider_impl.cc',
        'services/device/geolocation/location_arbitrator.cc',
        'services/device/geolocation/public_ip_address_geolocator.cc'
    ],
    'screen_resolution': [
        'third_party/blink/renderer/core/frame/screen.cc',
        'ui/display/screen.cc',
        'ui/display/display.cc',
        'ui/display/display_list.cc'
    ],
    'display_zoom': [
        'third_party/blink/renderer/core/frame/screen.cc',
        'ui/display/screen.cc',
        'ui/display/display.cc'
    ],
    'screen_size': [
        'third_party/blink/renderer/core/frame/screen.cc',
        'ui/display/screen.cc'
    ],
    'color_depth': [
        'third_party/blink/renderer/core/frame/screen.cc',
        'ui/display/screen.cc'
    ],
    'touch_points': [
        'third_party/blink/renderer/core/frame/screen.cc',
        'ui/display/screen.cc'
    ],
    'canvas': [
        'third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d.cc',
        'third_party/blink/renderer/platform/graphics/canvas_2d_layer_bridge.cc',
        'third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.cc',
        'third_party/blink/renderer/platform/graphics/image_data_buffer.h'
    ],
    'canvas_font': [
        'third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d.cc',
        'third_party/blink/renderer/platform/fonts/font_selector.cc',
        'third_party/blink/renderer/platform/fonts/font_cache.cc'
    ],
    'css_font': [
        'third_party/blink/renderer/core/css/css_font_selector.cc',
        'third_party/blink/renderer/core/css/font_face_set.cc',
        'third_party/blink/renderer/platform/fonts/font_cache.cc'
    ],
    'webrtc': [
        'third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc',
        'net/base/network_interfaces.h',
        'services/network/p2p/socket_manager.cc',
        'third_party/blink/renderer/modules/peerconnection/rtc_ice_candidate.cc'
    ],
    'webgl': [
        'third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc',
        'gpu/command_buffer/client/gles2_implementation.cc',
        'third_party/blink/renderer/modules/webgl/webgl2_rendering_context.cc',
        'third_party/blink/renderer/core/html/canvas/html_canvas_element.cc'
    ],
    'webgpu': [
        'third_party/blink/renderer/modules/webgpu/gpu.cc',
        'third_party/blink/renderer/modules/webgpu/gpu_adapter.cc',
        'third_party/blink/renderer/modules/webgpu/gpu_device.cc'
    ],
    'audio_context': [
        'third_party/blink/renderer/modules/webaudio/audio_context.cc',
        'third_party/blink/renderer/modules/webaudio/base_audio_context.cc',
        'third_party/blink/renderer/modules/webaudio/offline_audio_context.cc'
    ],
    'client_rects': [
        'third_party/blink/renderer/core/dom/element.cc',
        'third_party/blink/renderer/core/layout/layout_object.cc',
        'third_party/blink/renderer/core/layout/layout_box.cc'
    ],
    'ssl_tls': [
        'net/ssl/ssl_client_socket_impl.cc',
        'net/ssl/ssl_config.cc',
        'net/socket/ssl_client_socket.cc'
    ],
    'hardware_concurrency': [
        'third_party/blink/renderer/core/workers/navigator_concurrent_hardware.cc',
        'third_party/blink/renderer/core/frame/navigator.cc'
    ],
    'storage_quota': [
        'third_party/blink/renderer/modules/quota/storage_manager.cc',
        'content/browser/quota/quota_manager_impl.cc'
    ],
    'device_memory': [
        'third_party/blink/renderer/core/frame/navigator_device_memory.cc',
        'third_party/blink/renderer/core/frame/navigator.cc'
    ],
    'battery': [
        'third_party/blink/renderer/modules/battery/battery_manager.cc',
        'services/device/battery/battery_status_manager.cc'
    ],
    'port_scan_protection': [
        'net/socket/tcp_client_socket.cc',
        'net/socket/udp_client_socket.cc',
        'content/browser/renderer_host/render_process_host_impl.cc'
    ],
    'console_output': [
        'third_party/blink/renderer/core/inspector/console_message.cc',
        'content/browser/devtools/devtools_agent_host_impl.cc'
    ],
    'do_not_track': [
        'third_party/blink/renderer/core/frame/navigator.cc',
        'net/http/http_request_headers.cc'
    ],
    'user_agent': [
        'content/common/user_agent.cc',
        'third_party/blink/renderer/core/frame/navigator.cc',
        'net/http/http_util.cc'
    ],
    'plugins': [
        'third_party/blink/renderer/core/frame/navigator_plugins.cc',
        'content/browser/plugin_service_impl.cc'
    ],
    'mime_types': [
        'third_party/blink/renderer/core/frame/navigator_plugins.cc',
        'net/base/mime_util.cc'
    ],
    'navigator_properties': [
        'third_party/blink/renderer/core/frame/navigator.cc',
        'third_party/blink/renderer/core/frame/navigator_id.cc'
    ],
    'device_pixel_ratio': [
        'third_party/blink/renderer/core/frame/screen.cc',
        'ui/display/screen.cc'
    ],
    'webdriver_detection': [
        'third_party/blink/renderer/core/frame/navigator.cc',
        'content/browser/renderer_host/render_process_host_impl.cc'
    ],
    'tls_client_hello': [
        'net/ssl/ssl_client_socket_impl.cc',
        'net/socket/ssl_client_socket.cc'
    ],
    'cdp_protection': [
        'content/browser/devtools/devtools_agent_host_impl.cc',
        'content/browser/devtools/devtools_http_handler.cc'
    ],
    'ip_address': [
        'net/base/network_interfaces.cc',
        'services/network/network_service.cc'
    ],
    'media_devices': [
        'third_party/blink/renderer/modules/mediastream/media_devices.cc',
        'content/browser/media/media_devices_dispatcher_host.cc'
    ],
    'speech_voices': [
        'third_party/blink/renderer/modules/speech/speech_synthesis.cc',
        'content/browser/speech/speech_synthesis_impl.cc'
    ],
    'local_storage': [
        'third_party/blink/renderer/modules/storage/storage_area.cc',
        'content/browser/dom_storage/dom_storage_context_wrapper.cc'
    ],
    'proxy': [
        'net/proxy_resolution/proxy_config.cc',
        'net/proxy_resolution/proxy_resolver.cc'
    ],
    'dns': [
        'net/dns/host_resolver_impl.cc',
        'net/dns/dns_client.cc'
    ],
    'indexed_db': [
        'third_party/blink/renderer/modules/indexeddb/idb_factory.cc',
        'content/browser/indexed_db/indexed_db_context_impl.cc'
    ]
}

def setup_directories():
    """创建补丁管理系统所需的目录结构"""
    directories = [
        PATCHES_DIR,
        CONFIG_DIR,
        BACKUP_DIR
    ]
    
    # 为每个指纹类别创建补丁目录
    for category in FINGERPRINT_CATEGORIES:
        directories.append(os.path.join(PATCHES_DIR, category))
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"创建目录: {directory}")
    
    print("补丁管理系统目录结构创建完成")

def generate_config_template():
    """生成指纹配置模板文件"""
    config_template = {
        "fingerprint_mode": "random",  # random 或 fixed
        "fingerprint_id": str(uuid.uuid4()),
        "creation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "settings": {}
    }
    
    # 为每个指纹类别添加默认配置
    for category in FINGERPRINT_CATEGORIES:
        config_template["settings"][category] = {
            "enabled": True,
            "mode": "default",  # default, custom, random 等，根据具体指纹类型有所不同
            "params": {}
        }
    
    # 添加一些特定指纹的默认参数
    config_template["settings"]["language"]["params"] = {
        "language": "en-US",
        "languages": ["en-US", "en"]
    }
    
    config_template["settings"]["screen_resolution"]["params"] = {
        "width": 1920,
        "height": 1080
    }
    
    config_template["settings"]["geolocation"]["params"] = {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "accuracy": 100
    }
    
    # 保存模板文件
    template_path = os.path.join(CONFIG_DIR, "template.json")
    with open(template_path, "w", encoding="utf-8") as f:
        json.dump(config_template, f, indent=2, ensure_ascii=False)
    
    print(f"配置模板已生成: {template_path}")
    return template_path

def create_random_config():
    """创建随机指纹配置文件"""
    # 先加载模板
    template_path = os.path.join(CONFIG_DIR, "template.json")
    if not os.path.exists(template_path):
        template_path = generate_config_template()
    
    with open(template_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # 设置为随机模式
    config["fingerprint_mode"] = "random"
    config["fingerprint_id"] = str(uuid.uuid4())
    config["creation_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # TODO: 为各个指纹类别生成随机参数
    # 这里需要根据每种指纹的特性生成合适的随机值
    
    # 保存随机配置文件
    random_config_path = os.path.join(CONFIG_DIR, f"fingerprint_{config['fingerprint_id']}.json")
    with open(random_config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"随机指纹配置已生成: {random_config_path}")
    return random_config_path

def backup_original_file(file_path):
    """备份原始文件"""
    rel_path = os.path.relpath(file_path, SRC_DIR)
    backup_path = os.path.join(BACKUP_DIR, rel_path)
    
    # 确保备份目录存在
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    
    # 如果备份文件不存在，则创建备份
    if not os.path.exists(backup_path):
        shutil.copy2(file_path, backup_path)
        print(f"已备份文件: {rel_path}")
    
    return backup_path

def restore_file(file_path):
    """从备份还原文件"""
    rel_path = os.path.relpath(file_path, SRC_DIR)
    backup_path = os.path.join(BACKUP_DIR, rel_path)
    
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, file_path)
        print(f"已还原文件: {rel_path}")
        return True
    else:
        print(f"警告: 未找到备份文件: {rel_path}")
        return False

def apply_patch(patch_file, target_file):
    """应用补丁到目标文件"""
    try:
        # 备份原始文件
        backup_original_file(target_file)
        
        # 使用git apply应用补丁
        cmd = ["git", "apply", "--ignore-whitespace", "--directory", os.path.dirname(SRC_DIR), patch_file]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"已应用补丁: {os.path.basename(patch_file)} 到 {os.path.relpath(target_file, SRC_DIR)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"应用补丁失败: {e.stderr}")
        return False

def generate_patch(original_file, modified_file, patch_name, category):
    """生成补丁文件"""
    rel_path = os.path.relpath(original_file, SRC_DIR)
    patch_dir = os.path.join(PATCHES_DIR, category)
    os.makedirs(patch_dir, exist_ok=True)
    
    patch_file = os.path.join(patch_dir, f"{patch_name}_{os.path.basename(original_file)}.patch")
    
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

def apply_fingerprint_patches(config_file):
    """根据配置文件应用指纹补丁"""
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    print(f"正在应用指纹配置: {config['fingerprint_id']}")
    
    # 记录已应用的补丁
    applied_patches = []
    
    # 遍历每个指纹类别
    for category, settings in config["settings"].items():
        if not settings.get("enabled", True):
            print(f"跳过禁用的指纹类别: {category}")
            continue
        
        mode = settings.get("mode", "default")
        if mode == "default":
            print(f"跳过使用默认设置的指纹类别: {category}")
            continue
        
        print(f"应用 {category} 指纹补丁 (模式: {mode})")
        
        # 获取该类别需要修改的文件列表
        target_files = PATCH_FILE_MAPPINGS.get(category, [])
        
        for rel_file in target_files:
            # 构建完整的文件路径
            target_file = os.path.join(SRC_DIR, rel_file)
            
            # 查找对应的补丁文件
            patch_dir = os.path.join(PATCHES_DIR, category)
            patch_files = [f for f in os.listdir(patch_dir) if f.endswith(".patch") and f.startswith(mode)]
            
            # 筛选出针对当前文件的补丁
            file_patches = [f for f in patch_files if os.path.basename(rel_file) in f]
            
            if file_patches:
                patch_file = os.path.join(patch_dir, file_patches[0])
                if apply_patch(patch_file, target_file):
                    applied_patches.append({
                        "category": category,
                        "target_file": target_file,
                        "patch_file": patch_file
                    })
            else:
                print(f"警告: 未找到 {category} 类别下针对 {rel_file} 的 {mode} 模式补丁")
    
    # 保存应用记录
    record_file = os.path.join(CONFIG_DIR, f"applied_{config['fingerprint_id']}.json")
    with open(record_file, "w", encoding="utf-8") as f:
        json.dump({
            "fingerprint_id": config['fingerprint_id'],
            "applied_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "patches": applied_patches
        }, f, indent=2, ensure_ascii=False)
    
    print(f"指纹补丁应用完成，共应用 {len(applied_patches)} 个补丁")
    return record_file

def restore_all_patches():
    """还原所有已应用的补丁"""
    # 查找最新的应用记录
    record_files = [f for f in os.listdir(CONFIG_DIR) if f.startswith("applied_") and f.endswith(".json")]
    if not record_files:
        print("未找到补丁应用记录，无需还原")
        return
    
    # 按修改时间排序，获取最新的记录
    record_files.sort(key=lambda f: os.path.getmtime(os.path.join(CONFIG_DIR, f)), reverse=True)
    record_file = os.path.join(CONFIG_DIR, record_files[0])
    
    with open(record_file, "r", encoding="utf-8") as f:
        record = json.load(f)
    
    print(f"正在还原指纹 {record['fingerprint_id']} 的补丁")
    
    restored_count = 0
    for patch_info in record["patches"]:
        target_file = patch_info["target_file"]
        if restore_file(target_file):
            restored_count += 1
    
    print(f"补丁还原完成，共还原 {restored_count} 个文件")
    
    # 重命名记录文件，标记为已还原
    restored_record = record_file.replace("applied_", "restored_")
    os.rename(record_file, restored_record)
    
    return restored_count

def main():
    parser = argparse.ArgumentParser(description="Chromium指纹补丁管理系统")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # 创建目录结构命令
    create_parser = subparsers.add_parser("create_structure", help="创建补丁目录结构")
    
    # 应用补丁命令
    apply_parser = subparsers.add_parser("apply", help="应用指纹补丁")
    apply_parser.add_argument("--config", help="指纹配置文件路径")
    apply_parser.add_argument("--random", action="store_true", help="使用随机指纹配置")
    
    # 还原补丁命令
    restore_parser = subparsers.add_parser("restore", help="还原已应用的补丁")
    
    # 生成补丁命令
    generate_parser = subparsers.add_parser("generate", help="生成新的补丁")
    generate_parser.add_argument("--name", required=True, help="补丁名称")
    generate_parser.add_argument("--category", required=True, choices=FINGERPRINT_CATEGORIES, help="指纹类别")
    generate_parser.add_argument("--file", required=True, help="要生成补丁的文件路径（相对于src目录）")
    generate_parser.add_argument("--mode", required=True, help="补丁模式（例如：custom, random）")
    
    # 生成配置模板命令
    template_parser = subparsers.add_parser("template", help="生成指纹配置模板")
    
    args = parser.parse_args()
    
    if args.command == "create_structure":
        setup_directories()
        generate_config_template()
    
    elif args.command == "apply":
        if args.random:
            config_file = create_random_config()
        elif args.config:
            config_file = args.config
        else:
            print("错误: 必须指定配置文件路径或使用--random参数")
            return 1
        
        apply_fingerprint_patches(config_file)
    
    elif args.command == "restore":
        restore_all_patches()
    
    elif args.command == "generate":
        # 构建完整的文件路径
        target_file = os.path.join(SRC_DIR, args.file)
        if not os.path.exists(target_file):
            print(f"错误: 文件不存在: {target_file}")
            return 1
        
        # 备份原始文件
        backup_file = backup_original_file(target_file)
        
        print(f"请修改文件 {target_file} 后再次运行此命令以生成补丁")
        print(f"修改完成后，运行: python {sys.argv[0]} generate --name={args.name} --category={args.category} --file={args.file} --mode={args.mode} --modified")
        
        # 检查是否已修改
        if hasattr(args, "modified") and args.modified:
            patch_name = f"{args.mode}_{args.name}"
            generate_patch(backup_file, target_file, patch_name, args.category)
    
    elif args.command == "template":
        generate_config_template()
    
    else:
        parser.print_help()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())