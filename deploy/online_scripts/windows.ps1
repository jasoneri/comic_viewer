# 检查是否以管理员权限运行
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Output "需要管理员权限运行此脚本"
    Start-Process powershell.exe -Verb RunAs -ArgumentList "-File `"$PSCommandPath`""
    exit
}

# 获取项目路径
$proj_p = Get-Location

# 1. 检查并安装 Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Output "未找到 Python，正在安装 Python 3.12..."
    $pythonInstaller = "python-3.12.3-amd64.exe"
    $pythonUrl = "https://www.python.org/ftp/python/3.12.3/$pythonInstaller"
    $installerPath = Join-Path $env:TEMP $pythonInstaller
    
    Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath
    Start-Process -FilePath $installerPath -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1" -Wait
    Remove-Item $installerPath
    
    # 刷新环境变量
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# 2. 安装 uv
Write-Output "正在安装 uv..."
python -m pip install uv

# 3. 使用 uv 安装后端依赖
Write-Output "正在安装后端依赖..."
python -m uv pip install -r "backend/requirements.txt"

# 4. 检查并安装 Node.js
$npm = Get-Command npm -ErrorAction SilentlyContinue
if (-not $npm) {
    Write-Output "未找到 Node.js，正在安装最新版本..."
    $nodeInstaller = "node-v20.11.1-x64.msi"
    $nodeUrl = "https://nodejs.org/dist/v20.11.1/$nodeInstaller"
    $installerPath = Join-Path $env:TEMP $nodeInstaller
    
    Invoke-WebRequest -Uri $nodeUrl -OutFile $installerPath
    Start-Process -FilePath "msiexec.exe" -ArgumentList "/i", $installerPath, "/quiet", "/norestart" -Wait
    Remove-Item $installerPath
    
    # 刷新环境变量
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# 5. 安装前端依赖
Write-Output "正在安装前端依赖..."
Set-Location frontend
npm i
Set-Location $proj_p

Write-Output "所有依赖安装完成！"
pause 