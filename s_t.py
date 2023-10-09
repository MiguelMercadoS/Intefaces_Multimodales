import streamlit as st
from googletrans import Translator
from gtts import gTTS
from PIL import Image
import os
 

st.title("Traductor")
image = Image.open('translate.png')
st.image(image, width=300)
try:
    os.mkdir("temp")
except:
    pass
st.subheader("Leer y traducir desde texto.")

st.write('Usa el aplicativo cuando quieras decir algo en un idioma que no hables')
source_lang = "es"  # Lenguaje de origen (puedes cambiarlo según tus necesidades)
translator = Translator()
text = st.text_input("Ingrese el texto:")

# Lista de idiomas de destino
languages = {
    "Español": "es",
    "Inglés": "en",
    "Francés": "fr",
    "Ruso": "ru",
    "Chino Mandarín": "zh-cn", 
}
# Widget para seleccionar el idioma de destino
target_lang = st.selectbox("Seleccione el idioma de destino:", list(languages.keys()))
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
        
    


