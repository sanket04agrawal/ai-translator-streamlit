import streamlit as st
from PIL import Image
import pytesseract
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
import os

# ---------- PAGE CONFIG (Mobile friendly) ----------
st.set_page_config(
    page_title="AI Translator",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🌍 AI Translator")
st.caption("Text / Image → Translate → Speak")

# ---------- LANGUAGES ----------
languages = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "French": "fr",
    "Spanish": "es",
    "German": "de"
}

# ---------- INPUT MODE ----------
mode = st.radio(
    "Input Type",
    ["Text", "Image"],
    horizontal=True
)

text = ""

# ---------- TEXT INPUT ----------
if mode == "Text":
    text = st.text_area(
        "Enter text to translate",
        height=180,
        placeholder="Type here…"
    )

# ---------- IMAGE INPUT ----------
else:
    image = st.file_uploader(
        "Upload image",
        type=["png", "jpg", "jpeg"]
    )

    if image:
        img = Image.open(image)
        st.image(img, use_container_width=True)
        text = pytesseract.image_to_string(img)

# ---------- TARGET LANGUAGE ----------
target_lang = st.selectbox(
    "Translate to",
    list(languages.keys())
)

# ---------- BUTTONS (IMPORTANT PART) ----------
col1, col2 = st.columns(2)

translated_text = ""

with col1:
    translate_clicked = st.button("🔄 Translate", use_container_width=True)

with col2:
    speak_clicked = st.button("🔊 Speak", use_container_width=True)

# ---------- TRANSLATION ----------
if translate_clicked and text.strip():
    translated_text = GoogleTranslator(
        source="auto",
        target=languages[target_lang]
    ).translate(text)

    st.subheader("✅ Translated Text")
    st.write(translated_text)

# ---------- SPEECH ----------
if speak_clicked and text.strip():
    if not translated_text:
        translated_text = GoogleTranslator(
            source="auto",
            target=languages[target_lang]
        ).translate(text)

    tts = gTTS(translated_text, lang=languages[target_lang])

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name)
        os.remove(fp.name)

if not text.strip():
    st.info("👆 Enter text or upload an image")


