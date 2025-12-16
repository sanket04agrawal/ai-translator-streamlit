import streamlit as st
from PIL import Image
import pytesseract
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
import os

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Image & Text Translator",
    layout="centered"
)

st.title("🌍 AI Image & Text Translator")
st.write("Translate text or images into your language with voice output")

# ---------- LANGUAGE OPTIONS ----------
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

# ---------- INPUT TYPE ----------
mode = st.radio("Choose Input Type", ["Text", "Image"])

text = ""

# ---------- TEXT INPUT ----------
if mode == "Text":
    text = st.text_area("Enter text to translate", height=150)

# ---------- IMAGE INPUT ----------
else:
    image = st.file_uploader(
        "Upload an image (PNG / JPG)",
        type=["png", "jpg", "jpeg"]
    )

    if image:
        img = Image.open(image)
        st.image(img, caption="Uploaded Image", use_container_width=True)

        # OCR
        text = pytesseract.image_to_string(img)

# ---------- PROCESS ----------
if text.strip():
    st.subheader("📄 Extracted / Input Text")
    st.write(text)

    target_lang = st.selectbox(
        "Translate to",
        list(languages.keys())
    )

    # Translation
    translated_text = GoogleTranslator(
        source="auto",
        target=languages[target_lang]
    ).translate(text)

    st.subheader("✅ Translated Text")
    st.write(translated_text)

    # ---------- TEXT TO SPEECH ----------
    if st.button("🔊 Speak Translation"):
        tts = gTTS(
            translated_text,
            lang=languages[target_lang]
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.audio(fp.name)
            os.remove(fp.name)

else:
    st.info("👆 Enter text or upload an image to start translating.")

