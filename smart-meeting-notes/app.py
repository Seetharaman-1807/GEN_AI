import streamlit as st
import os
from groq import Groq
import json

# Set page configuration
st.set_page_config(
    page_title="Smart Meeting Notes",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #667eea;
        color: white;
    }
    .stButton>button:hover {
        background-color: #5a67d8;
        color: white;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Application Title
st.title("📝 Smart Meeting Notes")
st.markdown("Transform meeting transcripts into actionable insights using AI.")

# Sidebar for API Key
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Groq API Key", type="password", help="Get your free key at console.groq.com")
    
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key
        st.success("API Key accepted!")
    else:
        st.warning("Please enter your Groq API Key to continue.")
        st.markdown("[Get a free Groq API Key](https://console.groq.com/keys)")

# Main Content Area
if not api_key:
    st.info("👈 Please enter your Groq API Key in the sidebar to get started.")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=api_key)

# Input Tabs
tab1, tab2 = st.tabs(["📄 Paste Transcript", "🎤 Upload Audio"])

with tab1:
    transcript = st.text_area("Paste your meeting transcript here:", height=300)
    generate_btn = st.button("Generate Notes", type="primary")

with tab2:
    st.info("Audio upload feature coming soon! For now, please use the transcript tab.")
    uploaded_file = st.file_uploader("Upload audio file", type=['mp3', 'wav', 'm4a'])

# Logic to generate notes
if generate_btn and transcript:
    with st.spinner("Analyzing meeting transcript..."):
        try:
            prompt = f"""
            Analyze this meeting transcript and provide:
            1. SUMMARY: A concise 2-3 sentence summary of the meeting
            2. ACTION ITEMS: List specific action items with who is responsible (if mentioned)
            3. FOLLOW-UPS: List topics or questions that need follow-up

            Format your response as a valid JSON object with detailed keys: 
            "summary", "action_items" (list of strings), "follow_ups" (list of strings).
            
            Do not include markdown formatting like ```json ... ```. Just return the raw JSON.

            Transcript:
            {transcript}
            """

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=2048,
                response_format={"type": "json_object"},
            )

            # Parse Response
            result_text = chat_completion.choices[0].message.content
            try:
                result = json.loads(result_text)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails (not using json_object mode properly or model hallucinated)
                st.error("Failed to parse AI response. Please try again.")
                st.stop()
            
            # Display Results
            st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("📋 Summary")
                st.success(result.get("summary", "No summary available."))
                
            with col2:
                st.subheader("✅ Action Items")
                actions = result.get("action_items", [])
                if actions:
                    for action in actions:
                        st.write(f"- {action}")
                else:
                    st.write("No action items detected.")
                    
            with col3:
                st.subheader("🔄 Follow-ups")
                followups = result.get("follow_ups", [])
                if followups:
                    for item in followups:
                        st.write(f"- {item}")
                else:
                    st.write("No follow-ups detected.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

elif generate_btn and not transcript:
    st.warning("Please paste a transcript first.")
