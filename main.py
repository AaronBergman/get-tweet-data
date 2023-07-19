import streamlit as st
import zipfile
import os
import json
import csv
from datetime import datetime
from collections.abc import MutableMapping
import tempfile
import pandas as pd

# Flatten nested dictionaries
def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Filtered flatten - keeps only specified keys
def filtered_flatten(d, keys_to_keep, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if new_key in keys_to_keep:
            if isinstance(v, MutableMapping):
                items.extend(flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
    return dict(items)

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

        # Extract values from dictionaries 
        flat_data_list = [filtered_flatten(tweet, keys_to_keep) for tweet in data]
        
        # Create a pandas DataFrame from the flattened data
        df = pd.DataFrame(flat_data_list)

        # Render the DataFrame in the browser
        st.write(df)

        # Create CSV data from DataFrame
        csv_data = df.to_csv(index=False).encode("utf-8")

        # Offer a download button for the CSV
        st.download_button(
            label="Download CSV File",
            data=csv_data,
            file_name="tweets.csv",
            mime="text/csv"
        )

# Streamlit code to display the UI
st.title("Twitter Data Processor")
uploaded_file = st.file_uploader("Upload a ZIP file", type="zip")

if uploaded_file:
    process_file(uploaded_file)
