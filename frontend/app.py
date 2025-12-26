import streamlit as st
import requests
from PIL import Image
import io

# Define API URL (Backend must be running!)
API_URL = "http://127.0.0.1:8000/process-image/"

st.set_page_config(page_title="Hackathon OCR", layout="wide")

st.title("📄 AI-Powered OCR Platform")
st.markdown("### Digitize Handwritten & Printed Documents Instantly")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Settings")
    mode = st.radio("Select Document Type:", ("Printed", "Handwritten"))
    st.info("💡 'Handwritten' mode uses Deep Learning (Slower but smarter). 'Printed' uses Tesseract (Fast).")

# --- MAIN UPLOAD SECTION ---
uploaded_file = st.file_uploader("Upload an Image (JPG, PNG)", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Create two columns: Image Preview | Extracted Text
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Image")
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True)

    # Convert mode to lowercase for API ('Printed' -> 'printed')
    api_mode = mode.lower()

    if st.button("Extract Text"):
        with st.spinner("Processing... (This might take a moment)"):
            try:
                # Prepare file for API
                # specific format required for requests.post files
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {"mode": api_mode}

                # Call Backend API
                response = requests.post(API_URL, files=files, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    extracted_text = result.get("text", "")
                    
                    with col2:
                        st.subheader("Extracted Text")
                        st.text_area("Result", extracted_text, height=400)
                        
                        # Add Download Button
                        st.download_button(
                            label="Download as Text File",
                            data=extracted_text,
                            file_name="extracted_text.txt",
                            mime="text/plain"
                        )
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Connection Error: {e}. Is the backend running?")