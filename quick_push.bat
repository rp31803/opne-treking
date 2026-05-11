@echo off
REM Quick GitHub Push Script for OSINT Tracker
echo 🚀 OSINT Tracker - GitHub Push Script
echo =====================================
echo.

echo Checking if repository exists...
git ls-remote https://github.com/rp31803/osint-tracker.git >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Repository not found!
    echo.
    echo 📋 Please create the repository first:
    echo 1. Go to https://github.com/new
    echo 2. Repository name: osint-tracker
    echo 3. Make it PUBLIC
    echo 4. DO NOT check any initialization options
    echo 5. Click "Create repository"
    echo.
    echo Then run this script again.
    pause
    exit /b 1
)

echo ✅ Repository found! Pushing code...
git push -u origin master

if %errorlevel% equ 0 (
    echo.
    echo 🎉 Successfully pushed to GitHub!
    echo.
    echo 🚀 Next Steps:
    echo 1. Go to https://netlify.com
    echo 2. Sign up/Login with GitHub
    echo 3. Click "Add new site" → "Import an existing project"
    echo 4. Choose "Deploy with GitHub"
    echo 5. Select "osint-tracker" repository
    echo 6. Deploy!
    echo.
    echo 💡 Alternative: Use Streamlit Cloud for full functionality
    echo    https://share.streamlit.io
) else (
    echo ❌ Push failed. Please check your credentials.
)

echo.
pause