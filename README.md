# Chromium指纹补丁管理系统

## 项目概述

本项目旨在实现一个完整的Chromium指纹修改系统，支持Mac、Windows和Linux平台。该系统通过补丁管理器对Chromium源码中的指纹相关代码进行临时修改，实现浏览器指纹的自定义或随机化。

系统支持以下两种指纹模式：

1. **随机指纹模式**：在每次启动浏览器前，系统会自动生成一个JSON配置文件，包含各项指纹的种子配置参数列表。
2. **固定指纹环境模式**：启动浏览器时，系统会加载一个固定的JSON配置文件，确保每个账号拥有稳定一致的浏览器环境。

## 目录结构

```
D:\chromium125.0.6422.0\
├── patch_manager.py     # 补丁管理主脚本
├── patches\            # 补丁文件目录
│   ├── language\       # 浏览器语言相关补丁
│   ├── ui_language\    # 浏览器界面语言相关补丁
│   ├── timezone\       # 时区相关补丁
│   └── ...             # 其他指纹类别的补丁
├── configs\            # 指纹配置文件目录
│   ├── template.json   # 配置模板
│   └── ...             # 生成的指纹配置文件
├── backups\            # 原始文件备份目录
└── src\                # Chromium源码目录
```

## 支持的指纹类别

1. 浏览器语言
2. 浏览器界面语言
3. 时区
4. 地理位置
5. 屏幕分辨率
6. 显示缩放比例
7. 可用屏幕尺寸
8. 颜色深度
9. 最大触控点
10. Canvas画布指纹
11. Canvas字体指纹
12. CSS字体指纹
13. WebRTC网络接口
14. WebGL图像
15. WebGL元数据
16. WebGPU
17. WebGL特性掩码
18. AudioContext
19. ClientRects
20. TLS握手指纹
21. 硬件并发数
22. 硬盘数量
23. 设备内存
24. 电池信息
25. 端口扫描保护
26. 控制台输出控制
27. Do Not Track设置
28. User-Agent
29. 浏览器插件
30. MIME类型
31. Navigator附加属性
32. 设备像素比
33. WebDriver/自动化标志
34. ClientHello指纹
35. CDP连接防护
36. IP地址
37. 媒体设备列表
38. 语音合成声音
39. 本地存储隔离
40. 代理检测防护
41. DNS指纹
42. IndexedDB隔离

## 使用方法

### 初始化补丁管理系统

```bash
python patch_manager.py create_structure
```

此命令将创建补丁管理系统所需的目录结构，并生成指纹配置模板文件。

### 生成指纹配置模板

```bash
python patch_manager.py template
```

### 应用指纹补丁

#### 使用随机指纹配置

```bash
python patch_manager.py apply --random
```

#### 使用指定的配置文件

```bash
python patch_manager.py apply --config=configs/fingerprint_xxxx.json
```

### 还原已应用的补丁

```bash
python patch_manager.py restore
```

### 生成新的补丁

1. 首先运行以下命令备份原始文件：

```bash
python patch_manager.py generate --name=custom_language --category=language --file=third_party/blink/renderer/core/frame/navigator_language.cc --mode=custom
```

2. 修改指定的文件

3. 再次运行相同命令，但添加`--modified`参数生成补丁：

```bash
python patch_manager.py generate --name=custom_language --category=language --file=third_party/blink/renderer/core/frame/navigator_language.cc --mode=custom --modified
```

## 配置文件格式

指纹配置文件使用JSON格式，示例如下：

```json
{
  "fingerprint_mode": "random",
  "fingerprint_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "creation_time": "2023-05-20 12:34:56",
  "settings": {
    "language": {
      "enabled": true,
      "mode": "custom",
      "params": {
        "language": "en-US",
        "languages": ["en-US", "en"]
      }
    },
    "webrtc": {
      "enabled": true,
      "mode": "auto_replace",
      "params": {
        "use_proxy_ip": true
      }
    },
    "canvas": {
      "enabled": true,
      "mode": "noise",
      "params": {
        "seed": "canvas_noise_seed_string",
        "noise_level": 0.5
      }
    }
    // 其他指纹设置...
  }
}
```

## 集成到构建流程

在编译Chromium之前，可以通过以下步骤集成补丁管理系统：

1. 生成或选择一个指纹配置文件
2. 应用指纹补丁：`python patch_manager.py apply --config=<config_file>`
3. 执行正常的Chromium构建命令
4. 构建完成后，还原补丁：`python patch_manager.py restore`

## 注意事项

1. 补丁应用后会自动备份原始文件，以便后续还原
2. 每次应用补丁会生成应用记录，记录在`configs/applied_<fingerprint_id>.json`文件中
3. 还原补丁后，应用记录会被重命名为`configs/restored_<fingerprint_id>.json`
4. 在生成新补丁时，请确保修改的代码能够正确编译和运行

## 系统要求

- Python 3.6+
- Git (用于生成和应用补丁)
- Chromium源码 (版本 125.0.6422.0)
