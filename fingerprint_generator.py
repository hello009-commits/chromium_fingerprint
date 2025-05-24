#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chromium指纹随机生成器

该脚本用于生成随机的指纹配置文件，支持以下功能：
1. 生成完全随机的指纹配置
2. 基于模板生成部分随机的指纹配置
3. 支持指定特定的指纹参数

使用方法：
  python fingerprint_generator.py --output=<output_file>
  python fingerprint_generator.py --template=<template_file> --output=<output_file>
  python fingerprint_generator.py --language="zh-CN" --timezone="Asia/Shanghai" --output=<output_file>
"""

import argparse
import json
import os
import random
import sys
import uuid
from datetime import datetime

# 全局配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, 'configs')

# 随机语言列表
LANGUAGES = [
    "en-US", "en-GB", "zh-CN", "zh-TW", "ja", "ko", "de", "fr", "es", "it",
    "pt-BR", "ru", "nl", "pl", "tr", "ar", "th", "vi", "id", "cs"
]

# 随机时区列表
TIMEZONES = [
    "America/New_York", "America/Los_Angeles", "America/Chicago", "America/Denver",
    "Europe/London", "Europe/Paris", "Europe/Berlin", "Europe/Moscow",
    "Asia/Tokyo", "Asia/Shanghai", "Asia/Singapore", "Asia/Dubai",
    "Australia/Sydney", "Pacific/Auckland"
]

# 随机屏幕分辨率列表
SCREEN_RESOLUTIONS = [
    (1366, 768), (1920, 1080), (1536, 864), (1440, 900), (1600, 900),
    (1280, 720), (1600, 1200), (2560, 1440), (3840, 2160), (1280, 1024),
    (1680, 1050), (2560, 1600), (1920, 1200), (1360, 768), (1024, 768)
]

# 随机缩放比例列表
SCALE_FACTORS = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 3.0]

# 随机颜色深度列表
COLOR_DEPTHS = [24, 30, 32]

# 随机触控点列表
TOUCH_POINTS = [0, 5, 10]

# 随机硬件并发数列表
HARDWARE_CONCURRENCY = [2, 4, 6, 8, 12, 16, 20, 24]

# 随机设备内存列表 (GB)
DEVICE_MEMORY = [4, 8, 16, 32]

# 随机存储配额列表 (GB)
STORAGE_QUOTA = [500, 1000, 2000, 4000]

# 随机User-Agent列表
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0"
]

def generate_random_location():
    """生成随机地理位置"""
    # 生成一个合理范围内的随机经纬度
    latitude = random.uniform(-85, 85)
    longitude = random.uniform(-180, 180)
    accuracy = random.uniform(50, 1000)
    
    return {
        "latitude": round(latitude, 6),
        "longitude": round(longitude, 6),
        "accuracy": round(accuracy, 2)
    }

def generate_random_fingerprint():
    """生成随机指纹配置"""
    # 随机选择语言
    language = random.choice(LANGUAGES)
    languages = [language]
    if "-" in language:
        base_lang = language.split("-")[0]
        if base_lang not in languages:
            languages.append(base_lang)
    
    # 随机选择时区
    timezone = random.choice(TIMEZONES)
    
    # 随机选择屏幕分辨率
    width, height = random.choice(SCREEN_RESOLUTIONS)
    
    # 随机选择缩放比例
    scale_factor = random.choice(SCALE_FACTORS)
    
    # 计算可用屏幕尺寸（通常比实际分辨率小一些）
    available_width = int(width * 0.98)  # 假设任务栏等占用约2%的空间
    available_height = int(height * 0.95)  # 假设任务栏等占用约5%的空间
    
    # 随机选择颜色深度
    color_depth = random.choice(COLOR_DEPTHS)
    
    # 随机选择触控点
    max_touch_points = random.choice(TOUCH_POINTS)
    
    # 生成随机地理位置
    geolocation = generate_random_location()
    
    # 生成随机噪音种子
    canvas_noise_seed = str(uuid.uuid4())
    webgl_noise_seed = str(uuid.uuid4())
    
    # 构建指纹配置
    fingerprint = {
        "fingerprint_mode": "random",
        "fingerprint_id": str(uuid.uuid4()),
        "creation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "settings": {
            "language": {
                "enabled": True,
                "mode": "custom",
                "params": {
                    "language": language,
                    "languages": languages
                }
            },
            "ui_language": {
                "enabled": True,
                "mode": "custom",
                "params": {
                    "language": language
                }
            },
            "timezone": {
                "enabled": True,
                "mode": "custom",
                "params": {
                    "timezone": timezone
                }
            },
            "geolocation": {
                "enabled": True,
                "mode": "custom",
                "params": geolocation
            },
            "screen_resolution": {
                "enabled": True,
                "mode": "custom",
                "params": {
                    "width": width,
                    "height": height
                }
            },
            "display_zoom": {
                "enabled": True,
                "mode": "custom",
                "params": {
                    "scale_factor": scale_factor
                }
            },
            "screen_size": {
                "enabled": True,
                "mode": "custom",
                "params": {
                    "available_width": available_width,
                    "available_height": available_height
                }
            },
            "color_depth": {
                "enabled": True,
                "mode": "custom",
                "params": {
                    "depth": color_depth
                }
            },
            "touch_points": {
                "enabled": True,
                "mode": "custom",
                "params": {
                    "max_touch_points": max_touch_points
                }
            },
            "canvas": {
                "enabled": True,
                "mode": "noise",
                "params": {
                    "noise_seed": canvas_noise_seed,
                    "noise_level": round(random.uniform(0.1, 0.5), 2)
                }
            },
            "canvas_font": {
                "enabled": True,
                "mode": "custom",
                "params": {
                    "protected_fonts": ["Arial", "Times New Roman", "Courier New"]
                }
            },
            "css_font": {
                "enabled": True,
                "mode": "noise",
                "params": {
                    "noise_level": round(random.uniform(0.1, 0.4), 2)
                }
            },
            "webrtc": {
                "enabled": True,
                "mode": "auto_replace",
                "params": {}
            },
            "webgl": {
                "enabled": True,
                "mode": "noise",
                "params": {
                    "noise_seed": webgl_noise_seed,
                    "noise_level": round(random.uniform(0.1, 0.3), 2)
                }
            },
            "webgpu": {
                "enabled": True,
                "mode": "default",
                "params": {}
            },
            "audio_context": {
                "enabled": True,
                "mode": "noise",
                "params": {
                    "noise_level": round(random.uniform(0.05, 0.2), 2)
                }
            },
            "client_rects": {
                "enabled": True,
                "mode": "noise",
                "params": {
                    "noise_level": round(random.uniform(0.01, 0.1), 2)
                }
            },
            "ssl_tls": {
                "enabled": True,
                "mode": "noise",
                "params": {}
            },
            "hardware_concurrency": {
                "enabled": True,
                "mode": "custom",
                "params": {
                    "cores": random.choice(HARDWARE_CONCURRENCY)
                }
            },
            "storage_quota": {
                "enabled": True,
                "mode": "custom",
                "params": {
                    "quota_gb": random.choice(STORAGE_QUOTA)
                }
            },
            "device_memory": {
                "enabled": True,
                "mode": "custom",
                "params": {
                    "memory_gb": random.choice(DEVICE_MEMORY)
                }
            },
            "battery": {
                "enabled": True,
                "mode": "noise",
                "params": {
                    "charging": random.choice([True, False]),
                    "level": round(random.uniform(0.1, 1.0), 2)
                }
            },
            "port_scan_protection": {
                "enabled": True,
                "mode": "enable",
                "params": {}
            },
            "console_output": {
                "enabled": True,
                "mode": "disable",
                "params": {}
            },
            "do_not_track": {
                "enabled": True,
                "mode": "enable",
                "params": {
                    "value": random.choice(["1", "0", "unspecified"])
                }
            },
            "user_agent": {
                "enabled": True,
                "mode": "custom",
                "params": {
                    "user_agent": random.choice(USER_AGENTS)
                }
            },
            "plugins": {
                "enabled": True,
                "mode": "noise",
                "params": {
                    "noise_level": round(random.uniform(0.1, 0.3), 2)
                }
            },
            "mime_types": {
                "enabled": True,
                "mode": "noise",
                "params": {
                    "noise_level": round(random.uniform(0.05, 0.2), 2)
                }
            },
            "navigator_properties": {
                "enabled": True,
                "mode": "default",
                "params": {}
            },
            "device_pixel_ratio": {
                "enabled": True,
                "mode": "default",
                "params": {}
            },
            "webdriver_detection": {
                "enabled": True,
                "mode": "disable",
                "params": {}
            },
            "tls_client_hello": {
                "enabled": True,
                "mode": "noise",
                "params": {}
            },
            "cdp_protection": {
                "enabled": True,
                "mode": "enable",
                "params": {}
            },
            "ip_address": {
                "enabled": True,
                "mode": "custom",
                "params": {
                    "ip": f"{random.randint(192, 223)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
                }
            },
            "media_devices": {
                "enabled": True,
                "mode": "noise",
                "params": {
                    "noise_level": round(random.uniform(0.05, 0.2), 2)
                }
            },
            "speech_voices": {
                "enabled": True,
                "mode": "noise",
                "params": {
                    "noise_level": round(random.uniform(0.05, 0.2), 2)
                }
            },
            "local_storage": {
                "enabled": True,
                "mode": "isolate",
                "params": {}
            },
            "proxy": {
                "enabled": True,
                "mode": "fake_ip",
                "params": {
                    "proxy_ip": f"{random.randint(127, 192)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}",
                    "proxy_port": random.choice([8080, 3128, 1080, 8888, 9999])
                }
            },
            "dns": {
                "enabled": True,
                "mode": "noise",
                "params": {}
            },
            "indexed_db": {
                "enabled": True,
                "mode": "isolate",
                "params": {}
            }
        }
    }
    
    return fingerprint

def load_template(template_file):
    """加载指纹配置模板"""
    with open(template_file, "r", encoding="utf-8") as f:
        return json.load(f)

def merge_with_template(template, overrides):
    """将自定义参数合并到模板中"""
    result = template.copy()
    
    # 更新指纹ID和创建时间
    result["fingerprint_id"] = str(uuid.uuid4())
    result["creation_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 处理覆盖参数
    for category, params in overrides.items():
        if category in result["settings"]:
            # 启用该类别
            result["settings"][category]["enabled"] = True
            result["settings"][category]["mode"] = "custom"
            
            # 更新参数
            for key, value in params.items():
                result["settings"][category]["params"][key] = value
    
    return result

def save_fingerprint(fingerprint, output_file):
    """保存指纹配置到文件"""
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(fingerprint, f, indent=2, ensure_ascii=False)
    
    print(f"指纹配置已保存到: {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(description="Chromium指纹随机生成器")
    
    # 基本参数
    parser.add_argument("--output", help="输出文件路径")
    parser.add_argument("--template", help="模板文件路径")
    
    # 指纹参数
    parser.add_argument("--language", help="浏览器语言")
    parser.add_argument("--timezone", help="时区")
    parser.add_argument("--resolution", help="屏幕分辨率，格式：宽x高，例如：1920x1080")
    parser.add_argument("--latitude", type=float, help="地理位置纬度")
    parser.add_argument("--longitude", type=float, help="地理位置经度")
    
    args = parser.parse_args()
    
    # 确定输出文件路径
    if args.output:
        output_file = args.output
    else:
        fingerprint_id = str(uuid.uuid4())
        output_file = os.path.join(CONFIG_DIR, f"fingerprint_{fingerprint_id}.json")
        os.makedirs(CONFIG_DIR, exist_ok=True)
    
    # 处理自定义参数
    custom_params = {}
    
    if args.language:
        custom_params["language"] = {
            "language": args.language,
            "languages": [args.language]
        }
        if "-" in args.language:
            base_lang = args.language.split("-")[0]
            custom_params["language"]["languages"].append(base_lang)
    
    if args.timezone:
        custom_params["timezone"] = {"timezone": args.timezone}
    
    if args.resolution:
        try:
            width, height = map(int, args.resolution.split("x"))
            custom_params["screen_resolution"] = {"width": width, "height": height}
        except ValueError:
            print(f"错误: 无效的分辨率格式: {args.resolution}，应为宽x高，例如：1920x1080")
            return 1
    
    if args.latitude is not None and args.longitude is not None:
        custom_params["geolocation"] = {
            "latitude": args.latitude,
            "longitude": args.longitude,
            "accuracy": 100
        }
    
    # 生成指纹配置
    if args.template:
        # 基于模板生成
        template = load_template(args.template)
        fingerprint = merge_with_template(template, custom_params)
    else:
        # 生成完全随机的指纹配置
        fingerprint = generate_random_fingerprint()
        
        # 应用自定义参数
        for category, params in custom_params.items():
            if category in fingerprint["settings"]:
                for key, value in params.items():
                    fingerprint["settings"][category]["params"][key] = value
    
    # 保存指纹配置
    save_fingerprint(fingerprint, output_file)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())