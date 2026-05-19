"""
Prediction and inference utilities for the plant disease classifier.
"""

import os
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from src.remedies import get_remedy, get_disease_info


class PlantDiseasePredictor:
    """Load model and make predictions on plant leaf images."""
    
    def __init__(self, model_path="../models/plant_model.h5", img_size=224):
        """
        Initialize the predictor with a trained model.
        
        Args:
            model_path: Path to the saved model file
            img_size: Size of input images
        """
        self.img_size = img_size
        self.model_path = model_path
        self.model = None
        self.class_names = None
        
        if os.path.isfile(model_path) and os.path.getsize(model_path) > 1000:
            self.load_model()
        else:
            print(f"Warning: Model not found or empty at {model_path}")
    
    def load_model(self):
        """Load the trained model."""
        try:
            self.model = tf.keras.models.load_model(self.model_path)
            print(f"Model loaded successfully from {self.model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
    
    def set_class_names(self, class_names):
        """Set the class names for predictions."""
        self.class_names = class_names
    
    def preprocess_image(self, image_path_or_array):
        """
        Preprocess an image for prediction.
        
        Args:
            image_path_or_array: File path to image, PIL image, or numpy array
            
        Returns:
            Preprocessed image as numpy array
        """
        if isinstance(image_path_or_array, str):
            img = cv2.imread(image_path_or_array)
            if img is None:
                raise ValueError(f"Could not read image from {image_path_or_array}")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        elif isinstance(image_path_or_array, Image.Image):
            img = np.array(image_path_or_array)
        else:
            img = image_path_or_array
        
        if img is None:
            raise ValueError("Invalid image provided for preprocessing.")
        
        if isinstance(img, np.ndarray):
            if img.ndim == 2:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            elif img.ndim == 3 and img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
            elif img.ndim == 3 and img.shape[2] == 3:
                pass
            else:
                raise ValueError("Unsupported image array shape for preprocessing.")
        else:
            raise ValueError("Image must be a file path, PIL Image, or numpy array.")

        img = cv2.resize(img, (self.img_size, self.img_size))
        
        # Normalize to [0, 1]
        img = img.astype(np.float32) / 255.0
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        
        return img
    
    def predict(self, image_path_or_array, top_k=3):
        """
        Predict disease on an image.
        
        Args:
            image_path_or_array: File path to image or numpy array
            top_k: Return top K predictions
            
        Returns:
            dict: Prediction results including top classes and confidences
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Please load a model first.")
        
        if self.class_names is None:
            raise RuntimeError("Class names not set. Use set_class_names() first.")
        
        try:
            # Preprocess image
            img = self.preprocess_image(image_path_or_array)
            
            # Make prediction
            predictions = self.model.predict(img, verbose=0)[0]
            
            # Get top K predictions
            top_indices = np.argsort(predictions)[-top_k:][::-1]
            
            results = {
                "predicted_class": self.class_names[top_indices[0]],
                "confidence": float(predictions[top_indices[0]]),
                "top_predictions": [
                    {
                        "class": self.class_names[idx],
                        "confidence": float(predictions[idx])
                    }
                    for idx in top_indices
                ],
                "all_predictions": {
                    self.class_names[i]: float(predictions[i])
                    for i in range(len(predictions))
                }
            }
            
            return results
        
        except Exception as e:
            print(f"Error during prediction: {e}")
            return None
    
    def predict_with_remedy(self, image_path_or_array):
        """
        Predict disease and get treatment recommendations.
        
        Args:
            image_path_or_array: File path to image or numpy array
            
        Returns:
            dict: Prediction results with treatment information
        """
        prediction = self.predict(image_path_or_array, top_k=3)
        
        if prediction is None:
            return None
        
        predicted_class = prediction["predicted_class"]
        remedy = get_remedy(predicted_class)
        
        result = {
            "prediction": prediction,
            "remedy": remedy,
            "disease_info": get_disease_info(predicted_class)
        }
        
        return result


def preprocess_pil_image(pil_image, img_size=224):
    """
    Preprocess a PIL image for prediction.
    
    Args:
        pil_image: PIL Image object
        img_size: Target size
        
    Returns:
        Preprocessed image as numpy array with batch dimension
    """
    # Convert to numpy array
    img = np.array(pil_image)
    
    # If grayscale, convert to RGB
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    elif img.shape[2] == 4:  # RGBA
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    
    # Resize
    img = cv2.resize(img, (img_size, img_size))
    
    # Normalize
    img = img.astype(np.float32) / 255.0
    
    # Add batch dimension
    img = np.expand_dims(img, axis=0)
    
    return img
