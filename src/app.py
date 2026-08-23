import streamlit as tf_streamlit
import keras
from PIL import Image, ImageOps
import numpy as np

tf_streamlit.set_page_config(page_title="AI HVAC Guardian", page_icon="❄", layout="centered")

tf_streamlit.title("❄ AI HVAC Health Guardian")
tf_streamlit.subheader("Smart AC Contamination & Mold Detector (v1.0 MVP)")
tf_streamlit.write("Upload an image of your air conditioner filter to check its health status and detect potential bio-hazards.")


class_names = ['clean', 'dusty', 'mold']


@tf_streamlit.cache_resource
def load_my_ai_model():
    # Đường dẫn trỏ tới file mô hình nằm trong thư mục models của bạn [github.com]
    return keras.models.load_model('models/mold_detector_v1.keras')

try:
    model = load_my_ai_model()
    tf_streamlit.sidebar.success("🤖 AI Brain connected successfully!")
except Exception as e:
    tf_streamlit.sidebar.error("❌ Error: Cannot find 'mold_detector_v1.keras' inside 'models/' folder.")

uploaded_file = tf_streamlit.file_uploader("Choose an AC filter image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image_data = Image.open(uploaded_file)
    tf_streamlit.image(image_data, caption='Uploaded Image', use_container_width=True)
    
    with tf_streamlit.spinner('🤖 AI is analyzing the pixel patterns... Please wait.'):
        size = (224, 224)
        image_resized = ImageOps.fit(image_data, size, Image.Resampling.LANCZOS)
        img_array = np.asarray(image_resized)
        
        if img_array.shape[-1] == 4:
            img_array = img_array[..., :3]
            
        img_reshape = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_reshape)
        # Sử dụng hàm Softmax tối ưu của Keras để tính xác suất toán học
        score = keras.activations.softmax(keras.ops.convert_to_tensor(predictions))

        predicted_class = class_names[np.argmax(score)]
        confidence = 100 * np.max(score)

        tf_streamlit.markdown("---")
        tf_streamlit.write("### 🖥️ AI Diagnostic Analysis:")
        
        if predicted_class == 'clean':
            tf_streamlit.success(f"🟢 **Result: CLEAN** (Confidence: {confidence:.2f}%)")
            tf_streamlit.info("💡 Your filter is healthy. Keep up the good maintenance layout!")
        elif predicted_class == 'dusty':
            tf_streamlit.warning(f"🟡 **Result: DUSTY / CLOGGED** (Confidence: {confidence:.2f}%)")
            tf_streamlit.info("💡 Warning: Heavy dust buildup detected. Please wash or replace the filter soon to save energy.")
        else:
            tf_streamlit.error(f"🔴 **Result: MOLD SPORES DETECTED** (Confidence: {confidence:.2f}%)")
            tf_streamlit.info("💡 Critical Hazard: Potential toxic mold found! Wear a mask and perform immediate deep disinfection.")

tf_streamlit.markdown("---")
tf_streamlit.caption("⚠️ **Disclaimer:** This AI prototype is an educational extracurricular project and does not constitute official professional HVAC or medical advice.")
