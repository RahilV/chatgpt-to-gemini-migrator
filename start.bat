@echo off
echo ========================================
echo   ChatGPT to Gemini Migration Tool
echo ========================================
echo.

:menu
echo What would you like to do?
echo.
echo 1. View the Guide (open index.html)
echo 2. Run Migration (convert conversations)
echo 3. View Conversations (start viewer)
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto guide
if "%choice%"=="2" goto migrate
if "%choice%"=="3" goto view
if "%choice%"=="4" goto end
echo Invalid choice. Please try again.
echo.
goto menu

:guide
echo.
echo Opening guide in your browser...
start index.html
echo.
goto menu

:migrate
echo.
echo Running migration script...
echo.
python migrate_to_gemini.py
echo.
echo Migration complete!
echo.
pause
goto menu

:view
echo.
echo Starting conversation viewer...
echo Your browser will open automatically.
echo Press Ctrl+C to stop the server when done.
echo.
python view_conversations.py
goto menu

:end
echo.
echo Thank you for using ChatGPT to Gemini Migration Tool!
echo.
pause
