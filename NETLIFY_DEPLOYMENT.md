# OSINT Tracker - Netlify Deployment Guide

## 🚀 Deployment Options

Since this is a Streamlit application, here are your deployment options:

### Option 1: Streamlit Cloud (Recommended)
**Best for Streamlit apps** - Official platform, free tier available
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Deploy directly

### Option 2: Netlify Static Export
**Limited functionality** - Converts app to static HTML
```bash
# Install streamlit-pydantic (for static export)
pip install streamlit-pydantic

# Run static export
streamlit run main.py --server.headless true --server.runOnSave true
# Then use browser developer tools to save as HTML
```

### Option 3: Netlify Functions (Advanced)
**Full functionality** - Requires serverless setup

## 📋 Current App Status
- ✅ Streamlit 1.57.0
- ✅ All dependencies in requirements.txt
- ✅ Modular code structure
- ✅ Working locally

## 🔧 For Netlify Deployment:

1. **Create netlify.toml**
2. **Set up build commands**
3. **Configure environment variables**
4. **Deploy**

Would you like me to set up the Netlify configuration files?