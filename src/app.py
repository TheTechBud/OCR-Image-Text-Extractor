import streamlit as st
import cv2
import easyocr
import numpy as np

st.title("OCR Text Extraction Tool")

uploaded_file = st.file_uploader("Upload an Image", type=["png","jpg","jpeg"])

if uploaded_file is not None:

    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    st.image(image, caption="Uploaded Image")

    reader = easyocr.Reader(['en'], gpu=False)

    results = reader.readtext(image)

    st.subheader("Detected Text")

    for bbox, text, prob in results:
        st.write(f"{text}")