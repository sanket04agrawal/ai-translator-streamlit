import streamlit as st
from PIL import Image
import pytesseract
from googletrans import Translator
from gtts import gTTS
import tempfile
import os

st.set_page_config(page_title="AI Translator", layout="centered")

st.title("🌍 AI Image & Text Translator")
st.write("Translate text or images into your language with voice output")

translator = Translator()

# Language options
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

mode = st.radio("Choose Input Type", ["Text", "Image"])

text = ""

if mode == "Text":
    text = st.text_area("Enter text to translate")

else:
    image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if image:
        img = Image.open(image)
        st.image(img, caption="Uploaded Image", use_column_width=True)
        text = pytesseract.image_to_string(img)

if text:
    st.subheader("📄 Extracted Text")
    st.write(text)

    target_lang = st.selectbox("Translate to", list(languages.keys()))

    translated = translator.translate(text, dest=languages[target_lang])

    st.subheader("✅ Translated Text")
    st.write(translated.text)

    if st.button("🔊 Speak Translation"):
        tts = gTTS(translated.text, lang=languages[target_lang])
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.audio(fp.name)
            os.remove(fp.name)
