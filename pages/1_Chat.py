import sys
import os

# Fix path so pages can find root-level modules
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

import streamlit as st
from utils.languages import LANGUAGES
from services.chat_service import process_message
from services.firebase_service import init_firebase, create_room, send_message, get_messages
from datetime import datetime

st.set_page_config(page_title="Chat", layout="wide")

mode = st.radio("Chat Mode", ["Single User", "Two Users"])

# ───────────────────────── SINGLE USER ─────────────────────────
if mode == "Single User":
    st.title("🧍 Single User Mode")
    text = st.text_input("Enter text")
    if st.button("Process"):
        translated, audio = process_message(
            text,
            "en",
            "es",
            "Joanna"
        )
        st.success(translated)

# ───────────────────────── TWO USERS ──────────────────────────
else:
    st.title("👥 Two User Chat")
    db = init_firebase()
    room = st.query_params.get("room", None)
    if not room:
        if st.button("Create Room"):
            room = create_room()
            st.query_params["room"] = room
            st.rerun()
        st.stop()
    st.code(f"Share link: ?room={room}")
    user = st.selectbox("User", ["A", "B"])
    text = st.text_input("Message")
    if st.button("Send") and text:
        send_message(room, {
            "user": user,
            "text": text,
            "time": datetime.now().strftime("%H:%M")
        })
    st.markdown("### Chat")
    for m in get_messages(room):
        d = m.to_dict()
        st.write(f"{d['user']}: {d['text']}")