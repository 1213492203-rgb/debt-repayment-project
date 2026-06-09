@echo off
chcp 65001 >nul
echo ========================================
echo  关闭 Chrome 并用调试模式重开
echo  保留你所有登录状态和书签
echo ========================================
echo.

echo [1/2] 关闭现有 Chrome...
taskkill /F /IM chrome.exe >nul 2>&1
timeout /t 2 /nobreak >nul
echo        Chrome 已关闭

echo [2/2] 用调试端口启动 Chrome（使用你的真实配置）...
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --user-data-dir="C:\Users\Administrator\AppData\Local\Google\Chrome\User Data" ^
  --profile-directory="Default"

timeout /t 3 /nobreak >nul
echo.
echo ========================================
echo  Chrome 已启动！调试端口: 9222
echo  你可以正常浏览，脚本会连接过来自动操作
echo ========================================
