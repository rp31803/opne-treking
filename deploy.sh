#!/bin/bash
# OSINT Tracker - Netlify Deployment Script

echo "🚀 OSINT Tracker Deployment Options"
echo "=================================="
echo ""
echo "This Streamlit app has several deployment options:"
echo ""

# Option 1: Streamlit Cloud (Recommended)
echo "1️⃣ RECOMMENDED: Streamlit Cloud"
echo "   - Official platform for Streamlit apps"
echo "   - Free tier available"
echo "   - Easy GitHub integration"
echo ""
echo "   Steps:"
echo "   1. Go to https://share.streamlit.io"
echo "   2. Connect your GitHub repository"
echo "   3. Select main.py as the main file"
echo "   4. Deploy!"
echo ""

# Option 2: Netlify Static Export
echo "2️⃣ Netlify Static Export (Limited)"
echo "   - Converts to static HTML"
echo "   - Loses interactive features"
echo "   - Good for demos only"
echo ""
echo "   To create static export:"
echo "   pip install streamlit-pydantic"
echo "   streamlit run main.py --server.headless true"
echo "   Then save the page as HTML"
echo ""

# Option 3: Netlify Functions (Advanced)
echo "3️⃣ Netlify Functions (Full Features)"
echo "   - Requires serverless function setup"
echo "   - Complex but maintains all functionality"
echo "   - Requires Python runtime configuration"
echo ""

echo "📋 Current Configuration:"
echo "   - netlify.toml: Build configuration"
echo "   - package.json: Node.js dependencies"
echo "   - _redirects: Routing rules"
echo "   - requirements.txt: Python dependencies"
echo ""

echo "🔧 Next Steps:"
echo "   1. Push code to GitHub repository"
echo "   2. Connect repository to Netlify"
echo "   3. Configure build settings:"
echo "      - Build command: pip install -r requirements.txt && streamlit run main.py"
echo "      - Publish directory: (leave empty for functions)"
echo "   4. Add environment variables if needed"
echo ""

echo "⚠️  Note: For full Streamlit functionality, consider Streamlit Cloud instead of Netlify."
echo "   Netlify is better suited for static sites, not Python web apps."