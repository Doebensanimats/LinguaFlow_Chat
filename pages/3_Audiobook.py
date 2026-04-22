from components.navbar import render_navbar

render_navbar("Audio")

import streamlit as st
import boto3
import os
import io
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Audiobook Generator", page_icon="🎧")

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
translate = boto3.client("translate", region_name=AWS_REGION)
polly     = boto3.client("polly", region_name=AWS_REGION)

LANGUAGES = {
    "English": ("en", "Joanna"),
    "Spanish": ("es", "Lupe"),
    "French": ("fr", "Lea"),
    "German": ("de", "Vicki"),
}

st.title("🎧 Audiobook Generator")

text = st.text_area("Enter or paste text", height=200)

col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("From", list(LANGUAGES.keys()))
with col2:
    tgt_lang = st.selectbox("To", list(LANGUAGES.keys()), index=1)

# ── Process ───────────────────────────────
if st.button("🎙️ Generate Audiobook"):
    if not text.strip():
        st.warning("Enter text first")
        st.stop()

    with st.spinner("Translating..."):
        translated = translate.translate_text(
            Text=text,
            SourceLanguageCode=LANGUAGES[src_lang][0],
            TargetLanguageCode=LANGUAGES[tgt_lang][0],
        )["TranslatedText"]

    st.subheader("📖 Translated Text")
    st.write(translated)

    with st.spinner("Generating audio..."):
        response = polly.synthesize_speech(
            Text=translated,
            OutputFormat="mp3",
            VoiceId=LANGUAGES[tgt_lang][1],
        )

        audio = response["AudioStream"].read()

    st.audio(audio, format="audio/mp3")

    st.download_button(
        "⬇️ Download Audio",
        audio,
        file_name="audiobook.mp3"
    )