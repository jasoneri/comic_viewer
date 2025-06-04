Clear-Host
Write-Host @"
                              
                          ,---. 
                         /__./| 
                    ,---.;  ; | 
          __  ,-.  /___/ \  | | 
        ,' ,'/ /|  \   ;  \ ' | 
        '  | |' |   \   \  \: | 
        |  |   ,'    ;   \  ' . 
        '  :  /       \   \   ' 
        |  | '         \   `   ; 
        ;  : |          :   \ | 
         ---'            '---"  
"@  -ForegroundColor Red

# ===== 初始化变量 =====
$originalWorkingDir = Get-Location
$owner = "jasoneri"
$repo = "redViewer"
$realProjPath = Join-Path $originalWorkingDir $repo
$releasesApiUrl = "https://api.github.com/repos/$owner/$repo/releases"
$script:updateInfo = {
    UpdateAvailable = $false
    LatestTag = $null
}

# ===== 环境检查函数 =====
function Test-Environment {
    $envMissing = $false
    
    # 检查Python
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Output "❌ Python未安装"
        $envMissing = $true
    }
    
    # 检查Node.js
    if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
        Write-Output "❌ Node.js未安装"
        $envMissing = $true
    }
    
    return $envMissing
}
function Install-Environment {
    # 检查是否以管理员权限运行
    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if (-not $isAdmin) {
        $currentDir = Get-Location
        Write-Output "请求管理员权限安装环境..."
        Start-Process powershell.exe -Verb RunAs -ArgumentList "-NoExit -Command `"cd '$currentDir'; & '$PSCommandPath' --install-env`""
        exit
    }
    
    # 安装Python
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Output "下载 Python 3.12 中..."
        $pythonInstaller = "python-3.12.3-amd64.exe"
        $pythonUrl = "https://mirrors.huaweicloud.com/python/3.12.3/$pythonInstaller"
        $installerPath = Join-Path $originalWorkingDir $pythonInstaller
        $pythonInstallDir = Join-Path $originalWorkingDir "python3.12"
        if (-not (Test-Path $pythonInstallDir)) { 
            New-Item -ItemType Directory -Path $pythonInstallDir -Force | Out-Null 
        }
        Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath
        Write-Output "安装 Python 3.12 中..."
        Start-Process -FilePath $installerPath -Wait
        Remove-Item $installerPath
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

    }
    
    # 安装Node.js
    if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
        Write-Output "下载 Node.js 中..."
        $nodeInstaller = "node-v22.16.0-x64.msi"
        $nodeUrl = "https://npmmirror.com/mirrors/node/v22.16.0/$nodeInstaller"
        $installerPath = Join-Path $originalWorkingDir $nodeInstaller
        $nodeInstallDir = Join-Path $originalWorkingDir "nodejs22"
        if (-not (Test-Path $nodeInstallDir)) { 
            New-Item -ItemType Directory -Path $nodeInstallDir -Force | Out-Null 
        }
        Invoke-WebRequest -Uri $nodeUrl -OutFile $installerPath

        Write-Output "安装 Node.js 中..."
        Start-Process -FilePath "msiexec.exe" -ArgumentList "/i", $installerPath -Wait
        Remove-Item $installerPath
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        npm config set registry https://mirrors.huaweicloud.com/repository/npm/ 
    }
    
    # 刷新环境变量
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
}
# 处理环境安装参数
if ($args -contains "--install-env") {
    Install-Environment
    exit
}
# 检查环境
if (Test-Environment) {
    Write-Output "缺少必要环境，将优先安装..."
    Install-Environment
}

# ===== 0.1 最小化安装uv和packaging =====
$hasPackaging = python -c "import uv; print('installed')" 2>$null
if (-not $hasPackaging) {
    python -m pip install uv  -i http://mirrors.aliyun.com/pypi/simple/
}
$hasPackaging = python -c "import packaging; print('installed')" 2>$null
if (-not $hasPackaging) {
    python -m uv pip install packaging --index-url http://mirrors.aliyun.com/pypi/simple/
}

# ===== 1. 检查更新函数 =====
function Test-Update {
    try {
        $response = Invoke-RestMethod -Uri $releasesApiUrl -Method Get -ErrorAction Stop
        $latestTag = $response[0].tag_name
        # 检查本地版本image.png
        $localVerPath = Join-Path $originalWorkingDir "ver.txt"
        $updateAvailable = $false

        if (Test-Path $localVerPath) {
            $localVer = (Get-Content $localVerPath -Raw).Trim()
            # 使用Python比较版本
            $isNewer = python -c "from packaging.version import parse; print(parse('$latestTag') > parse('$localVer'))"
            if ($isNewer -eq "True") {
                Write-Host "`n═════════════════════════════════════" -ForegroundColor Green
                Write-Host "🎁 发现新版本: $latestTag" -ForegroundColor Green -BackgroundColor Black
                Write-Host "═════════════════════════════════════" -ForegroundColor Green
                $updateAvailable = $true
            }
        }
        else {
            $updateAvailable = $true
        }
        $script:updateInfo = @{
            UpdateAvailable = $updateAvailable
            LatestTag = $latestTag
        }
    }
    catch {
        Write-Output "❌ 检查更新失败: $($_.Exception.Message)"
    }
}

# ===== 2. 更新函数 =====
function Invoke-Update {
    # 使用全局变量获取最新版本
    $latestTag = $script:updateInfo.LatestTag
    if (-not $latestTag) {
        Write-Host "❌ 无法获取最新版本标签" -ForegroundColor Red
        return $null
    }
    
    try {
        # 询问是否启用加速
        $speedPrefix = ""
        $enableSpeed = Read-Host "是否启用加速？(y/n)"
        if ($enableSpeed -eq 'y') {
            $speedUrl = Read-Host "请粘贴格式链接（进 github.akams.cn 输入任意字符获取，例如：https://aaaa.bbbb/https/114514）"
            if ($speedUrl -match '(https?://[^/]+)') {
                $speedPrefix = $Matches[1]
                Write-Output "✈️ 加速前缀: $speedPrefix"
            }
            else {
                Write-Output "❌ 链接格式无效，不使用加速"
            }
        }
        # 构建下载URL
        $downloadUrl = "https://github.com/$owner/$repo/archive/refs/tags/$latestTag.zip"
        if ($speedPrefix) { 
            $downloadUrl = "$speedPrefix/https://github.com/$owner/$repo/archive/refs/tags/$latestTag.zip"
        }
        
        # 2.1 下载源码
        $zipPath = Join-Path $originalWorkingDir "$repo-$latestTag.zip"
        Write-Output "正在下载源码.s.."
        Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath
        
        # 2.2 解压源码
        $tmpDir = Join-Path $originalWorkingDir "tmp"
        if (-not (Test-Path $realProjPath)) { 
            New-Item -ItemType Directory -Path $realProjPath -Force | Out-Null 
        }
        if (-not (Test-Path $tmpDir)) { 
            New-Item -ItemType Directory -Path $tmpDir -Force | Out-Null 
        }
        Expand-Archive -Path $zipPath -DestinationPath $tmpDir -Force
        
        # 2.3 剪切覆盖到目标目录
        $tmpProjTagDir = Get-ChildItem -Path $tmpDir -Directory | Select-Object -First 1
        Get-ChildItem -Path $tmpProjTagDir.FullName | Move-Item -Destination $realProjPath -Force
        Remove-Item -LiteralPath $tmpDir -Force -Recurse -ErrorAction SilentlyContinue
        # 记录新版本到原始目录
        $latestTag | Out-File (Join-Path $originalWorkingDir "ver.txt") -Encoding utf8
        Write-Host "✅ 代码已更换至新版..."

        # 获取当前项目路径
        Set-Location $realProjPath
        
        # 2.4 使用uv安装后端依赖
        Write-Output "正在安装后端依赖..."
        python -m uv pip install -r "backend/requirements/windows.txt" --index-url http://mirrors.aliyun.com/pypi/simple/
        
        # 2.5 安装前端依赖
        Write-Output "正在安装前端依赖..."
        Set-Location frontend
        npm i
        Set-Location $originalWorkingDir
        Write-Host "✅ 更新至版本: $($script:updateInfo.LatestTag)" -ForegroundColor Green
        return 
    }
    catch {
        Write-Output "❌ 更新失败: $($_.Exception.Message)"
        return $null
    }
}

# ===== 3. 运行函数 =====
function Start-RedViewer {
    
    try {
        Set-Location $realProjPath
        Write-Host "🔖TIP: 退出请直接关闭终端窗口" -ForegroundColor Yellow
        Write-Output "正在启动RedViewer..."
        Set-Location (Join-Path $realProjPath "frontend")
        npm start
        
        Set-Location $originalWorkingDir
    }
    catch {
        Write-Output "❌ 启动失败: $($_.Exception.Message)"
    }
}

# ===== 主程序 =====
# 检查更新
Test-Update

# 用户选择菜单
while ($true) {

    Write-Host "`n————————————" -ForegroundColor Cyan
    Write-Host "|  主菜单  |" -ForegroundColor Cyan
    Write-Host "————————————" -ForegroundColor Cyan
    Write-Host "`n1: ♻️  更新/部署"
    Write-Host "2: 🚀 运行"
    Write-Host "其他任意键: 🔚 退出`n"
    
    $choice = Read-Host "请选择操作，然后按回车"
    
    switch ($choice) {
        '1' { # 更新
            if (-not $updateInfo.UpdateAvailable) {
                Write-Host "⏹️ 本地已是最新版本" -ForegroundColor Yellow
                $force = Read-Host "是否强制重新安装? (y/n)"
                if ($force -ne 'y') {
                    continue
                } else {
                    Write-Output "正在清理本地redViewer"
                    Remove-Item -LiteralPath $realProjPath -Force -Recurse -ErrorAction SilentlyContinue
                }
            }
            # 执行更新
            Invoke-Update
        }
        '2' { # 运行
            if (-not (Test-Path $realProjPath)) {
                Write-Host "❌ 未找到本地安装[$realProjPath]，请先部署" -ForegroundColor Red
                continue
            } else {
                Start-RedViewer
            }
        }
        default {
            exit
        }
    }
}