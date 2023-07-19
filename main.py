import streamlit as st
import zipfile
import os
import shutil
import json
import csv
from datetime import datetime
from collections.abc import MutableMapping
import tempfile

# The flatten and filtered_flatten functions remain unchanged.

def process_file(file):
    if not file:
        st.error("No file selected for uploading.")
        return

    if not zipfile.is_zipfile(file):
        st.error("Only zip files are allowed.")
        return

    # Create a temporary directory to store the unzipped contents
    with tempfile.TemporaryDirectory() as unzipped_folder:

        # Extract the contents of the .zip file into the newly created directory
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(unzipped_folder)

        # Locate the 'tweets.js' file in the 'data' subfolder
        data_folder = os.path.join(unzipped_folder, 'data')
        tweets_js_path = os.path.join(data_folder, 'tweets.js')

        # Read the contents of 'tweets.js'
        with open(tweets_js_path, 'r') as file:
            contents = file.read()

        # Find the index of the first square bracket
        first_bracket_index = contents.index('[')

        # Remove characters before the first square bracket
        trimmed_contents = contents[first_bracket_index:]

        # Load the JSON data
        data = json.loads(trimmed_contents)

        # Generate a timestamp for the CSV file
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Define the path for the CSV file
        csv_file_path = os.path.join(unzipped_folder, f"tweets{timestamp}.csv")

        # Define the keys to keep
        keys_to_keep = [
            'entities_user_mentions',
            'favorite_count',
            'in_reply_to_status_id_str',
            'id_str',
            'in_reply_to_user_id',
            'retweet_count',
            'created_at',
            'full_text',
            'in_reply_to_screen_name'
        ]

        # Extract values from dictionaries and write the data to the CSV file
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            if data:  # Check if the data is not empty
                # Flatten the dictionaries, filter by keys and write to CSV
                flat_data = [filtered_flatten(tweet, keys_to_keep) for tweet in data]
                writer.writerow(flat_data[0].keys())  # Write header row
                for tweet in flat_data:
                    writer.writerow(tweet.values())

        # Allow the user to download the generated CSV file
        with open(csv_file_path, 'rb') as f:
            st.download_button(
                label="Download CSV File",
                data=f,
                file_name="tweets.csv",
                mime="text/csv"
            )

# Streamlit code to display the UI
st.title("Twitter Data Processor")
uploaded_file = st.file_uploader("Upload a ZIP file", type="zip")

if uploaded_file:
    process_file(uploaded_file)
