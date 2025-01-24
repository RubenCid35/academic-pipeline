import streamlit as st
import requests

# Streamlit app title
st.title("Academic PDF File Upload")

# pipeline location input
pipeline_url = st.text_input("Pipeline Location URL", value="localhost:8080")

# File uploader component to allow users to upload a file
uploaded_file = st.file_uploader("Drop your PDF file here (Academic Publication Only)", type=["pdf"])

# Add blank space for layout
st.write("\n")

# Button to trigger the upload
if st.button("Send File"):
    if not uploaded_file:
        st.error("Please drop a PDF file before submitting.")
    else:
        try:
            with st.spinner("Uploading and processing your file... Please wait."):
                data = { 'file': uploaded_file }
                response = requests.post(pipeline_url + "/process", files = data)
                print(f"response: {response.status_code} - content: {response.text}")
                # Display the response status and content
                if response.status_code == 200 and response.text.strip().lower() == "true":
                    st.success(f"File uploaded successfully!")
                else:
                    st.error(f"Failed to upload the file. ")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Disclaimer about response storage
st.write("\n")
st.write("Disclaimer: The server response will be stored in BigQuery for future analysis.")
