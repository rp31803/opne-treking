# OSINT Geolocation & Phone Tracker

A comprehensive Open Source Intelligence (OSINT) tool built with Python and Streamlit for analyzing images and phone numbers.

## Features

### 📸 Image Analysis
- Extract EXIF metadata from images (timestamps, camera info, etc.)
- GPS coordinate extraction and reverse geocoding
- Interactive location maps
- Support for JPG, PNG, TIFF, BMP formats

### 📄 PDF Analysis
- Extract metadata (title, author, creation date, etc.)
- Full text extraction from PDF documents
- Automatic detection of phone numbers, emails, and URLs
- Convert PDF pages to images for GPS analysis
- Support for PDF documents

### 📱 Phone Number Analysis
- Validate phone numbers globally
- Extract carrier and region information
- Determine line type (mobile, fixed, etc.)
- Timezone information

## Installation

1. Clone or download the project files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. For PDF processing, ensure you have poppler installed:
   - **Windows**: Download from https://blog.alivate.com.au/poppler-windows/
   - **macOS**: `brew install poppler`
   - **Linux**: `sudo apt-get install poppler-utils`

## Usage

Run the Streamlit application:
```bash
streamlit run main.py
```

The app will open in your browser with two main tabs:

### Image/PDF Analysis Tab
- Upload image files (JPG, PNG, TIFF, BMP) or PDF documents
- Click "Analyze File" to extract metadata and location data
- View GPS coordinates, timestamps, and interactive maps
- For PDFs: see extracted text, potential contacts, and metadata

### Phone Tracker Tab
- Enter phone numbers with or without country codes
- Select default country for parsing
- Get carrier, region, and validation information

## Requirements

- Python 3.8+
- Internet connection (for geocoding services)
- Poppler (for PDF processing)

## Dependencies

- streamlit: Web interface
- Pillow: Image processing
- exifread: EXIF data extraction
- phonenumbers: Phone number parsing
- geopy: Geocoding and reverse geocoding
- folium: Interactive maps
- PyPDF2: PDF metadata extraction
- pdfplumber: Advanced PDF text extraction
- pdf2image: PDF to image conversion

## Security Note

This tool is designed for ethical OSINT research and educational purposes. Always ensure you have proper authorization before analyzing files or phone numbers that don't belong to you.

## 🚀 Deployment Options

### Recommended: Streamlit Cloud (Easiest)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Select `main.py` as the main file
4. Deploy instantly with a public URL

### Alternative: Netlify (Advanced)
**Note:** Netlify is primarily for static sites. For full Streamlit functionality, use Streamlit Cloud instead.

1. **Static Export (Limited functionality):**
   ```bash
   pip install streamlit-pydantic
   streamlit run main.py --server.headless true
   # Save as HTML from browser
   ```

2. **Serverless Functions (Full functionality):**
   - Requires complex serverless setup
   - Use the provided `netlify.toml` configuration
   - Set up Python runtime in Netlify functions

## Project Structure

```
osint-tracker/
├── main.py                 # Main Streamlit application
├── image_osint.py          # Image and PDF analysis functions
├── phone_osint.py          # Phone number analysis functions
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── netlify.toml           # Netlify configuration
├── package.json           # Node.js configuration
├── _redirects             # Netlify routing
├── deploy.sh              # Deployment script
└── .streamlit/
    └── config.toml        # Streamlit configuration
```