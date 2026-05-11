# 🚀 OSINT Tracker - Netlify Deployment Guide

## Step-by-Step Deployment Process

### 1. Create GitHub Repository
1. Go to [github.com](https://github.com) and sign in
2. Click "New repository"
3. Name it: `osint-tracker` or `osint-geolocation-tracker`
4. Make it **Public** (required for free Netlify deployment)
5. **DO NOT** initialize with README (we already have one)
6. Click "Create repository"

### 2. Push Code to GitHub
```bash
# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/osint-tracker.git

# Push to GitHub
git push -u origin master
```

### 3. Deploy to Netlify

#### Option A: One-Click Deploy (Recommended)
1. Go to [netlify.com](https://netlify.com)
2. Sign up/Login with GitHub
3. Click "Add new site" → "Import an existing project"
4. Choose "Deploy with GitHub"
5. Authorize Netlify to access your GitHub
6. Select your `osint-tracker` repository
7. Configure build settings:
   - **Branch to deploy:** `master` or `main`
   - **Build command:** `pip install -r requirements.txt && python -m streamlit run main.py --server.port $PORT --server.headless true`
   - **Publish directory:** (leave empty)
8. Click "Deploy site"

#### Option B: Static Export (Limited Functionality)
If you want a static version (loses interactivity):
```bash
# Install static export tool
pip install streamlit-pydantic

# Run static export
streamlit run main.py --server.headless true --server.runOnSave true

# In browser, save the page as HTML
# Then upload the HTML file to Netlify
```

### 4. Configure Netlify Settings
After deployment, go to Site Settings:
- **Domain:** Custom domain (optional)
- **Environment variables:** Add any secrets if needed
- **Build hooks:** For automatic redeployment on git push

### 5. Test Your Deployment
- Visit the Netlify-provided URL
- Test all features: Image upload, PDF analysis, phone validation
- Check that maps load correctly

## ⚠️ Important Notes

### Streamlit on Netlify Limitations:
- **Netlify is designed for static sites**, not Python apps
- **Full interactivity may not work** due to serverless limitations
- **File uploads might not work** in static export mode
- **Maps and dynamic content** may have issues

### Recommended Alternative: Streamlit Cloud
For the **best experience** with full functionality:
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Select `main.py` as the main file
4. Deploy instantly!

### Troubleshooting:
- **Build fails:** Check the build logs in Netlify dashboard
- **App doesn't load:** Verify Python version and dependencies
- **Features don't work:** Consider using Streamlit Cloud instead

## 🎉 Success!
Your OSINT Tracker will be live at: `https://your-site-name.netlify.app`

Need help with any step? Check the detailed logs in your Netlify dashboard!