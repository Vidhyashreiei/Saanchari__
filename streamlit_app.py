import streamlit as st
import google.generativeai as genai
from PIL import Image

# Streamlit UI setup
st.set_page_config(page_title="Saanchari - AP Tourism Chatbot", layout="wide")

st.title("🗺️ Saanchari - Andhra Pradesh Tourism Chatbot")
#st.caption("Powered by Google Gemini | Developed by Kshipani Tech Ventures Pvt Ltd")

st.markdown("""
<style>
    .stChatMessage { margin-bottom: 1rem; }
    .user-msg { background: linear-gradient(135deg, #F75768 0%, #FB6957 100%); color: white; padding: 1rem; border-radius: 12px 12px 0 12px; }
    .bot-msg { background: linear-gradient(135deg, #07546B 0%, #0A6B7D 100%); color: white; padding: 1rem; border-radius: 12px 12px 12px 0; }
    .header { font-size: 2rem; font-weight: bold; color: #07546B; }
    .footer { font-size: 0.85rem; color: #888888; text-align: center; margin-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# Embed Gemini API key directly
GEMINI_API_KEY = "AIzaSyCkt9a84fx7gXwMuREXVE05XAKpNgAJw_s"   #Gemini API key

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

# Built-in questions
builtin_questions = [
    "What are the top tourist attractions in Andhra Pradesh?",
    "Tell me about the famous food in Andhra Pradesh.",
    "What is the best time to visit Andhra Pradesh?"
]

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Built-in question buttons
st.subheader("Quick Questions")
col1, col2, col3 = st.columns(3)
if col1.button(builtin_questions[0]):
    st.session_state.messages.append({"role": "user", "content": builtin_questions[0]})
if col2.button(builtin_questions[1]):
    st.session_state.messages.append({"role": "user", "content": builtin_questions[1]})
if col3.button(builtin_questions[2]):
    st.session_state.messages.append({"role": "user", "content": builtin_questions[2]})

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(f"<div class='user-msg'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-msg'>{message['content']}</div>", unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask something about Andhra Pradesh Tourism..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

# Generate response for new user message
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(st.session_state.messages[-1]["content"])
                reply = response.text.strip()
            except Exception as e:
                reply = f"⚠️ Gemini API Error: {str(e)}"
            st.markdown(f"<div class='bot-msg'>{reply}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": reply})

# Sticky footer at the bottom
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; right: 0; background-color: #FFFFFF; 
            border-top: 1px solid #CFD1D1; padding: 0.5rem; text-align: center; z-index: 999;'>
    <small style='color: #07546B;'>© 2025 Kshipani Tech Ventures Pvt Ltd. All rights reserved.</small>
</div>
""", unsafe_allow_html=True)
