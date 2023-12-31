import streamlit as st
import cv2
import numpy as np
import pytesseract
from gtts import gTTS
import tempfile
from googletrans import Translator
from PIL import Image
import os

st.title("Traducción óptica")
image1 = Image.open('fotoimg.jpg')
st.image(image1)

img_file_buffer = st.camera_input("Captura el texto que quieres traducir:")

with st.sidebar:
    filtro = st.radio("Aplicar Filtro", ('Filtro Activado', 'Filtro Desactivado'))

if img_file_buffer is not None:
    bytes_data = img_file_buffer.getValue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == 'Filtro Activado':
        cv2_img = cv2.bitwise_not(cv2_img)
    else: cv2_img=cv2_img

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.write(text)

    if text:
        try:
            audio = gTTS(text=text, lang='es') 
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
                audio.save(temp_audio_file.name)
                audio_path = temp_audio_file.name
                st.audio(audio_path, format="audio/mp3")
        except Exception as e:
            st.error("No se pudo reproducir el audio con la traducción.")

# ------------------------------------------------------------------
st.title("Traductor")
image = Image.open('traductor.jpg')
st.image(image, width=300)

try:
    os.mkdir("temp")
except:
    pass

st.subheader("Leer y traducir desde texto.")
st.write('Usa la aplicación cuando quieras decir algo en un idioma que no hables')

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
