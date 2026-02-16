<<<<<<< HEAD
# 📝 Smart Meeting Notes (Python Version)

A powerful, streamlined application to transform meeting transcripts into actionable insights using Python, Streamlit, and Groq API (Llama 3).

## Features

- 🐍 **Built with Python** - Uses Streamlit for a robust, data-centric UI
- ⚡ **Ultra-Fast AI** - Powered by Groq API + Llama 3 70B
- 📋 **Structured Output** - JSON-mode parsing ensures consistent summaries, action items, and follow-ups
- 🔐 **Secure** - API Keys managed via session state (never stored permanently)

## Quick Start

1.  **Install Dependencies**
    *   Ensure you have Python installed.
    *   Run `pip install -r requirements.txt`

2.  **Run the App**
    *   Double-click `run_app.bat`
    *   OR run `streamlit run app.py` in your terminal.

3.  **Use the App**
    *   Enter your **Groq API Key** in the sidebar.
    *   Paste your transcript.
    *   Click **Generate Notes**.

## Requirements

- Python 3.8+
- Groq API Key (get free at [console.groq.com](https://console.groq.com/keys))

## Project Structure

- `app.py`: Main application code
- `requirements.txt`: Python dependencies
- `run_app.bat`: Quick launch script
- `sample-transcript.txt`: Test data

