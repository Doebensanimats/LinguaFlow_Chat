import streamlit as st
from components.navbar import render_navbar

# ── PAGE CONFIG (MUST BE FIRST) ─────────────────────────
st.set_page_config(
    page_title="LinguaFlow",
    page_icon="🌐",
    layout="wide"
)

# ── NAVBAR ──────────────────────────────────────────────
render_navbar("Home")

# ── STYLE ───────────────────────────────────────────────
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0F172A, #1E293B);
    color: white;
}

.hero {
    text-align: center;
    padding: 4rem 2rem;
}

.hero h1 {
    font-size: 3rem;
    font-weight: 800;
}

.hero p {
    font-size: 1.2rem;
    color: #CBD5F5;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
    transition: 0.2s;
    border: 1px solid rgba(255,255,255,0.1);
}

.card:hover {
    transform: translateY(-5px);
    border-color: #38BDF8;
}

.card h3 {
    margin-bottom: 0.5rem;
}

.card p {
    font-size: 0.9rem;
    color: #A5B4FC;
}

.footer {
    text-align: center;
    padding: 2rem;
    font-size: 0.8rem;
    color: #94A3B8;
}
</style>
""", unsafe_allow_html=True)

# ── HERO SECTION ────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🌐 LinguaFlow</h1>
    <p>Real-Time Multilingual Communication Platform</p>
    <p>Speak. Type. Translate. Listen — instantly.</p>
</div>
""", unsafe_allow_html=True)

# ── FEATURES ────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>💬 Live Chat</h3>
        <p>Real-time speech & text translation between two users.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Chat"):
        st.switch_page("pages/1_Chat.py")

with col2:
    st.markdown("""
    <div class="card">
        <h3>📄 Document Translator</h3>
        <p>Upload and translate PDFs, Word documents, and text files.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Translate Documents"):
        st.switch_page("pages/2_Document_Translator.py")

with col3:
    st.markdown("""
    <div class="card">
        <h3>🎧 Audiobook Generator</h3>
        <p>Convert translated text into natural-sounding speech.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Create Audiobook"):
        st.switch_page("pages/3_Audiobook.py")

# ── VALUE PROPOSITION ───────────────────────────────────
st.markdown("---")

st.markdown("## 🚀 Why LinguaFlow?")
colA, colB = st.columns(2)

with colA:
    st.write("""
    - ⚡ Real-time translation (low latency)
    - 🌍 Supports multiple languages
    - 🎙️ Speech + text input
    - 🔊 Audio playback with AI voices
    """)

with colB:
    st.write("""
    - 📄 Document translation support
    - 🎧 Audio content generation
    - ☁️ Powered by AWS AI services
    - 💡 Designed for global communication
    """)

# ── FOOTER ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Built with ❤️ using Streamlit + AWS (Transcribe, Translate, Polly)
</div>
""", unsafe_allow_html=True)