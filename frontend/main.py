# streamlit_app.py
import streamlit as st
import requests

API_URL = "http://localhost:8000"

# Initialize session state
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "username" not in st.session_state:
    st.session_state.username = None


def login(username, password):
    response = requests.post(
        f"{API_URL}/auth/token",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        st.session_state.access_token = token
        st.session_state.username = username
        st.success("Logged in successfully!")
    else:
        st.error("Login failed. Check credentials.")


def register(username, password):
    response = requests.post(
        f"{API_URL}/auth/", json={"username": username, "password": password}
    )
    if response.status_code == 201:
        st.success("Registration successful! You can now log in.")
    else:
        st.error("Registration failed. User may already exist.")


# Auth UI
st.title("🔐 Login or Register")

auth_tab = st.tabs(["Login", "Register"])

with auth_tab[0]:
    st.subheader("Login")
    login_username = st.text_input("Username", key="login_user")
    login_password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        login(login_username, login_password)

with auth_tab[1]:
    st.subheader("Register")
    reg_username = st.text_input("New Username", key="reg_user")
    reg_password = st.text_input("New Password", type="password", key="reg_pass")
    if st.button("Register"):
        register(reg_username, reg_password)


# Only show file upload if logged in
if st.session_state.access_token:
    st.title("📄 PDF Upload Chatbot")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file:
        st.write(f"File selected: `{uploaded_file.name}`")

        if st.button("Send to Backend"):
            with st.spinner("Uploading and summarizing..."):
                try:
                    files = {
                        "file": (uploaded_file.name, uploaded_file, "application/pdf")
                    }
                    response = requests.post(
                        f"{API_URL}/summarize",
                        files=files,
                        data={
                            "user_id": st.session_state.username
                        },  # backend doesn't use this anymore if token used
                        headers={
                            "Authorization": f"Bearer {st.session_state.access_token}"
                        },
                    )

                    if response.status_code == 200:
                        summary = response.json().get("summary")
                        st.success("PDF summarized and saved!")
                        st.subheader("Summary")
                        st.write(summary)
                    else:
                        st.error(f"Upload failed: {response.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

    # Fetch previous summaries
    st.subheader("🗂️ Your Previous Summaries")
    try:
        res = requests.get(
            f"{API_URL}/summaries",
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
        )
        if res.status_code == 200 and res.json():
            for item in res.json():
                st.markdown(f"### 📄 {item['file_name']} ({item['timestamp']})")
                st.write(item["summary"])
        else:
            st.info("No summaries found yet.")
    except Exception as e:
        st.error(f"Failed to fetch summaries: {e}")
