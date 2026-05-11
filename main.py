import streamlit as st
import json
from image_osint import extract_image_data, extract_pdf_data, get_location_address, generate_map, analyze_file_authenticity
from phone_osint import analyze_phone_number

def main():
    st.title("🕵️ OSINT Geolocation & Phone Tracker")
    st.markdown("Open Source Intelligence tool for analyzing images and phone numbers")

    # Add tabs for different functionalities
    tab1, tab2, tab3 = st.tabs(["📸 Image Analysis", "📄 Document Analysis", "🔍 Authenticity Check"])

    with tab1:
        st.header("Image EXIF Analysis")
        st.write("Upload an image to extract GPS coordinates, timestamps, and location data.")
        st.markdown("---")

        # File upload (images only)
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['jpg', 'jpeg', 'png', 'tiff', 'bmp'],
            help="Upload an image with EXIF data to analyze GPS coordinates and metadata"
        )

        if uploaded_file is not None:
            # Display the uploaded image
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

            # Analyze button
            if st.button("🔍 Analyze Image", type="primary", key="analyze_image_btn"):
                with st.spinner("Analyzing image..."):
                    # Process image
                    file_data = extract_image_data(uploaded_file)

                    # Display results
                    st.success("Analysis Complete!")

                    # Basic image info
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Filename", file_data.get('filename', 'N/A'))
                    with col2:
                        st.metric("Type", file_data.get('file_type', 'Image'))
                    with col3:
                        size = file_data.get('image_size', (0,0))
                        st.metric("Size", f"{size[0]}x{size[1]}")

                    # Image-specific analysis display
                    st.subheader("📋 EXIF Metadata")

                    if 'error' in file_data:
                        st.error(f"Error: {file_data['error']}")
                    else:
                        # Timestamp
                        if file_data.get('datetime'):
                            st.write(f"**📅 Timestamp:** {file_data['datetime']}")
                        else:
                            st.write("**📅 Timestamp:** Not found")

                        # GPS Data
                        if file_data.get('gps_available'):
                            st.write(f"**📍 GPS Available:** Yes")
                            st.write(f"**Latitude:** {file_data.get('latitude', 'N/A'):.6f}")
                            st.write(f"**Longitude:** {file_data.get('longitude', 'N/A'):.6f}")

                            # Reverse geocoding
                            with st.spinner("Getting location address..."):
                                address = get_location_address(
                                    file_data['latitude'],
                                    file_data['longitude']
                                )
                            st.write(f"**🏠 Address:** {address}")

                            # Generate map
                            st.subheader("🗺️ Location Map")
                            with st.spinner("Generating map..."):
                                m = generate_map(file_data['latitude'], file_data['longitude'])
                                if m:
                                    folium_static(m, key="image_map")
                                else:
                                    st.error("Could not generate map")

                        else:
                            st.write("**📍 GPS Available:** No")
                            st.info("This image does not contain GPS location data.")

                    # Raw JSON data
                    with st.expander("📄 Raw Analysis Data"):
                        st.json(file_data)

    with tab2:
        st.header("Document & Phone Analysis")
        st.write("Analyze PDF documents and phone numbers for intelligence gathering.")
        st.markdown("---")

        # Sub-tabs for document and phone analysis
        sub_tab1, sub_tab2 = st.tabs(["📄 PDF Analysis", "📱 Phone Tracker"])

        with sub_tab1:
            st.subheader("PDF Document Analysis")
            pdf_file = st.file_uploader(
                "Choose a PDF file",
                type=['pdf'],
                help="Upload a PDF document to analyze metadata, text, and extract intelligence",
                key="pdf_uploader"
            )

            if pdf_file is not None:
                st.write(f"**Filename:** {pdf_file.name}")
                st.write(f"**File size:** {len(pdf_file.getvalue()) / 1024:.1f} KB")

                if st.button("🔍 Analyze PDF", type="primary", key="analyze_pdf_btn"):
                    with st.spinner("Analyzing PDF document..."):
                        pdf_data = extract_pdf_data(pdf_file)

                        st.success("PDF Analysis Complete!")

                        # Basic PDF info
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Pages", pdf_data.get('num_pages', 'N/A'))
                        with col2:
                            st.metric("Text Length", pdf_data.get('text_length', 0))
                        with col3:
                            st.metric("Type", pdf_data.get('file_type', 'PDF'))

                        if 'error' in pdf_data:
                            st.error(f"Error: {pdf_data['error']}")
                        else:
                            # PDF-specific analysis display
                            st.subheader("📋 PDF Metadata")

                            metadata = pdf_data.get('metadata', {})
                            if metadata:
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write(f"**📖 Title:** {metadata.get('title', 'N/A')}")
                                    st.write(f"**👤 Author:** {metadata.get('author', 'N/A')}")
                                    st.write(f"**📝 Subject:** {metadata.get('subject', 'N/A')}")
                                with col2:
                                    st.write(f"**🛠️ Creator:** {metadata.get('creator', 'N/A')}")
                                    st.write(f"**🏭 Producer:** {metadata.get('producer', 'N/A')}")
                                    st.write(f"**📅 Created:** {metadata.get('creation_date', 'N/A')}")

                            # Text content
                            extracted_text = pdf_data.get('extracted_text', '')
                            if extracted_text:
                                st.subheader("📄 Extracted Text")
                                preview_text = extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text
                                st.text_area("Text Content", preview_text, height=200, disabled=True, key="pdf_text_area")
                                st.write(f"**Total characters:** {len(extracted_text)}")

                                # OSINT findings
                                findings_col1, findings_col2, findings_col3 = st.columns(3)

                                with findings_col1:
                                    phones = pdf_data.get('potential_phone_numbers', [])
                                    if phones:
                                        st.write("**📞 Potential Phones:**")
                                        for phone in phones[:3]:
                                            st.write(f"• {phone}")
                                        if len(phones) > 3:
                                            st.write(f"*... and {len(phones)-3} more*")

                                with findings_col2:
                                    emails = pdf_data.get('potential_emails', [])
                                    if emails:
                                        st.write("**📧 Potential Emails:**")
                                        for email in emails[:3]:
                                            st.write(f"• {email}")
                                        if len(emails) > 3:
                                            st.write(f"*... and {len(emails)-3} more*")

                                with findings_col3:
                                    urls = pdf_data.get('potential_urls', [])
                                    if urls:
                                        st.write("**🔗 Potential URLs:**")
                                        for url in urls[:3]:
                                            st.write(f"• {url}")
                                        if len(urls) > 3:
                                            st.write(f"*... and {len(urls)-3} more*")

                            # GPS data from converted page
                            if 'page_gps_data' in pdf_data:
                                st.subheader("📍 GPS Data (from PDF page)")
                                gps_data = pdf_data['page_gps_data']
                                st.write(f"**Latitude:** {gps_data['latitude']:.6f}")
                                st.write(f"**Longitude:** {gps_data['longitude']:.6f}")

                                # Reverse geocoding
                                with st.spinner("Getting location address..."):
                                    address = get_location_address(gps_data['latitude'], gps_data['longitude'])
                                st.write(f"**🏠 Address:** {address}")

                                # Generate map
                                st.subheader("🗺️ Location Map")
                                with st.spinner("Generating map..."):
                                    m = generate_map(gps_data['latitude'], gps_data['longitude'])
                                    if m:
                                        folium_static(m, key="pdf_map")
                                    else:
                                        st.error("Could not generate map")

                        # Raw JSON data
                        with st.expander("📄 Raw PDF Analysis Data", key="pdf_raw_expander"):
                            st.json(pdf_data)

        with sub_tab2:
            st.subheader("Phone Number Analysis")
            phone_input = st.text_input(
                "Enter phone number",
                placeholder="+1-555-123-4567 or 5551234567",
                help="Enter phone number with or without country code"
            )

            country_code = st.selectbox(
                "Default Country (if not specified in number)",
                ["IN", "US", "GB", "CA", "AU", "DE", "FR", "IT", "ES", "BR"],
                index=0,
                help="Select default country for number parsing"
            )

            # Analyze button and validation
            if phone_input:
                if st.button("🔍 Analyze Phone Number", type="primary", key="analyze_phone_btn"):
                    with st.spinner("Analyzing phone number..."):
                        # Analyze phone number
                        analysis = analyze_phone_number(phone_input, country_code)

                        # Display results
                        st.success("Analysis Complete!")

                        # Validation status
                        if analysis.get('valid'):
                            st.success("✅ Valid Phone Number")
                        else:
                            st.error("❌ Invalid Phone Number")
                            if 'error' in analysis:
                                st.error(f"Error: {analysis['error']}")

                        # Results in columns
                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader("📞 Basic Information")
                            st.write(f"**Input:** {analysis.get('input', 'N/A')}")
                            st.write(f"**Formatted:** {analysis.get('formatted_number', 'N/A')}")
                            st.write(f"**Country Code:** +{analysis.get('country_code', 'N/A')}")
                            st.write(f"**Line Type:** {analysis.get('line_type', 'N/A')}")

                        with col2:
                            st.subheader("📍 Location & Carrier")
                            st.write(f"**Carrier:** {analysis.get('carrier', 'N/A')}")
                            st.write(f"**Region:** {analysis.get('region', 'N/A')}")
                            if analysis.get('timezone'):
                                st.write(f"**Timezone:** {', '.join(analysis['timezone'])}")
                            else:
                                st.write("**Timezone:** N/A")

                        # Raw JSON data
                        with st.expander("📄 Raw Analysis Data"):
                            st.json(analysis)
            else:
                st.info("👆 Enter a phone number above and click '🔍 Analyze Phone Number' to begin analysis.")

    with tab3:
        st.header("🔍 File Authenticity Analysis")
        st.write("Analyze uploaded files for signs of manipulation, tampering, or authenticity.")
        st.write("Supports image manipulation detection and PDF integrity checks.")
        st.markdown("---")

        # File upload for authenticity check
        auth_file = st.file_uploader(
            "Choose a file to analyze authenticity",
            type=['jpg', 'jpeg', 'png', 'tiff', 'bmp', 'pdf'],
            help="Upload an image or PDF to check for manipulation or tampering",
            key="auth_uploader"
        )

        if auth_file is not None:
            st.write(f"**Filename:** {auth_file.name}")
            st.write(f"**File size:** {len(auth_file.getvalue()) / 1024:.1f} KB")

            if st.button("🔍 Check Authenticity", type="primary", key="auth_check_btn"):
                with st.spinner("Analyzing file authenticity..."):
                    auth_result = analyze_file_authenticity(auth_file)

                    st.success("Authenticity Analysis Complete!")

                    # Display results
                    if 'error' in auth_result:
                        st.error(f"Analysis Error: {auth_result['error']}")
                    else:
                        # Main classification
                        classification = auth_result.get('classification', 'UNKNOWN')
                        confidence = auth_result.get('confidence', 'N/A')

                        if classification in ['REAL', 'HIGHLY TRUSTWORTHY', 'TRUSTWORTHY']:
                            st.success(f"✅ {classification} (Confidence: {confidence})")
                        elif classification in ['LIKELY REAL', 'SUSPICIOUS']:
                            st.warning(f"⚠️ {classification} (Confidence: {confidence})")
                        else:
                            st.error(f"❌ {classification} (Confidence: {confidence})")

                        # Detailed results
                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader("📊 Analysis Results")
                            if 'authenticity_score' in auth_result:
                                st.write(f"**Authenticity Score:** {auth_result['authenticity_score']}%")
                            if 'analysis_method' in auth_result:
                                st.write(f"**Method:** {auth_result['analysis_method']}")

                        with col2:
                            st.subheader("📋 Technical Details")
                            if 'mean_difference' in auth_result:
                                st.write(f"**Mean Difference:** {auth_result['mean_difference']}")
                            if 'suspicious_pixels_ratio' in auth_result:
                                st.write(f"**Suspicious Pixels:** {auth_result['suspicious_pixels_ratio']}%")
                            if 'file_integrity' in auth_result:
                                st.write(f"**File Integrity:** {auth_result['file_integrity']}")

                        # Special displays for different file types
                        if 'ela_image_data' in auth_result:
                            st.subheader("🔍 Error Level Analysis (ELA)")
                            st.write("This image shows compression artifacts. Brighter areas indicate potential manipulation.")
                            ela_image = Image.open(io.BytesIO(auth_result['ela_image_data']))
                            st.image(ela_image, caption="ELA Analysis Result", use_column_width=True)

                        # PDF-specific results
                        if 'digital_signatures' in auth_result:
                            signatures = auth_result['digital_signatures']
                            if signatures:
                                st.subheader("✍️ Digital Signatures")
                                for sig in signatures:
                                    st.write(f"✅ {sig}")
                            else:
                                st.write("**Digital Signatures:** None found")

                        if 'suspicious_elements' in auth_result:
                            suspicious = auth_result['suspicious_elements']
                            if suspicious:
                                st.subheader("⚠️ Suspicious Elements")
                                for element in suspicious:
                                    st.error(f"• {element}")

                        if 'metadata_consistency' in auth_result:
                            consistency = auth_result['metadata_consistency']
                            if consistency == 'CONSISTENT':
                                st.success("**Metadata Consistency:** ✅ Consistent")
                            elif consistency == 'INCONSISTENT':
                                st.error("**Metadata Consistency:** ❌ Inconsistent")
                            else:
                                st.info(f"**Metadata Consistency:** {consistency}")

                    # Raw analysis data
                    with st.expander("📄 Raw Authenticity Data", key="auth_raw_expander"):
                        st.json(auth_result)

if __name__ == "__main__":
    main()