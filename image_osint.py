import exifread
from PIL import Image
import os
import pypdf
import pdfplumber
from pdf2image import convert_from_bytes
import io
import re
import streamlit as st
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static
import numpy as np
from scipy import ndimage
import hashlib

def extract_image_data(image_file):
    """
    Extract EXIF data from an image file, including GPS coordinates and timestamp.

    Args:
        image_file: File-like object or path to image file

    Returns:
        dict: Dictionary containing extracted metadata
    """
    try:
        # Open image with PIL to get basic info
        img = Image.open(image_file)

        # Reset file pointer for exifread
        image_file.seek(0)

        # Extract EXIF data using exifread
        tags = exifread.process_file(image_file)

        result = {
            'filename': getattr(image_file, 'name', 'uploaded_image'),
            'image_size': img.size,
            'image_format': img.format,
            'datetime': None,
            'latitude': None,
            'longitude': None,
            'gps_available': False
        }

        # Extract DateTime
        if 'EXIF DateTimeOriginal' in tags:
            result['datetime'] = str(tags['EXIF DateTimeOriginal'])
        elif 'EXIF DateTime' in tags:
            result['datetime'] = str(tags['EXIF DateTime'])
        elif 'Image DateTime' in tags:
            result['datetime'] = str(tags['Image DateTime'])

        # Extract GPS coordinates
        if ('GPS GPSLatitude' in tags and
            'GPS GPSLatitudeRef' in tags and
            'GPS GPSLongitude' in tags and
            'GPS GPSLongitudeRef' in tags):

            result['gps_available'] = True

            # Convert GPS coordinates to decimal degrees
            lat_dms = str(tags['GPS GPSLatitude']).replace('[', '').replace(']', '').split(',')
            lon_dms = str(tags['GPS GPSLongitude']).replace('[', '').replace(']', '').split(',')

            if len(lat_dms) >= 3 and len(lon_dms) >= 3:
                # Parse degrees, minutes, seconds
                lat_deg = float(lat_dms[0])
                lat_min = float(lat_dms[1])
                lat_sec = float(lat_dms[2].split('/')[0]) / float(lat_dms[2].split('/')[1]) if '/' in lat_dms[2] else float(lat_dms[2])

                lon_deg = float(lon_dms[0])
                lon_min = float(lon_dms[1])
                lon_sec = float(lon_dms[2].split('/')[0]) / float(lon_dms[2].split('/')[1]) if '/' in lon_dms[2] else float(lon_dms[2])

                # Convert to decimal degrees
                latitude = lat_deg + (lat_min / 60.0) + (lat_sec / 3600.0)
                longitude = lon_deg + (lon_min / 60.0) + (lon_sec / 3600.0)

                # Apply hemisphere reference
                if str(tags['GPS GPSLatitudeRef']) == 'S':
                    latitude = -latitude
                if str(tags['GPS GPSLongitudeRef']) == 'W':
                    longitude = -longitude

                result['latitude'] = latitude
                result['longitude'] = longitude

        return result

    except Exception as e:
        return {
            'error': f"Failed to extract EXIF data: {str(e)}",
            'filename': getattr(image_file, 'name', 'uploaded_image') if hasattr(image_file, 'name') else 'unknown'
        }

def get_location_address(lat, lon):
    """
    Get human-readable address from GPS coordinates using reverse geocoding.

    Args:
        lat (float): Latitude
        lon (float): Longitude

    Returns:
        str: Human-readable address
    """
    try:
        from geopy.geocoders import Nominatim
        from geopy.exc import GeocoderTimedOut, GeocoderServiceError

        geolocator = Nominatim(user_agent="osint-tracker")
        location = geolocator.reverse(f"{lat}, {lon}", timeout=10)

        if location:
            return location.address
        else:
            return "Address not found"

    except GeocoderTimedOut:
        return "Geocoding timed out. Try again later."
    except GeocoderServiceError:
        return "Geocoding service unavailable."
    except Exception as e:
        return f"Error getting address: {str(e)}"

def generate_map(lat, lon):
    """
    Generate an interactive map with a marker at the given coordinates.

    Args:
        lat (float): Latitude
        lon (float): Longitude

    Returns:
        folium.Map: Interactive map object
    """
    try:
        import folium

        # Create map centered on the location
        m = folium.Map(location=[lat, lon], zoom_start=15)

        # Add marker
        folium.Marker(
            [lat, lon],
            popup=f"Location: {lat:.6f}, {lon:.6f}",
            tooltip="GPS Location"
        ).add_to(m)

        return m

    except Exception as e:
        print(f"Error generating map: {str(e)}")
        return None

def analyze_image_authenticity(image_file):
    """
    Analyze image for signs of manipulation using Error Level Analysis (ELA).

    Args:
        image_file: File-like object containing image data

    Returns:
        dict: Authenticity analysis results
    """
    try:
        # Read the original image
        original = Image.open(image_file)
        image_file.seek(0)  # Reset file pointer

        # Convert to RGB if necessary (for JPEG compression analysis)
        if original.mode not in ('RGB', 'L'):
            original = original.convert('RGB')

        # Save at different quality levels to detect compression artifacts
        temp_buffer_high = io.BytesIO()
        temp_buffer_low = io.BytesIO()

        # Save at high quality (95%)
        original.save(temp_buffer_high, format='JPEG', quality=95)
        temp_buffer_high.seek(0)

        # Save at low quality (70%)
        original.save(temp_buffer_low, format='JPEG', quality=70)
        temp_buffer_low.seek(0)

        # Reload images
        high_quality = Image.open(temp_buffer_high)
        low_quality = Image.open(temp_buffer_low)

        # Calculate difference (ELA)
        ela_image = Image.new('RGB', original.size)
        high_array = np.array(high_quality)
        low_array = np.array(low_quality)

        # Calculate absolute difference
        diff = np.abs(high_array.astype(np.int16) - low_array.astype(np.int16))
        diff = np.clip(diff, 0, 255).astype(np.uint8)

        ela_image = Image.fromarray(diff)

        # Analyze the ELA result
        ela_array = np.array(ela_image)
        mean_diff = np.mean(ela_array)
        std_diff = np.std(ela_array)
        max_diff = np.max(ela_array)

        # Calculate suspicious regions (high difference areas)
        threshold = mean_diff + 2 * std_diff
        suspicious_pixels = np.sum(ela_array > threshold)
        total_pixels = ela_array.size
        suspicious_ratio = suspicious_pixels / total_pixels

        # Determine authenticity score
        authenticity_score = 1.0 - min(suspicious_ratio * 10, 1.0)  # Scale and invert

        # Classify as real or fake
        if authenticity_score > 0.8:
            classification = "REAL"
            confidence = "High"
        elif authenticity_score > 0.6:
            classification = "LIKELY REAL"
            confidence = "Medium"
        elif authenticity_score > 0.4:
            classification = "SUSPICIOUS"
            confidence = "Medium"
        else:
            classification = "FAKE/MANIPULATED"
            confidence = "High"

        result = {
            'classification': classification,
            'confidence': confidence,
            'authenticity_score': round(authenticity_score * 100, 2),
            'mean_difference': round(mean_diff, 2),
            'std_difference': round(std_diff, 2),
            'max_difference': int(max_diff),
            'suspicious_pixels_ratio': round(suspicious_ratio * 100, 4),
            'analysis_method': 'Error Level Analysis (ELA)',
            'ela_image_available': True
        }

        # Store ELA image for display
        ela_buffer = io.BytesIO()
        ela_image.save(ela_buffer, format='PNG')
        ela_buffer.seek(0)
        result['ela_image_data'] = ela_buffer.getvalue()

        return result

    except Exception as e:
        return {
            'error': f"Authenticity analysis failed: {str(e)}",
            'classification': 'UNKNOWN',
            'confidence': 'N/A'
        }

def analyze_pdf_authenticity(pdf_file):
    """
    Analyze PDF for signs of tampering and authenticity.

    Args:
        pdf_file: File-like object containing PDF data

    Returns:
        dict: PDF authenticity analysis results
    """
    try:
        pdf_data = pdf_file.read()
        pdf_file.seek(0)  # Reset file pointer

        pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_data))

        result = {
            'file_integrity': 'UNKNOWN',
            'digital_signatures': [],
            'metadata_consistency': 'UNKNOWN',
            'suspicious_elements': [],
            'authenticity_score': 0,
            'classification': 'UNKNOWN'
        }

        # Check for digital signatures (simplified approach)
        try:
            signatures = []
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                # Check for signature fields in AcroForm
                if '/Annots' in page:
                    try:
                        annotations = page['/Annots']
                        # Handle both direct arrays and indirect references
                        if hasattr(annotations, 'get_object'):
                            annotations = annotations.get_object()

                        # If annotations is a list/array
                        if isinstance(annotations, list):
                            for annot_ref in annotations:
                                try:
                                    if hasattr(annot_ref, 'get_object'):
                                        annot = annot_ref.get_object()
                                    else:
                                        annot = annot_ref

                                    # Check if this is a signature widget
                                    if isinstance(annot, dict):
                                        subtype = annot.get('/Subtype')
                                        ft = annot.get('/FT')
                                        if subtype == '/Widget' and ft == '/Sig':
                                            signatures.append(f"Signature field on page {page_num + 1}")
                                except:
                                    continue
                    except:
                        pass

            result['digital_signatures'] = signatures
        except Exception as e:
            # If signature detection fails, just continue without signatures
            result['digital_signatures'] = []

        # Check metadata consistency
        metadata = pdf_reader.metadata
        if metadata:
            creation_date = metadata.get('/CreationDate', '')
            mod_date = metadata.get('/ModDate', '')

            # Check if modification date is after creation date
            if creation_date and mod_date:
                try:
                    # PDF dates are in format: D:YYYYMMDDHHMMSS or D:YYYYMMDDHHMMSS+HH'MM'
                    # Extract just the date part for comparison
                    def extract_date(date_str):
                        if isinstance(date_str, str) and date_str.startswith('D:'):
                            # Extract YYYYMMDD part
                            date_part = date_str[2:10]
                            if len(date_part) == 8 and date_part.isdigit():
                                return date_part
                        return None

                    creation_date_clean = extract_date(str(creation_date))
                    mod_date_clean = extract_date(str(mod_date))

                    if creation_date_clean and mod_date_clean:
                        if mod_date_clean < creation_date_clean:
                            result['metadata_consistency'] = 'INCONSISTENT'
                            result['suspicious_elements'].append('Modification date is before creation date')
                        else:
                            result['metadata_consistency'] = 'CONSISTENT'
                    else:
                        result['metadata_consistency'] = 'UNKNOWN'
                except:
                    result['metadata_consistency'] = 'UNKNOWN'
            else:
                result['metadata_consistency'] = 'UNKNOWN'

        # Check for JavaScript (potential security risk)
        try:
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                if '/AA' in page or '/OpenAction' in page:
                    result['suspicious_elements'].append(f'Auto-action on page {page_num + 1}')
        except:
            pass

        # Calculate authenticity score
        score = 50  # Base score

        if result['digital_signatures']:
            score += 30  # Signed documents are more trustworthy

        if result['metadata_consistency'] == 'CONSISTENT':
            score += 10
        elif result['metadata_consistency'] == 'INCONSISTENT':
            score -= 20

        if not result['suspicious_elements']:
            score += 10
        else:
            score -= len(result['suspicious_elements']) * 15

        score = max(0, min(100, score))
        result['authenticity_score'] = score

        # Classify based on score
        if score >= 80:
            result['classification'] = 'HIGHLY TRUSTWORTHY'
        elif score >= 60:
            result['classification'] = 'TRUSTWORTHY'
        elif score >= 40:
            result['classification'] = 'SUSPICIOUS'
        else:
            result['classification'] = 'UNTRUSTWORTHY'

        # File integrity check (basic)
        try:
            # Check if PDF structure is valid
            pdf_reader.pages  # This will raise an exception if PDF is corrupted
            result['file_integrity'] = 'VALID'
        except:
            result['file_integrity'] = 'CORRUPTED'
            result['classification'] = 'INVALID'
            score = 0

        return result

    except Exception as e:
        return {
            'error': f"PDF authenticity analysis failed: {str(e)}",
            'classification': 'UNKNOWN',
            'authenticity_score': 0
        }

def analyze_file_authenticity(uploaded_file):
    """
    Analyze any uploaded file for authenticity based on file type.

    Args:
        uploaded_file: Streamlit uploaded file object

    Returns:
        dict: Authenticity analysis results
    """
    file_extension = uploaded_file.name.split('.')[-1].lower() if '.' in uploaded_file.name else ''

    if file_extension in ['jpg', 'jpeg', 'png', 'bmp', 'tiff']:
        return analyze_image_authenticity(uploaded_file)
    elif file_extension == 'pdf':
        return analyze_pdf_authenticity(uploaded_file)
    else:
        return {
            'classification': 'UNSUPPORTED',
            'confidence': 'N/A',
            'error': f'Authenticity analysis not supported for .{file_extension} files'
        }

def extract_pdf_data(pdf_file):
    """
    Extract metadata and text content from a PDF file.

    Args:
        pdf_file: File-like object containing PDF data

    Returns:
        dict: PDF metadata and extracted information
    """
    try:
        # Read PDF content
        pdf_data = pdf_file.read()
        pdf_file.seek(0)  # Reset file pointer

        # Create PDF reader object
        pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_data))

        # Extract metadata
        metadata = pdf_reader.metadata
        result = {
            'filename': getattr(pdf_file, 'name', 'uploaded_pdf') if hasattr(pdf_file, 'name') else 'unknown',
            'file_type': 'PDF',
            'num_pages': len(pdf_reader.pages),
            'metadata': {}
        }

        # Extract basic metadata
        if metadata:
            result['metadata'] = {
                'title': metadata.get('/Title', 'N/A'),
                'author': metadata.get('/Author', 'N/A'),
                'subject': metadata.get('/Subject', 'N/A'),
                'creator': metadata.get('/Creator', 'N/A'),
                'producer': metadata.get('/Producer', 'N/A'),
                'creation_date': metadata.get('/CreationDate', 'N/A'),
                'modification_date': metadata.get('/ModDate', 'N/A')
            }

        # Extract text from all pages using pdfplumber for better accuracy
        full_text = ""
        try:
            with pdfplumber.open(io.BytesIO(pdf_data)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n\n"
        except Exception as e:
            result['text_extraction_error'] = f"Error extracting text: {str(e)}"

        result['extracted_text'] = full_text.strip()
        result['text_length'] = len(full_text)

        # Try to extract phone numbers from text
        phone_pattern = r'[\+]?[1-9]?[0-9]{1,4}?[\s\-\.]?[\(]?[0-9]{1,3}[\)]?[\s\-\.]?[0-9]{3,4}[\s\-\.]?[0-9]{3,4}'
        phones_found = re.findall(phone_pattern, full_text)
        if phones_found:
            result['potential_phone_numbers'] = list(set(phones_found))

        # Try to extract email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails_found = re.findall(email_pattern, full_text)
        if emails_found:
            result['potential_emails'] = list(set(emails_found))

        # Try to extract URLs
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls_found = re.findall(url_pattern, full_text)
        if urls_found:
            result['potential_urls'] = list(set(urls_found))

        # Convert first page to image for potential EXIF analysis
        try:
            images = convert_from_bytes(pdf_data, first_page=1, last_page=1)
            if images:
                # Save first page as image for EXIF analysis
                img_byte_arr = io.BytesIO()
                images[0].save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)

                # Create a file-like object for EXIF analysis
                class FakeFile:
                    def __init__(self, data, name):
                        self.data = data
                        self.name = name

                    def read(self):
                        return self.data

                    def seek(self, pos):
                        pass

                fake_image_file = FakeFile(img_byte_arr.getvalue(), "pdf_page_1.png")

                # Try to extract EXIF from the converted image
                page_exif = extract_image_data(fake_image_file)
                if 'latitude' in page_exif and 'longitude' in page_exif:
                    result['page_gps_data'] = {
                        'latitude': page_exif['latitude'],
                        'longitude': page_exif['longitude']
                    }
        except Exception as e:
            result['image_conversion_error'] = f"Could not convert PDF page to image: {str(e)}"

        return result

    except Exception as e:
        return {
            'error': f"Failed to process PDF: {str(e)}",
            'filename': getattr(pdf_file, 'name', 'uploaded_pdf') if hasattr(pdf_file, 'name') else 'unknown'
        }