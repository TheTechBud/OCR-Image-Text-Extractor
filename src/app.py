import streamlit as st
import cv2
import numpy as np
from pre_process import preprocess_image
from ocr_engine import run_ocr
from visualisation import draw_boxes
from text_cleaner import clean_ocr_text

st.title("OCR Text Extraction Tool")

uploaded_file = st.file_uploader("Upload an Image", type=["png","jpg","jpeg"])

if uploaded_file is not None:

    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    st.image(image, caption="Uploaded Image")

    original, processed = preprocess_image(image)

    st.image(processed, caption="Preprocessed Image")

    results = run_ocr(processed)

    boxed = draw_boxes(original, results)

    st.image(boxed, caption="Detected Text Regions")

    st.subheader("Detected Text")

    extracted_text = ""

    for bbox, text, prob in results:
        extracted_text += text + "\n"

    cleaned_text = clean_ocr_text(extracted_text)
    st.text(cleaned_text)

    st.download_button(
        "Download Extracted Text",
        cleaned_text,
        file_name="ocr_output.txt"
    )