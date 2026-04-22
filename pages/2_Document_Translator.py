from components.navbar import render_navbar

render_navbar("Docs")


import streamlit as st
import boto3
import os
import io
import pdfplumber
from docx import Document
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Document Translator", page_icon="📄")

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
translate = boto3.client("translate", region_name=AWS_REGION)

LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Portuguese": "pt",
}

st.title("📄 Document Translator")

# ── Upload ─────────────────────────────────
file = st.file_uploader("Upload document", type=["txt", "pdf", "docx"])

col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("From", list(LANGUAGES.keys()))
with col2:
    tgt_lang = st.selectbox("To", list(LANGUAGES.keys()), index=1)

# ── Extract text ───────────────────────────
def extract_text(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    elif file.name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    elif file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])

    return ""

# ── Translate in chunks ────────────────────
def translate_large(text, src, tgt):
    chunk_size = 4000
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    translated_text = ""
    for chunk in chunks:
        res = translate.translate_text(
            Text=chunk,
            SourceLanguageCode=src,
            TargetLanguageCode=tgt,
        )
        translated_text += res["TranslatedText"]

    return translated_text

# ── Run ───────────────────────────────────
if file:
    text = extract_text(file)

    st.subheader("📜 Extracted Text")
    st.text_area("", text, height=200)

    if st.button("🌍 Translate Document"):
        with st.spinner("Translating..."):
            translated = translate_large(
                text,
                LANGUAGES[src_lang],
                LANGUAGES[tgt_lang]
            )

        st.subheader("✅ Translated")
        st.text_area("", translated, height=200)

        st.download_button(
            "⬇️ Download Translation",
            translated,
            file_name="translated.txt"
        )