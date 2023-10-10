import streamlit as st
from googletrans import Translator
from gtts import gTTS
from PIL import Image
import easyocr
import os

st.title("Traductor")
image = Image.open('traductor.jpg')
st.image(image, width=300)
try:
    os.mkdir("temp")
except:
    pass
st.subheader("Leer y traducir desde texto o imagen")

st.write('Usa la aplicación para traducir texto o texto de imágenes en un idioma que no hables')
source_lang = "es"  # Lenguaje de origen (puedes cambiarlo según tus necesidades)
translator = Translator()
text = st.text_input("Escribe el texto que quieres traducir aquí:")

# Lista de idiomas de destino
languages = {
    "Alemán": "de",
    "Español": "es",
    "Inglés": "en",
    "Portugués": "pr",
    "Francés": "fr",
    "Ruso": "ru",
    "Chino Mandarín": "zh-cn",
}

# Widget para seleccionar el idioma de destino
target_lang = st.selectbox("¿En cuál idioma quieres traducirlo?:", list(languages.keys()))

def text_to_speech(text, tld):
    tts = gTTS(text, lang=tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

if text and target_lang:
    target_lang_code = languages[target_lang]
    translated_text = translator.translate(text, src=source_lang, dest=target_lang_code).text
    if target_lang == "Chino Mandarín":
        target_lang_code = "zh-cn"
    elif target_lang == "Francés":
        target_lang_code = "fr"
    result, output_text = text_to_speech(translated_text, target_lang_code)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown(f"## Tu audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)
    st.markdown(f"## Texto en audio:")
    st.write(f" {output_text}")

# Sección para cargar una imagen con texto
st.subheader("Cargar una imagen con texto:")
uploaded_image = st.file_uploader("Carga una imagen:", type=["jpg", "png", "jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Imagen cargada", use_column_width=True)
    
    # Detectar texto en la imagen
    reader = easyocr.Reader(["en"])
    detected_text = reader.readtext(uploaded_image)

    # Extraer y mostrar el texto detectado
    if detected_text:
        extracted_text = " ".join([text for (text, _, _) in detected_text])
        st.markdown("## Texto detectado en la imagen:")
        st.write(extracted_text)

        # Traducir el texto detectado
        translated_text = translator.translate(extracted_text, src="en", dest=target_lang_code).text
        st.markdown("## Texto traducido:")
        st.write(translated_text)

    


