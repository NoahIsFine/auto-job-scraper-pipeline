@echo off
echo ========================================================
echo Auto Job Scraper Pipeline - Task Scheduler Setup
echo ========================================================
echo.
echo This will create a Windows Scheduled Task to run the scraper
echo automatically every Monday at 9:00 AM.
echo.

:: %~dp0 gets the absolute path of the directory containing this script
set SCRIPT_DIR=%~dp0
set BAT_PATH=%SCRIPT_DIR%run_scraper.bat

schtasks /Create /SC WEEKLY /D MON /TN "Auto Job Scraper Pipeline" /TR "\"%BAT_PATH%\"" /ST 09:00 /F

echo.
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Scheduled task created successfully!
) else (
    echo [ERROR] Failed to create the scheduled task. 
    echo Please try right-clicking this file and selecting "Run as administrator".
)
echo.
pause
