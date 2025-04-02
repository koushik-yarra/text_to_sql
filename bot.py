import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configure Google Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize session state to track messages and user details
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_name" not in st.session_state:
    st.session_state.user_name = None  # Store user name

# Streamlit UI Setup
st.set_page_config(page_title="Personalized Chatbot", page_icon="🤖")
st.title("🤖 Personalized Chatbot")

# Function to greet the user
def greet_user():
    if st.session_state.user_name:
        st.write(f"Hello, {st.session_state.user_name}! How can I assist you today?")
    else:
        st.write("Hello! What’s your name?")

# Ask for name if not provided
if not st.session_state.user_name:
    user_name_input = st.text_input("What is your name?")
    if user_name_input:
        st.session_state.user_name = user_name_input
        st.session_state.messages.append(("assistant", f"Nice to meet you, {user_name_input}!"))

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg[0]):
        st.markdown(msg[1])

# User input section
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Append user message to session state
    st.session_state.messages.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Use Google Gemini to get a personalized response
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(user_input)
    bot_reply = response.text

    # Add a personalized touch to the response
    if "hello" in user_input.lower():
        bot_reply = f"Hey {st.session_state.user_name}, {bot_reply}"

    # Append bot response to session state
    st.session_state.messages.append(("assistant", bot_reply))
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
