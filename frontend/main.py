# streamlit_app.py
import streamlit as st
import requests

st.title("📄 PDF Upload Chatbot")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.write(f"File selected: `{uploaded_file.name}`")

    if st.button("Send to Backend"):
        with st.spinner("Uploading..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                response = requests.post(
                    "http://localhost:8000/upload-pdf/", files=files
                )

                if response.status_code == 200:
                    st.success("PDF uploaded successfully!")
                else:
                    st.error(f"Upload failed: {response.json().get('message')}")
            except Exception as e:
                st.error(f"Error: {e}")
