#!/bin/bash
# OSINT Tracker - Complete Netlify Deployment Script

echo "🚀 OSINT Tracker - Complete Netlify Deployment"
echo "=============================================="
echo ""

# Check if repository exists
echo "Step 1: Checking GitHub repository..."
if git ls-remote https://github.com/rp31803/osint-tracker.git > /dev/null 2>&1; then
    echo "✅ Repository found!"
else
    echo "❌ Repository not found!"
    echo ""
    echo "📋 CREATE THE REPOSITORY FIRST:"
    echo "1. Go to https://github.com/new"
    echo "2. Sign in to GitHub"
    echo "3. Repository name: osint-tracker"
    echo "4. Make it PUBLIC"
    echo "5. DO NOT check any initialization options"
    echo "6. Click 'Create repository'"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Push to GitHub
echo ""
echo "Step 2: Pushing to GitHub..."
git push -u origin master

if [ $? -ne 0 ]; then
    echo "❌ Push failed. Please check your GitHub credentials."
    exit 1
fi

echo ""
echo "🎉 Successfully pushed to GitHub!"
echo ""
echo "Step 3: Netlify Deployment Instructions"
echo "======================================"
echo ""
echo "1. 🌐 Go to: https://netlify.com"
echo "2. 🔐 Sign up/Login with GitHub"
echo "3. ➕ Click 'Add new site' → 'Import an existing project'"
echo "4. 📚 Choose 'Deploy with GitHub'"
echo "5. 🔍 Select your 'osint-tracker' repository"
echo "6. ⚙️  Build settings (should auto-detect):"
echo "   - Branch: master"
echo "   - Build command: pip install -r requirements.txt && echo 'Ready'"
echo "   - Publish directory: build"
echo "7. 🚀 Click 'Deploy site'"
echo ""
echo "⏱️  Deployment will take 2-3 minutes..."
echo ""
echo "🎯 What you'll get:"
echo "   ✅ Professional landing page"
echo "   ✅ Links to full Streamlit app"
echo "   ✅ Free HTTPS"
echo "   ✅ Custom domain ready"
echo ""
echo "💡 Pro Tip: For full interactive features, also deploy to:"
echo "   https://share.streamlit.io (select main.py)"
echo ""
echo "🎊 Your OSINT Tracker is ready for the world!"