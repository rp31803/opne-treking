@echo off
REM Netlify Troubleshooting Script
echo 🔧 OSINT Tracker - Netlify Troubleshooting
echo =========================================
echo.

echo Step 1: Checking local files...
if exist "build\index.html" (
    echo ✅ Build directory exists with index.html
) else (
    echo ❌ Build directory missing - run setup first
    pause
    exit /b 1
)

echo.
echo Step 2: Checking GitHub repository...
git ls-remote https://github.com/rp31803/opne-treking.git >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ GitHub repository accessible
) else (
    echo ❌ Cannot access GitHub repository
    echo    - Check if repository exists
    echo    - Verify repository name: opne-treking
    echo    - Check your internet connection
)

echo.
echo Step 3: Netlify Troubleshooting Steps:
echo =====================================
echo.
echo If your Netlify site shows "Not Found":
echo.
echo 1. 🔍 CHECK SITE STATUS:
echo    - Go to netlify.com dashboard
echo    - Find your site (opne-treking)
echo    - Check if build succeeded or failed
echo.
echo 2. 🚀 REDEPLOY OPTIONS:
echo.
echo    Option A - Auto Redeploy:
echo    - Click "Deploy site" in Netlify dashboard
echo    - Wait for build completion
echo.
echo    Option B - Manual Deploy:
echo    - In Netlify: "Sites" → "Deploy manually"
echo    - Drag and drop the "build" folder
echo    - Click "Deploy"
echo.
echo    Option C - Clear Cache:
echo    - Site settings → "Build & deploy"
echo    - Click "Clear cache and deploy site"
echo.
echo 3. ⚙️ VERIFY BUILD SETTINGS:
echo    - Branch: master
echo    - Build command: echo 'Static site ready - no build needed'
echo    - Publish directory: build
echo.
echo 4. 🌐 CHECK SITE URL:
echo    - Your URL should be: https://[sitename].netlify.app
echo    - If wrong, go to Site settings → Domain management
echo.
echo 5. 🔧 IF BUILD FAILS:
echo    - Check build logs in Netlify dashboard
echo    - Look for specific error messages
echo    - Try the manual deploy option above

echo.
echo 💡 QUICK FIXES:
echo ===============
echo.
echo • Make sure repository is PUBLIC on GitHub
echo • Check that build/ folder contains index.html
echo • Try manual deploy as fallback
echo • Clear Netlify cache and redeploy
echo.
echo 📞 NEED HELP?
echo =============
echo.
echo If issues persist:
echo 1. Check Netlify build logs for specific errors
echo 2. Try creating a new site with same repository
echo 3. Use Streamlit Cloud instead: https://share.streamlit.io

echo.
echo 🎯 EXPECTED RESULT:
echo ==================
echo Your site should show a professional landing page
echo with buttons to deploy the full app on Streamlit Cloud.

echo.
pause