import streamlit as st
from googletrans import Translator
from gtts import gTTS
from PIL import Image
import os
uploaded = files.upload()
from PIL import Image
import pytesseract
import cv2

img_cv = cv2.imread(r'/content/Becaimg.jpg')

# By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
# we need to convert from BGR to RGB format/mode:
img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
print(pytesseract.image_to_string(img_rgb))
# OR
img_rgb = Image.frombytes('RGB', img_cv.shape[:2], img_cv, 'raw', 'BGR', 0, 0)
text_in=pytesseract.image_to_string(img_rgb)
print(pytesseract.image_to_string(img_rgb))

st.title("Traductor")
image = Image.open('traductor.jpg')
st.image(image, width=300)
try:
    os.mkdir("temp")
except:
    pass
st.subheader("Leer y traducir desde texto.")

st.write('Usa el aplicativo cuando quieras decir algo en un idioma que no hables')
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
target_lang = st.selectbox("¿En cual idioma quieres traducirlo?:", list(languages.keys()))
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
image2 = Image.open('traducir.jpg')
st.image(image2, width=250)

