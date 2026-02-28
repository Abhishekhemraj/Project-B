# AI Joke Generator Deployment Guide

This project is a modular, production-ready AI Joke Generator that leverages Groq's LLM and a local ranked dataset.

## 🚀 Running Locally

Follow these steps to get the Web UI running on your machine:

1.  **Clone the repository** (if you haven't already).
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up your Environment Variables**:
    Create a `.env` file in the root directory and add your Groq API Key:
    ```env
    GROQ_API_KEY=your_key_here
    ```
4.  **Launch the Web UI**:
    ```bash
    streamlit run joke_ui.py
    ```
5.  **Access the app**:
    Open your browser and navigate to `http://localhost:8501`.

---

## ☁️ Online Deployment

### Streamlit Community Cloud (Recommended)
This is the easiest way to deploy for free.

1.  Push your code to a **GitHub repository**.
2.  Log in to [Streamlit Cloud](https://share.streamlit.io/).
3.  Click **"New app"** and select your repository and the `joke_ui.py` file.
4.  **Crucial Step**: Go to "Advanced settings" in the Streamlit Cloud deployment dashboard and add your `GROQ_API_KEY` to the **Secrets** section:
    ```toml
    GROQ_API_KEY = "your_actual_key_here"
    ```
5.  Click **Deploy**!

### Hugging Face Spaces
1.  Create a new Space on [Hugging Face](https://huggingface.co/spaces).
2.  Select **Streamlit** as the SDK.
3.  Upload your files or connect your GitHub.
4.  Add your `GROQ_API_KEY` in the Space's **Settings > Variables and Secrets**.

---

## 🛠 Project Structure
- `joke_ui.py`: The main Streamlit web application.
- `manual_test.py`: CLI script for manual backend testing.
- `phase4_integration/main.py`: The core application logic.
- `requirements.txt`: List of Python dependencies.
