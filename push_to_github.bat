@echo off
REM OSINT Tracker - GitHub & Netlify Deployment Script (Windows)
echo 🚀 OSINT Tracker Deployment Script
echo ==================================
echo.

REM Step 1: GitHub Setup
echo Step 1: Setting up GitHub repository
echo -----------------------------------
echo 1. Go to https://github.com and create a new repository named 'osint-tracker'
echo 2. Make it PUBLIC (required for free Netlify deployment)
echo 3. DO NOT initialize with README or .gitignore
echo 4. Copy the repository URL
echo.

REM Ask for GitHub username
set /p GITHUB_USER="Enter your GitHub username: "

if "%GITHUB_USER%"=="" (
    echo ❌ GitHub username is required
    pause
    exit /b 1
)

set REPO_URL=https://github.com/%GITHUB_USER%/osint-tracker.git

echo Setting up remote repository: %REPO_URL%
git remote add origin %REPO_URL%

echo Pushing to GitHub...
git push -u origin master

if %ERRORLEVEL% EQU 0 (
    echo ✅ Successfully pushed to GitHub!
    echo.
    echo Step 2: Netlify Deployment
    echo -------------------------
    echo 1. Go to https://netlify.com
    echo 2. Sign up/Login with GitHub
    echo 3. Click 'Add new site' → 'Import an existing project'
    echo 4. Choose 'Deploy with GitHub'
    echo 5. Select your 'osint-tracker' repository
    echo 6. Configure build settings:
    echo    - Branch: master
    echo    - Build command: pip install -r requirements.txt ^&^& python -m streamlit run main.py --server.port $PORT --server.headless true
    echo    - Publish directory: (leave empty)
    echo 7. Click 'Deploy site'
    echo.
    echo ⚠️  Note: For full Streamlit functionality, consider Streamlit Cloud instead:
    echo    https://share.streamlit.io
    echo.
    echo 🎉 Your code is ready for deployment!
) else (
    echo ❌ Failed to push to GitHub. Please check your credentials and try again.
    echo You can also push manually with:
    echo git remote add origin %REPO_URL%
    echo git push -u origin master
)

echo.
pause