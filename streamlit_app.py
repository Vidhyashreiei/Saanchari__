import streamlit as st
import google.generativeai as genai

from PIL import Image
import os
from dotenv import load_dotenv
from googletrans import Translator

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

# Streamlit UI setup
st.set_page_config(page_title="Saanchari", layout="wide")

# Place a compact language selector next to the title (top right)
st.markdown("""
    <style>
        .title-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }
          /* Language selector styling ↓↓↓ */
        .lang-select {
            background: #fff;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            padding: 0.1rem 0.45rem;        /* smaller padding */
            min-width: 110px;               /* downsized width */
            font-size: 0.9rem;              /* ≈14 px */
        }
        .lang-select label {display:none;}
        .stSelectbox > div {
            padding: 0.1rem 0.45rem;
            font-size: 0.9rem;
            line-height: 1.25rem;
        }
    </style>
""", unsafe_allow_html=True)

lang_map = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te"
}

# Place the selector outside the title-row container
st.markdown("<div class='lang-select'>", unsafe_allow_html=True)
selected_lang = st.selectbox("", list(lang_map.keys()), index=0, label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

# Title row (without language selector inside)
st.markdown("<div class='title-row'>", unsafe_allow_html=True)
st.markdown("<span style='font-size:2rem;font-weight:bold;color:#07546B;'>🗺️ Saanchari - Andhra Pradesh Tourism Chatbot</span>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

translator = Translator()

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

# System prompt for food-related queries
SYSTEM_PROMPT = (
    "You are an expert on Andhra Pradesh tourism and cuisine. "
    "Whenever asked about food, provide detailed information about famous dishes, street food, regional specialties, and culinary traditions from all parts of Andhra Pradesh."
)

# Generate response for new user message
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                prompt = st.session_state.messages[-1]["content"]
                full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"
                response = model.generate_content(full_prompt)
                reply = response.text.strip()
                # Translate reply if needed
                if lang_map[selected_lang] != "en":
                    reply = translator.translate(reply, dest=lang_map[selected_lang]).text
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
