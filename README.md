# 🌾 Smart Crop Health Monitor - ML Plant Disease Detector

An intelligent, AI-powered system that analyzes leaf images to detect plant diseases and recommend treatment options.

## 🎯 Features

- **AI Disease Detection**: Upload a leaf image and get instant disease predictions
- **Multi-Plant Support**: Detects diseases in Pepper, Potato, and Tomato plants
- **Treatment Recommendations**: Provides both organic and chemical treatment options
- **Prevention Guidelines**: Detailed prevention strategies for each disease
- **User-Friendly Interface**: Streamlit-based web application
- **Transfer Learning**: Uses pre-trained MobileNetV2 for fast, accurate predictions
- **Disease Database**: Browse comprehensive information about all supported diseases

## 🌱 Supported Diseases

### Pepper (Bell)
- Bacterial Spot
- Healthy

### Potato
- Early Blight
- Late Blight
- Healthy

### Tomato
- Bacterial Spot
- Early Blight
- Late Blight
- Leaf Mold
- Septoria Leaf Spot
- Target Spot
- Tomato Mosaic Virus (ToMV)
- Tomato Yellow Leaf Curl Virus (TYLCV)
- Two-Spotted Spider Mites
- Healthy

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 2GB+ of available disk space for model and dataset
- A webcam or image files for testing

## 🚀 Quick Start

### 1. Clone/Setup the Project

```bash
cd d:\Projects\ML & BigData\CropHealthMonitor
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Train the Model (First Time Only)

If you have the PlantVillage dataset:

```bash
python src/train.py
```

This will:
- Load images from `dataset/PlantVillage/`
- Create a MobileNetV2 transfer learning model
- Train for up to 50 epochs with early stopping
- Save the model to `models/plant_model.h5`
- Display training metrics and test accuracy

⏱️ **Training Time**: 30-60 minutes depending on your GPU/CPU

### 5. Run the Web Application

```bash
streamlit run app/app.py
```

The app will open in your browser at `http://localhost:8501`

## 📊 Project Structure

```
CropHealthMonitor/
├── app/
│   └── app.py                 # Main Streamlit web application
├── src/
│   ├── data_loader.py         # Dataset loading and preprocessing
│   ├── model.py               # CNN and transfer learning models
│   ├── predict.py             # Inference and prediction utilities
│   ├── remedies.py            # Disease treatment database
│   └── train.py               # Training script
├── dataset/
│   └── PlantVillage/          # Plant disease image dataset
├── models/
│   └── plant_model.h5         # Trained model (generated after training)
├── notebooks/                 # Jupyter notebooks (optional)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🔧 Usage Guide

### Using the Web Application

1. **Disease Detection Tab**:
   - Upload an image or take a photo with your camera
   - Click "Analyze Disease"
   - View predictions with confidence scores
   - Get treatment recommendations

2. **Disease Database Tab**:
   - Browse all diseases in the database
   - Select a disease to view detailed information
   - Read symptoms, treatments, and prevention tips

3. **Instructions Tab**:
   - Learn best practices for uploading images
   - View supported diseases by plant type
   - Get tips for accurate predictions

### Image Upload Tips

✅ **DO**:
- Use clear, well-lit photos
- Include the entire leaf in frame
- Include both healthy and affected areas
- Use high-resolution images
- Take photos at 45-90 degree angles

❌ **DON'T**:
- Use blurry or dark images
- Crop the leaf too tightly
- Include shadows or reflections
- Use very zoomed-in photos
- Upload images of healthy plants only

## 🧠 Model Architecture

### Available Models

1. **MobileNetV2** (Recommended) ⭐
   - Faster inference (< 1 second)
   - Smaller model size (50-100MB)
   - Good accuracy for mobile deployment
   - Default model used

2. **Custom CNN**
   - 4-block convolutional architecture
   - ~50M parameters
   - Good accuracy but slower inference

3. **ResNet50**
   - More powerful but slower
   - Larger model size (~200MB)
   - Best accuracy but high computation

### Model Performance

Expected metrics after training:
- **Accuracy**: 95-98%
- **Top-3 Accuracy**: 99%+
- **Inference Time**: <1 second per image
- **Model Size**: ~50MB (MobileNetV2)

## 📚 Treatment Recommendations

Each disease includes:

### 🌿 Organic Treatment
- Natural and sustainable methods
- No chemical pesticides
- Environmentally friendly approaches

### ⚗️ Chemical Treatment
- Effective chemical interventions
- Professional-grade solutions
- Safety precautions included

### 🛡️ Prevention
- Long-term disease management
- Cultural practices
- Resistant variety selection

## 🔍 Model Training Details

### Training Process

```python
# Custom training example
from src.data_loader import DataLoader
from src.model import get_model

# Load data
loader = DataLoader("dataset/PlantVillage")
X, y, classes = loader.load_dataset()

# Split data
X_train, X_val, X_test, y_train, y_val, y_test = loader.split_dataset(X, y)

# Create and train model
model = get_model("mobilenetv2", num_classes=len(classes))
history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=50)
```

### Transfer Learning

The model uses:
- **Pre-trained Weights**: ImageNet weights from MobileNetV2
- **Fine-tuning**: Custom dense layers for disease classification
- **Data Augmentation**: Rotation, zoom, shift, flip
- **Early Stopping**: Prevents overfitting
- **Learning Rate Reduction**: Adaptive learning rate scheduling

## 🎓 Making Predictions Programmatically

```python
from src.predict import PlantDiseasePredictor

# Initialize predictor
predictor = PlantDiseasePredictor("models/plant_model.h5")
predictor.set_class_names(class_names)

# Predict on image
results = predictor.predict_with_remedy("leaf_image.jpg")

# Access results
predicted_disease = results["prediction"]["predicted_class"]
confidence = results["prediction"]["confidence"]
treatment = results["remedy"]

print(f"Disease: {predicted_disease}")
print(f"Confidence: {confidence * 100:.2f}%")
print(f"Treatment: {treatment['organic_treatment']}")
```

## 📈 Performance Optimization

### For CPU-only Systems
```bash
# Use a smaller model
# Edit training to use custom CNN instead of MobileNetV2
```

### For GPU Acceleration
```bash
# Install GPU support
pip install tensorflow[and-cuda]
```

### Inference Optimization
```python
# Use quantized model for faster inference
converter = tf.lite.TFLiteConverter.from_saved_model("model_path")
tflite_model = converter.convert()
```

## 🐛 Troubleshooting

### Model Not Found
**Error**: "Model not found at models/plant_model.h5"
**Solution**: Train the model first: `python src/train.py`

### Out of Memory
**Error**: GPU out of memory during training
**Solution**: 
- Reduce batch size: `batch_size=16` in train.py
- Use CPU: Set `CUDA_VISIBLE_DEVICES=""` before running

### Slow Inference
**Problem**: Predictions taking >5 seconds
**Solution**:
- Verify GPU is being used: Check TensorFlow output
- Use smaller image size: Change to 128x128
- Use CPU quantization

### Inaccurate Predictions
**Problem**: Wrong disease classifications
**Solution**:
- Use clearer images
- Include more of the affected area
- Retrain with more data
- Try different model architectures

## 📦 Dependencies

Key packages used:
- **TensorFlow 2.14**: Deep learning framework
- **Keras**: Neural network API
- **OpenCV**: Image processing
- **NumPy/Pandas**: Data manipulation
- **Streamlit**: Web interface
- **Pillow**: Image handling
- **Scikit-learn**: ML utilities

See `requirements.txt` for complete list.

## 🤝 Contributing

To add new diseases:

1. **Update Dataset**: Add images to `dataset/PlantVillage/NewDisease/`
2. **Update Remedies**: Add treatment info in `src/remedies.py`
3. **Retrain Model**: Run `python src/train.py`
4. **Test**: Verify predictions in the web app

## 📄 License

This project is open source and available for educational and research purposes.

## 🔗 Resources

### Dataset
- PlantVillage Dataset: https://plantvillage.psu.edu/

### References
- MobileNetV2 Paper: https://arxiv.org/abs/1801.04381
- Transfer Learning: https://cs231n.github.io/transfer-learning/

## ❓ FAQ

**Q: How accurate is the model?**
A: The model achieves 95-98% accuracy on the test set. Accuracy depends on image quality.

**Q: Can I use this on my phone?**
A: Yes! MobileNetV2 is designed for mobile. Use TensorFlow Lite for deployment.

**Q: What if my plant isn't supported?**
A: You can add new plants by collecting images and retraining the model.

**Q: How often should I update the model?**
A: Retrain quarterly with new images to improve accuracy.

**Q: Can I use this commercially?**
A: Check the PlantVillage dataset license and comply with all terms.

## 📞 Support

For issues or questions:
1. Check the README and FAQ
2. Review error messages carefully
3. Check the Streamlit app instructions tab
4. Verify your dataset structure matches the expected format

---

**Happy Crop Monitoring! 🌾🤖**
