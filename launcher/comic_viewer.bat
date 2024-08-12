@echo off

set "_root=%~dp0"
set "_root=%_root:~0,-1%"
echo "%_root%"
cd /d "%_root%"

set "_pyBin=%_root%\runtime"
set "PATH=%_root%\site-packages;%_pyBin%;%PATH%"

python scripts/deploy/init.py

echo 检查npm包更新...
call cd scripts/frontend && call npm i
IF %ERRORLEVEL% NEQ 0 goto error
call cd ../backend && start cmd /k "python app.py"
start /d %_root%\scripts\frontend npm run start-vue

:error
exit /B %ERRORLEVEL%
