@echo off

set "_root=%~dp0"
set "_root=%_root:~0,-1%"
echo "%_root%"
cd /d "%_root%"

set "_pyBin=%_root%\runtime"
set "PATH=%_root%\site-packages;%_pyBin%;%_root%\scripts\backend;%PATH%"

IF %ERRORLEVEL% NEQ 0 goto error
call cd backend && start cmd /k "python app.py"
start /d %_root%\frontend npm run start-vue
goto end

:error
echo npm install failed with error %ERRORLEVEL%
exit /B %ERRORLEVEL%

:end
echo npm package update successfully