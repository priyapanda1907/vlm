import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np

st.set_page_config(page_title="Dcument OCR App", layout="centered")
st.title("Document OCR App")
st.caption("Upload a scanned document or photo of text to extract  editable text.")

uploaded_file = st.file_uploader("Upload a documnet image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Document", use_container_width=True)

    img_array = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    with st.expander("preview preprocessed image"):
        st.image(thresh, caption="Grayscale + Otsu Threshold", use_container_width=True)
    with st.spinner("Running OCR ..."):
        text = pytesseract.image_to_string(thresh)

    st.subheader("Extracted Text")
    st.text_area("Result", text, height=300)

    st.download_button("Download Text", text, file_name="extracted.txt", mime="text/plain")
else:
    st.info("Upload an image to get started ")