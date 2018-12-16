C:/msys64/usr/bin/bash.exe -c "./make-daty-installer stage1"
if errorlevel 1 (
exit /b %errorlevel%
)

C:/msys64/usr/bin/bash.exe -c "./make-daty-installer stage2"
if errorlevel 1 (
exit /b %errorlevel%
)
