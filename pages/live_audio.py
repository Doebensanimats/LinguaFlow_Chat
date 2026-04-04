import streamlit as st
import boto3
import json
import time
import uuid
import os
import pandas as pd
from datetime import datetime
from audio_recorder_streamlit import audio_recorder
from dotenv import load_dotenv

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LinguaFlow – Live Audio",
    page_icon="🎙️",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --primary:   #FF6B35;
    --secondary: #004E89;
    --bg:        #0D0D0D;
    --surface:   #1A1A2E;
    --surface2:  #16213E;
    --text:      #F0EBF4;
    --muted:     #8B8FA8;
    --border:    rgba(255,107,53,0.25);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}
.main { background: var(--bg); }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D0D0D 0%, #1A1A2E 100%);
    border-right: 1px solid var(--border);
}

.hero {
    background: linear-gradient(135deg, #004E89 0%, #FF6B35 100%);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "🎙️";
    position: absolute; right: 2rem; top: 1rem;
    font-size: 5rem; opacity: 0.15;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem; font-weight: 800;
    color: #fff; margin: 0 0 0.3rem;
}
.hero p { color: rgba(255,255,255,0.8); font-size: 16px; margin: 0; }

.person-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
}
.person-a { border-top: 4px solid #FF6B35; }
.person-b { border-top: 4px solid #004E89; }

.person-name {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem; font-weight: 800;
    margin-bottom: 1rem;
}

.transcript-box {
    background: #111827;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 1rem;
    min-height: 80px;
    font-size: 15px;
    color: var(--text);
    margin: 0.5rem 0;
}

.translation-box {
    background: #0a2a1a;
    border: 1px solid rgba(6,214,160,0.3);
    border-radius: 10px;
    padding: 1rem;
    min-height: 80px;
    font-size: 16px;
    color: #06D6A0;
    margin: 0.5rem 0;
}

.conv-bubble-a {
    background: rgba(255,107,53,0.12);
    border-left: 3px solid #FF6B35;
    border-radius: 0 12px 12px 0;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
}
.conv-bubble-b {
    background: rgba(0,78,137,0.2);
    border-right: 3px solid #59A5D8;
    border-radius: 12px 0 0 12px;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    text-align: right;
}
.bubble-meta { font-size: 12px; color: var(--muted); margin-bottom: 0.2rem; }
.bubble-original { font-size: 14px; color: var(--muted); }
.bubble-translated { font-size: 15px; color: var(--text); font-weight: 500; }

.stButton > button {
    background: linear-gradient(135deg, #FF6B35, #e8541f);
    color: #fff;
    border: none;
    border-radius: 10px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 15px;
    padding: 0.6rem 1.5rem;
    box-shadow: 0 4px 20px rgba(255,107,53,0.3);
    transition: transform 0.15s;
}
.stButton > button:hover { transform: translateY(-2px); }

.stSelectbox > div > div {
    background: #111827;
    border: 1px solid rgba(255,107,53,0.25);
    border-radius: 10px;
    color: var(--text);
}
</style>
""", unsafe_allow_html=True)

# ── Config ────────────────────────────────────────────────────────────────────
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
S3_BUCKET  = os.environ.get("INPUT_BUCKET", "translation-app-input-2026")

# ── AWS clients ───────────────────────────────────────────────────────────────
transcribe_client = boto3.client("transcribe", region_name=AWS_REGION)
translate_client  = boto3.client("translate",  region_name=AWS_REGION)
polly_client      = boto3.client("polly",      region_name=AWS_REGION)
s3_client         = boto3.client("s3",         region_name=AWS_REGION)

# ── Languages ─────────────────────────────────────────────────────────────────
LANGUAGES = {
    "English":    {"translate": "en", "transcribe": "en-US", "polly": "Joanna"},
    "Spanish":    {"translate": "es", "transcribe": "es-US", "polly": "Lupe"},
    "French":     {"translate": "fr", "transcribe": "fr-FR", "polly": "Lea"},
    "German":     {"translate": "de", "transcribe": "de-DE", "polly": "Vicki"},
    "Italian":    {"translate": "it", "transcribe": "it-IT", "polly": "Bianca"},
    "Portuguese": {"translate": "pt", "transcribe": "pt-BR", "polly": "Camila"},
    "Japanese":   {"translate": "ja", "transcribe": "ja-JP", "polly": "Mizuki"},
    "Korean":     {"translate": "ko", "transcribe": "ko-KR", "polly": "Seoyeon"},
    "Hindi":      {"translate": "hi", "transcribe": "hi-IN", "polly": "Aditi"},
    "Arabic":     {"translate": "ar", "transcribe": "ar-SA", "polly": "Zeina"},
    "Dutch":      {"translate": "nl", "transcribe": "nl-NL", "polly": "Laura"},
    "Turkish":    {"translate": "tr", "transcribe": "tr-TR", "polly": "Filiz"},
    "Swahili":    {"translate": "sw", "transcribe": "sw-KE", "polly": None},
}

# ── Session state ─────────────────────────────────────────────────────────────
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# ── Helpers ───────────────────────────────────────────────────────────────────
def upload_audio_to_s3(audio_bytes, filename):
    s3_client.put_object(Bucket=S3_BUCKET, Key=f"audio/{filename}", Body=audio_bytes)
    return f"s3://{S3_BUCKET}/audio/{filename}"

def transcribe_audio(s3_uri, language_code, job_name):
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": s3_uri},
        MediaFormat="wav",
        LanguageCode=language_code,
        OutputBucketName=S3_BUCKET,
        OutputKey=f"transcripts/{job_name}.json",
    )
    for _ in range(60):
        response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        status = response["TranscriptionJob"]["TranscriptionJobStatus"]
        if status == "COMPLETED":
            obj = s3_client.get_object(Bucket=S3_BUCKET, Key=f"transcripts/{job_name}.json")
            transcript_json = json.loads(obj["Body"].read())
            return transcript_json["results"]["transcripts"][0]["transcript"]
        elif status == "FAILED":
            return None
        time.sleep(2)
    return None

def translate_text(text, source, target):
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source,
        TargetLanguageCode=target,
    )
    return response["TranslatedText"]

def speak_translation(text, voice_id):
    neural_voices = ["Joanna", "Lupe", "Lea", "Vicki", "Laura", "Seoyeon"]
    engine = "neural" if voice_id in neural_voices else "standard"
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=voice_id,
        Engine=engine,
    )
    return response["AudioStream"].read()

def process_audio(audio_bytes, speaker_name, src_lang_name, tgt_lang_name):
    src = LANGUAGES[src_lang_name]
    tgt = LANGUAGES[tgt_lang_name]
    job_name = f"lingua-{uuid.uuid4().hex[:12]}"
    filename = f"{job_name}.wav"
    progress = st.progress(0, text="Uploading audio...")
    try:
        s3_uri = upload_audio_to_s3(audio_bytes, filename)
        progress.progress(25, text="Transcribing speech...")
        transcript = transcribe_audio(s3_uri, src["transcribe"], job_name)
        if not transcript:
            st.error("Transcription failed. Please try again.")
            progress.empty()
            return None, None, None
        progress.progress(65, text="Translating...")
        translated = translate_text(transcript, src["translate"], tgt["translate"])
        audio_out = None
        if tgt["polly"]:
            progress.progress(85, text="Generating speech...")
            try:
                audio_out = speak_translation(translated, tgt["polly"])
            except Exception:
                pass
        progress.progress(100, text="Done!")
        time.sleep(0.4)
        progress.empty()
        return transcript, translated, audio_out
    except Exception as e:
        progress.empty()
        st.error(f"Error: {str(e)}")
        return None, None, None

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 1.5rem;'>
        <div style='font-family:Syne,sans-serif; font-size:1.6rem; font-weight:800; color:#FF6B35;'>🌐 LinguaFlow</div>
        <div style='color:#8B8FA8; font-size:13px;'>Live Audio Translation</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 👤 Person A")
    person_a_name = st.text_input("Name", value="Person A", key="name_a")
    lang_a = st.selectbox("Speaks", list(LANGUAGES.keys()), index=0, key="lang_a")

    st.markdown("### 👤 Person B")
    person_b_name = st.text_input("Name", value="Person B", key="name_b")
    lang_b = st.selectbox("Speaks", list(LANGUAGES.keys()), index=1, key="lang_b")

    st.markdown("---")
    if st.button("Clear Conversation"):
        st.session_state.conversation = []
        st.rerun()

    st.markdown(f"""
    <div style='color:#8B8FA8; font-size:13px; margin-top:1rem;'>
    💬 Exchanges so far: <b>{len(st.session_state.conversation)}</b>
    </div>
    """, unsafe_allow_html=True)

# ── Main ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero'>
    <h1>Live Audio Conversation</h1>
    <p>Speak in your language — hear the reply in theirs. Powered by AWS Transcribe, Translate and Polly.</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([2, 1, 2])
with c1:
    st.markdown(f"<div style='text-align:center; font-family:Syne,sans-serif; font-size:1.1rem; color:#FF6B35; font-weight:700;'>🎙️ {person_a_name}<br><span style='font-size:13px; color:#8B8FA8;'>{lang_a}</span></div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div style='text-align:center; font-size:1.5rem; padding-top:0.5rem;'>⇄</div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div style='text-align:center; font-family:Syne,sans-serif; font-size:1.1rem; color:#59A5D8; font-weight:700;'>🎙️ {person_b_name}<br><span style='font-size:13px; color:#8B8FA8;'>{lang_b}</span></div>", unsafe_allow_html=True)

st.markdown("---")

col_a, col_b = st.columns(2, gap="large")

# ── Person A ──────────────────────────────────────────────────────────────────
with col_a:
    st.markdown(f"<div class='person-panel person-a'><div class='person-name'>🟠 {person_a_name}</div></div>", unsafe_allow_html=True)
    st.markdown(f"**Speaks:** {lang_a} → **Translated to:** {lang_b}")
    st.markdown("Press mic to record:")
    audio_a = audio_recorder(
        text="", recording_color="#FF6B35",
        neutral_color="#8B8FA8", icon_size="2x", key="recorder_a"
    )
    if audio_a:
        transcript_a, translated_a, audio_out_a = process_audio(audio_a, person_a_name, lang_a, lang_b)
        if transcript_a:
            st.markdown("**You said:**")
            st.markdown(f"<div class='transcript-box'>{transcript_a}</div>", unsafe_allow_html=True)
            st.markdown(f"**In {lang_b}:**")
            st.markdown(f"<div class='translation-box'>{translated_a}</div>", unsafe_allow_html=True)
            if audio_out_a:
                st.audio(audio_out_a, format="audio/mp3")
            st.session_state.conversation.append({
                "speaker": person_a_name, "type": "a",
                "original": transcript_a, "translated": translated_a,
                "src_lang": lang_a, "tgt_lang": lang_b,
                "time": datetime.now().strftime("%H:%M:%S"),
            })
            st.rerun()

# ── Person B ──────────────────────────────────────────────────────────────────
with col_b:
    st.markdown(f"<div class='person-panel person-b'><div class='person-name'>🔵 {person_b_name}</div></div>", unsafe_allow_html=True)
    st.markdown(f"**Speaks:** {lang_b} → **Translated to:** {lang_a}")
    st.markdown("Press mic to record:")
    audio_b = audio_recorder(
        text="", recording_color="#004E89",
        neutral_color="#8B8FA8", icon_size="2x", key="recorder_b"
    )
    if audio_b:
        transcript_b, translated_b, audio_out_b = process_audio(audio_b, person_b_name, lang_b, lang_a)
        if transcript_b:
            st.markdown("**You said:**")
            st.markdown(f"<div class='transcript-box'>{transcript_b}</div>", unsafe_allow_html=True)
            st.markdown(f"**In {lang_a}:**")
            st.markdown(f"<div class='translation-box'>{translated_b}</div>", unsafe_allow_html=True)
            if audio_out_b:
                st.audio(audio_out_b, format="audio/mp3")
            st.session_state.conversation.append({
                "speaker": person_b_name, "type": "b",
                "original": transcript_b, "translated": translated_b,
                "src_lang": lang_b, "tgt_lang": lang_a,
                "time": datetime.now().strftime("%H:%M:%S"),
            })
            st.rerun()

# ── Conversation log ──────────────────────────────────────────────────────────
if st.session_state.conversation:
    st.markdown("---")
    st.markdown("<div style='font-family:Syne,sans-serif; font-size:1.1rem; font-weight:700; color:#FF6B35; margin-bottom:1rem;'>💬 Conversation Log</div>", unsafe_allow_html=True)

    for entry in st.session_state.conversation:
        if entry["type"] == "a":
            st.markdown(f"""
            <div class='conv-bubble-a'>
                <div class='bubble-meta'>🟠 {entry['speaker']} · {entry['time']} · {entry['src_lang']} → {entry['tgt_lang']}</div>
                <div class='bubble-original'>"{entry['original']}"</div>
                <div class='bubble-translated'>→ {entry['translated']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='conv-bubble-b'>
                <div class='bubble-meta'>🔵 {entry['speaker']} · {entry['time']} · {entry['src_lang']} → {entry['tgt_lang']}</div>
                <div class='bubble-original'>"{entry['original']}"</div>
                <div class='bubble-translated'>→ {entry['translated']}</div>
            </div>
            """, unsafe_allow_html=True)

    df = pd.DataFrame(st.session_state.conversation)
    st.download_button(
        "⬇️ Download Conversation Log",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="conversation_log.csv",
        mime="text/csv"
    )
