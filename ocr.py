# -*- coding: utf-8 -*-
"""OCR.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15DgzlhLCI3xcEMS7207TJdREHQfvu-jp

#Instalamos las dependencias necesarias
"""

#!sudo apt-get install tesseract-ocr
#!pip install pytesseract

"""#Cargamos la imagen"""

from google.colab import files
uploaded = files.upload()

from PIL import Image
import pytesseract
import cv2


#from gtts import gTTS
#from IPython.display import Audio

img_cv = cv2.imread(r'/content/Becaimg.jpg')

# By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
# we need to convert from BGR to RGB format/mode:
img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
print(pytesseract.image_to_string(img_rgb))
# OR
img_rgb = Image.frombytes('RGB', img_cv.shape[:2], img_cv, 'raw', 'BGR', 0, 0)
text_in=pytesseract.image_to_string(img_rgb)
print(pytesseract.image_to_string(img_rgb))
