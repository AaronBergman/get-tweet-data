import streamlit as st
import zipfile
import os
import json
import csv
from datetime import datetime
from collections.abc import MutableMapping
import tempfile


# The flatten and filtered_flatten functions remain unchanged.

def process_file(file):
    # Create a temporary directory for processing
    with tempfile.TemporaryDirectory() as tempdir:
        # Save uploaded file to temporary directory
        zip_path = os.path.join(tempdir, "uploaded.zip")
        with open(zip_path, 'wb') as f:
            f.write(file.getvalue())

        unzipped_folder = os.path.join(tempdir, "unzipped")
        os.makedirs(unzipped_folder, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(unzipped_folder)

        # ... Rest of the code remains mostly unchanged ...

        # Define the path for the CSV file
        csv_file_path = os.path.join(tempdir, f"tweets{timestamp}.csv")
        # ... More code ...

        # In the end, allow the user to download the generated CSV
        with open(csv_file_path, 'rb') as f:
            st.download_button(
                label="Download CSV File",
                data=f,
                file_name="tweets.csv",
                mime="text/csv"
            )

        # Open Google Sheets link in a new tab
        st.markdown("[Open Google Sheets](https://sheet.new)", unsafe_allow_html=True)

# Streamlit code to display the UI
st.title("Twitter Data Processor")
uploaded_file = st.file_uploader("Upload a ZIP file", type="zip")

if uploaded_file:
    process_file(uploaded_file)
