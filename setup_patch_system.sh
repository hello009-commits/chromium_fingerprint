#!/bin/bash

echo "===== Chromium指纹补丁管理系统初始化 ====="
echo 

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python，请先安装Python 3.6+"
    exit 1
fi

# 检查Git是否安装
if ! command -v git &> /dev/null; then
    echo "警告: 未找到Git，某些补丁功能可能无法正常工作"
fi

# 创建必要的目录
mkdir -p patches configs backups

# 运行初始化脚本
python3 setup_patch_system.py

echo 
echo "===== 初始化完成 ====="
echo 
echo "您可以使用以下命令："
echo "1. 生成随机指纹配置: python3 fingerprint_generator.py"
echo "2. 应用指纹补丁: python3 patch_manager.py apply --config=configs/template.json"
echo "3. 还原补丁: python3 patch_manager.py restore"
echo "4. 使用补丁构建Chromium: python3 build_with_patches.py --random --build-args=\"ninja -C out/Default chrome\""
echo 

# 设置执行权限
chmod +x patch_manager.py fingerprint_generator.py build_with_patches.py

echo "脚本已设置执行权限，您现在可以直接运行 ./patch_manager.py 等命令"