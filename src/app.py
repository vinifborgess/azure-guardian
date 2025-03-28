import streamlit as st
import requests

st.set_page_config(page_title="Azure Guardian", page_icon="🛡️", layout="centered")
st.title("🛡️ Azure Guardian")
st.caption("AI-Powered Chat Moderator")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "toxic_score" not in st.session_state:
    st.session_state.toxic_score = 0

if "banned" not in st.session_state:
    st.session_state.banned = False

# UI Layout
st.subheader("🎮 Chat Simulator")

col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input("Type your message (or use the microphone)", key="chat_input")
with col2:
    voice_triggered = st.button("🎙️ Speak")

send_triggered = st.button("Send")

# Function to send payload to backend
def send_to_backend(payload):
    try:
        response = requests.post("http://127.0.0.1:8000/moderate", json=payload)
        result = response.json()

        # Update session
        st.session_state.toxic_score = result.get("toxic_score", 0)
        text = result.get("text", "[no response]")
        action = result.get("action", "allow")
        feedback = result.get("feedback", "")

        if text:
            st.session_state.messages.append((text, action, feedback))

        if action == "ban":
            st.session_state.banned = True

    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")

# On Speak button click
if voice_triggered and not st.session_state.banned:
    payload = {"text": None, "use_voice": True}
    send_to_backend(payload)

# On Send button click
if send_triggered and not st.session_state.banned and user_input.strip():
    payload = {"text": user_input.strip(), "use_voice": False}
    send_to_backend(payload)

# Toxicity meter
st.subheader("🧪 Toxicity Level")
st.progress(min(st.session_state.toxic_score, 300) / 300)

# Moderation history
st.subheader("📜 Moderation Log")
for text, action, feedback in reversed(st.session_state.messages):
    if action == "allow":
        st.success(f"✅ {text}")
    elif action == "block":
        st.warning(f"⚠️ {text} — {feedback}")
    elif action == "ban":
        st.error(f"💀 {text} — {feedback}")

# Ban notice
if st.session_state.banned:
    st.error("🚫 You have been banned for toxic behavior. Reload the page to start a new session.")
