import sys
import os

root_path = os.path.abspath(os.path.dirname(__file__))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# Direct file load — bypasses package import issues
import importlib.util
spec = importlib.util.spec_from_file_location(
    "languages",
    os.path.join(root_path, "utils", "languages.py")
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
LANGUAGES = mod.LANGUAGES

import streamlit as st

st.set_page_config(
    page_title="LinguaFlow",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 LinguaFlow")
st.markdown("### Choose a module")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💬 Chat"):
        st.switch_page("pages/1_Chat.py")
with col2:
    if st.button("📄 Documents"):
        st.switch_page("pages/2_Document_Translator.py")
with col3:
    if st.button("🎧 Audiobook"):
        st.switch_page("pages/3_Audiobook.py")