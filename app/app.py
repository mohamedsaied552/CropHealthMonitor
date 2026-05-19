"""
SMART CROP HEALTH MONITOR
ML-based plant disease detection and treatment recommendation system.

Upload a leaf image → AI predicts disease → Show treatment options
"""

import json
import os
import sys
import streamlit as st
import numpy as np
from PIL import Image

project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from src.predict import PlantDiseasePredictor
from src.remedies import get_remedy, get_all_diseases

MODEL_PATH = os.path.join(project_root, "models", "plant_model.h5")
CLASS_NAMES_PATH = os.path.join(project_root, "models", "class_names.json")

DEFAULT_CLASS_NAMES = [
    "Pepper__bell___Bacterial_spot",
    "Pepper__bell___healthy",
    "Potato___Early_blight",
    "Potato___healthy",
    "Potato___Late_blight",
    "Tomato__Target_Spot",
    "Tomato__Tomato_mosaic_virus",
    "Tomato__Tomato_YellowLeaf__Curl_Virus",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_healthy",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
]


def get_class_names():
    """Load class names saved during training, or use defaults."""
    if os.path.isfile(CLASS_NAMES_PATH):
        with open(CLASS_NAMES_PATH, encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_CLASS_NAMES


def load_model_and_classes():
    """Load model and class names."""
    class_names = get_class_names()
    predictor = PlantDiseasePredictor(model_path=MODEL_PATH)
    predictor.set_class_names(class_names)
    return predictor, class_names


def format_disease_name(disease_class):
    """Format disease class name for display."""
    return disease_class.replace("__", " - ").replace("_", " ")


def display_prediction_results(results):
    """Display prediction results in an organized format."""
    
    prediction = results["prediction"]
    remedy = results["remedy"]
    
    # Main prediction
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Predicted Disease",
            format_disease_name(prediction["predicted_class"]),
            f"{prediction['confidence']*100:.2f}% confidence"
        )
    
    with col2:
        if "healthy" in prediction["predicted_class"].lower():
            st.success("✓ Plant is HEALTHY")
        else:
            st.warning("⚠ Disease Detected")
    
    # Confidence breakdown
    st.subheader("Confidence Scores")
    pred_dict = {}
    for item in prediction["top_predictions"]:
        class_name = format_disease_name(item["class"])
        pred_dict[class_name] = item["confidence"] * 100
    
    st.bar_chart(pred_dict)
    
    # Disease information
    if remedy:
        st.subheader("Disease Information")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Disease Name", remedy.get("disease_name", "Unknown"))
        with col2:
            st.metric("Plant Type", remedy.get("plant", "Unknown"))
        with col3:
            severity = remedy.get("severity", "Unknown")
            if severity == "Very High":
                st.error(f"Severity: {severity}")
            elif severity == "High":
                st.warning(f"Severity: {severity}")
            else:
                st.info(f"Severity: {severity}")
        
        # Symptoms
        st.subheader("Symptoms")
        for symptom in remedy.get("symptoms", []):
            st.write(f"• {symptom}")
        
        # Treatment tabs
        tab1, tab2, tab3 = st.tabs(["Organic Treatment", "Chemical Treatment", "Prevention"])
        
        with tab1:
            st.write("**Organic & Natural Treatment Options:**")
            for treatment in remedy.get("organic_treatment", []):
                st.write(f"✓ {treatment}")
        
        with tab2:
            treatments = remedy.get("chemical_treatment", [])
            if treatments:
                st.write("**Chemical Treatment Options:**")
                for treatment in treatments:
                    st.write(f"✓ {treatment}")
            else:
                st.warning("No chemical treatment available (viral disease)")
        
        with tab3:
            st.write("**Prevention Strategies:**")
            for prevention in remedy.get("prevention", []):
                st.write(f"✓ {prevention}")
    else:
        st.error("Treatment information not available for this disease")


def main():
    """Main Streamlit app."""
    
    # Page configuration
    st.set_page_config(
        page_title="Smart Crop Health Monitor",
        page_icon="🌾",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("🌾 Smart Crop Health Monitor")
    st.markdown("### AI-Powered Plant Disease Detection & Treatment Recommendation System")
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.info(
            "This application uses deep learning to:\n"
            "1. Analyze leaf images\n"
            "2. Detect plant diseases\n"
            "3. Recommend treatments\n\n"
            "**Upload a clear leaf image** to get started!"
        )
        
        st.header("Model Info")
        st.write(
            "- **Model**: MobileNetV2 with Transfer Learning\n"
            "- **Dataset**: PlantVillage\n"
            "- **Classes**: 15 disease types\n"
            "- **Input Size**: 224×224 pixels"
        )
        
        st.header("Supported Plants")
        st.write(
            "- 🫑 Pepper (Bell)\n"
            "- 🥔 Potato\n"
            "- 🍅 Tomato"
        )
    
    # Main content
    tabs = st.tabs(["🔍 Disease Detection", "📚 Disease Database", "ℹ️ Instructions"])
    
    # Tab 1: Disease Detection
    with tabs[0]:
        # Load model
        with st.spinner("Loading model..."):
            try:
                predictor, class_names = load_model_and_classes()
                model_loaded = predictor.model is not None
            except Exception as e:
                st.error(f"Error loading model: {e}")
                model_loaded = False
        
        if not model_loaded:
            st.error(
                "❌ Model not found at `models/plant_model.h5`\n\n"
                "Please train the model first using:\n"
                "`python src/train.py`"
            )
            return
        
        st.success("✓ Model loaded successfully!")
        
        # Image input
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.subheader("Upload Image")
            uploaded_file = st.file_uploader(
                "Choose a leaf image",
                type=["jpg", "jpeg", "png", "bmp"],
                help="Upload a clear photo of a leaf"
            )
        
        with col2:
            st.subheader("Camera Capture")
            camera_image = st.camera_input("Take a photo")
        
        # Process image
        image_to_process = None
        if uploaded_file is not None:
            image_to_process = Image.open(uploaded_file).convert("RGB")
        elif camera_image is not None:
            image_to_process = Image.open(camera_image).convert("RGB")
        
        if image_to_process is not None:
            # Display image
            st.subheader("Uploaded Image")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.image(image_to_process, use_container_width=True)
            
            with col2:
                st.write(f"**Size**: {image_to_process.size}")
                st.write(f"**Format**: {image_to_process.format}")
            
            # Make prediction
            if st.button("🔍 Analyze Disease", use_container_width=True, type="primary"):
                with st.spinner("Analyzing image..."):
                    try:
                        # Convert PIL to numpy
                        img_array = np.array(image_to_process)
                        
                        # Make prediction
                        results = predictor.predict_with_remedy(img_array)
                        
                        if results:
                            display_prediction_results(results)
                        else:
                            st.error("Error making prediction. Please try another image.")
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        st.write("Please try uploading a different image.")
    
    # Tab 2: Disease Database
    with tabs[1]:
        st.subheader("Plant Disease Database")
        
        disease_list = get_all_diseases()
        selected_disease = st.selectbox(
            "Select a disease to learn more",
            disease_list,
            format_func=format_disease_name
        )
        
        if selected_disease:
            remedy = get_remedy(selected_disease)
            if remedy:
                # Disease header
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Disease", remedy.get("disease_name", "Unknown"))
                with col2:
                    st.metric("Plant", remedy.get("plant", "Unknown"))
                with col3:
                    st.metric("Severity", remedy.get("severity", "Unknown"))
                
                # Symptoms
                st.subheader("🔍 Symptoms")
                for symptom in remedy.get("symptoms", []):
                    st.write(f"• {symptom}")
                
                # Treatment options
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🌿 Organic Treatment")
                    for treatment in remedy.get("organic_treatment", []):
                        st.write(f"• {treatment}")
                
                with col2:
                    st.subheader("⚗️ Chemical Treatment")
                    treatments = remedy.get("chemical_treatment", [])
                    if treatments:
                        for treatment in treatments:
                            st.write(f"• {treatment}")
                    else:
                        st.info("No chemical treatment available")
                
                # Prevention
                st.subheader("🛡️ Prevention")
                for prevention in remedy.get("prevention", []):
                    st.write(f"• {prevention}")
    
    # Tab 3: Instructions
    with tabs[2]:
        st.subheader("How to Use")
        
        st.markdown("""
        ### Step 1: Prepare Your Image
        - Take a clear photo of an affected leaf
        - Ensure good lighting
        - Include the entire leaf in frame
        - Avoid shadows and reflections
        
        ### Step 2: Upload Image
        - Click "Choose a leaf image" or "Take a photo"
        - Supported formats: JPG, PNG, BMP
        
        ### Step 3: Analyze
        - Click "Analyze Disease" button
        - Wait for AI analysis
        
        ### Step 4: Review Results
        - See predicted disease with confidence score
        - Read detailed disease information
        - Check treatment recommendations
        
        ### Tips for Best Results
        - **Lighting**: Use natural daylight
        - **Focus**: Keep the leaf sharp and clear
        - **Size**: Leaf should take up most of the image
        - **Angle**: Photograph at 45-90 degree angle
        - **Health**: Include both healthy and affected areas
        
        ### Supported Diseases
        """)
        
        # Display supported diseases
        disease_groups = {}
        for disease in get_class_names():
            if "Pepper" in disease:
                plant = "🫑 Pepper"
            elif "Potato" in disease:
                plant = "🥔 Potato"
            elif "Tomato" in disease:
                plant = "🍅 Tomato"
            else:
                plant = "Unknown"
            
            if plant not in disease_groups:
                disease_groups[plant] = []
            disease_groups[plant].append(disease)
        
        for plant, diseases in disease_groups.items():
            st.write(f"\n**{plant}**")
            for disease in diseases:
                st.write(f"  • {format_disease_name(disease)}")
        
        st.markdown("""
        ### Training Your Own Model
        To train the model with your own dataset:
        ```bash
        python src/train.py
        ```
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
        🌾 Smart Crop Health Monitor | AI-Powered Agriculture 🤖
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
