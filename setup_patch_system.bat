@echo off
echo ===== Chromium指纹补丁管理系统初始化 =====
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 错误: 未找到Python，请先安装Python 3.6+
    exit /b 1
)

REM 检查Git是否安装
git --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 警告: 未找到Git，某些补丁功能可能无法正常工作
)

REM 创建必要的目录
if not exist patches mkdir patches
if not exist configs mkdir configs
if not exist backups mkdir backups

REM 运行初始化脚本
python setup_patch_system.py

echo.
echo ===== 初始化完成 =====
echo.
echo 您可以使用以下命令：
echo 1. 生成随机指纹配置: python fingerprint_generator.py
echo 2. 应用指纹补丁: python patch_manager.py apply --config=configs/template.json
echo 3. 还原补丁: python patch_manager.py restore
echo 4. 使用补丁构建Chromium: python build_with_patches.py --random --build-args="ninja -C out/Default chrome"
echo.

pause