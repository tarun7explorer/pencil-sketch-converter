import cv2
import numpy as np
import streamlit as st
from PIL import Image
import io

# -------------------- Sketch Functions --------------------
def convert_to_pencil_sketch(img, ksize=27, sigma=12, gamma=0.65):
    """Classic pencil sketch using color dodge"""
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted_img = 255 - gray_img
    blurred_img = cv2.GaussianBlur(inverted_img, (ksize, ksize), sigma)
    pencil_sketch = cv2.divide(gray_img, 255 - blurred_img, scale=256)
    pencil_sketch = np.clip(pencil_sketch * gamma, 0, 255).astype(np.uint8)
    return pencil_sketch

def black_and_white_sketch(image):
    """Realistic black & white sketch with outlines"""
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
    )
    smooth = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)
    sketchy = cv2.bitwise_and(smooth, smooth, mask=edges)

    return sketchy

 # -------------------- Streamlit UI --------------------
# Streamlit page config
st.set_page_config(page_title="Pencil Sketch Converter", layout="centered")

# Custom CSS
st.markdown(
    """
    <style>
        .centered-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            width: 100%;
        }
        .custom-file-uploader {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
        }
        .upload-label {
            font-weight: bold;
            font-size: 14px;
            color: #2c3e50;
            margin-bottom: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <h1 style='text-align:center; color:#2c3e50; margin-bottom:5px;'>✏️ Pencil Sketch Converter</h1>
    <p style='text-align:center; font-size:20px; color:#2980b9;'><b>Created by Tarun Tej Gajibimkar</b></p>
    <hr style="border:1px solid #ddd; margin-top:10px; margin-bottom:30px;">
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Features Box (Always visible)
# -------------------------
st.markdown(
    """
    <div style="border:2px solid #2980b9; border-radius:10px; padding:15px; margin-top:10px; background-color:#f9f9f9;">
        <h3 style="color:#2c3e50; text-align:center;">✨ Features of this Project</h3>
        <ul style="font-size:15px; line-height:1.8; color:#2c3e50;">
            <li>🖤 <b>Black & White Sketch</b> → Realistic monochrome outlines</li>
            <li>✏️ <b>Classic Pencil Sketch</b> → Smooth hand-drawn look</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="centered-container" style="margin-top:5px;">
        <div style="width:250px; text-align:center;">
            <label class="upload-label">📂 Upload an image file</label>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
uploaded_file = st.file_uploader("", type=['jpg', 'jpeg', 'png'])

# Sketch style selector
mode = st.radio(
    "🎨 Select Sketch Style:",
    ["🖤 Black & White Sketch", "✏️ Classic Pencil Sketch"],
    horizontal=True,
)

def convert_to_pencil_sketch(img_bgr):
    gray_image = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(gray_image)
    blur = cv2.GaussianBlur(inverted, (21, 21), 0)
    inverted_blur = cv2.bitwise_not(blur)
    sketch = cv2.divide(gray_image, inverted_blur, scale=256.0)
    return sketch

def black_and_white_sketch(pil_image):
    gray = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2GRAY)
    return gray

if uploaded_file:
    # Open image
    image = Image.open(uploaded_file)

    # Apply selected sketch mode
    if mode == "✏️ Classic Pencil Sketch":
        img_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        sketch = convert_to_pencil_sketch(img_bgr)
        sketch_pil = Image.fromarray(sketch)

    elif mode == "🖤 Black & White Sketch":
        sketch = black_and_white_sketch(image)
        sketch_pil = Image.fromarray(sketch)

    # Side-by-side columns
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📸 Original Image")
        st.image(image, use_container_width=True)
    with c2:
        st.subheader("🎨 Generated Sketch")
        st.image(sketch_pil, use_container_width=True)

    # Download Button
    buf = io.BytesIO()
    sketch_pil.save(buf, format='PNG')
    buf.seek(0)
    st.download_button(
        "📥 Download Sketch",
        data=buf,
        file_name="pencil_sketch.png",
        mime="image/png"
    )