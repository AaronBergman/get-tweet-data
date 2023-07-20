import streamlit as st
import re
import json
import csv
import io
import base64

def render_js_to_csv(file):
    # Step 1: Trim the JavaScript file to get the JSON
    content = file.read().decode("utf-8")
    match = re.search(r"\[.*\]", content, re.DOTALL)
    if match:
        json_content = match.group()
        data = json.loads(json_content)

        # Step 2: Parse the JSON and extract the desired columns
        csv_output = io.StringIO()
        csv_writer = csv.writer(csv_output)

        headers = ['created_at', 'full_text', 'favorite_count', 'retweet_count',
                   'entities_user_mentions', 'in_reply_to_screen_name',
                   'in_reply_to_status_id_str', 'id_str']
        csv_writer.writerow(headers)

        for item in data:
            tweet = item['tweet']

            entities_user_mentions = ", ".join([mention['screen_name'] for mention in tweet['entities']['user_mentions']])
            row = [
                tweet['created_at'],
                tweet['full_text'],
                tweet['favorite_count'],
                tweet['retweet_count'],
                entities_user_mentions,
                tweet.get('in_reply_to_screen_name', ''),
                tweet.get('in_reply_to_status_id_str', ''),
                tweet['id_str']
            ]
            csv_writer.writerow(row)

        # Step 3: Display the CSV content on Streamlit app with a scrollbar
        csv_output.seek(0)
        st.text_area("Generated CSV", csv_output.getvalue(), height=250)

        # Step 4: Add a download button for the CSV
        csv_output.seek(0)
        b64 = base64.b64encode(csv_output.getvalue().encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV</a>'
        st.markdown(href, unsafe_allow_html=True)

    else:
        st.warning("No JavaScript content found.")


def get_file_extension(filename):
    file_extension = filename.split(".")[-1].lower()
    return file_extension

def render_file(file):
    file_extension = get_file_extension(file.name)
    if file_extension == "js":
        render_js_to_csv(file)
    else:
        st.error(f"Unsupported file format: {file_extension}")

def main():
    st.title("Your tweets as a spreadsheet")
    st.write('''
1. [Download your Twitter data](https://twitter.com/settings/download_your_data).
                It may take a few days to come through - they'll email you
2. Double click the provided .zip file. A new folder of the same name will appear in your file browser
3. Open that new folder
4. Open the folder inside called 'data'
5. Find the file called 'tweets.js'
6. Either drag and drop that into the grey box below, or click 'Browse files' and locate again
7. Hit download to access your spreadsheet, which you can load into Excel or Google Sheets
''')

    uploaded_file = st.file_uploader("Upload tweets.js", type=["js"])

    if uploaded_file is not None:
        render_file(uploaded_file)

if __name__ == "__main__":
    main()
