import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2, ResNet50
from tensorflow.keras.layers import (
    Dense, Dropout, GlobalAveragePooling2D, BatchNormalization, Conv2D, MaxPooling2D
)


def create_custom_cnn(input_shape=(224, 224, 3), num_classes=10):
    """
    Create a custom CNN model for plant disease classification.
    
    Args:
        input_shape: Shape of input images (height, width, channels)
        num_classes: Number of disease classes
        
    Returns:
        model: Compiled Keras model
    """
    model = models.Sequential([
        # Block 1
        Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=input_shape),
        BatchNormalization(),
        Conv2D(32, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        Dropout(0.25),
        
        # Block 2
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        Dropout(0.25),
        
        # Block 3
        Conv2D(128, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        Conv2D(128, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        Dropout(0.25),
        
        # Block 4
        Conv2D(256, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        Conv2D(256, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        Dropout(0.25),
        
        # Global pooling and dense layers
        GlobalAveragePooling2D(),
        Dense(512, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(256, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    
    return model


def create_mobilenetv2_model(input_shape=(224, 224, 3), num_classes=10):
    """
    Create a transfer learning model using MobileNetV2.
    Good for faster inference and smaller model size.
    
    Args:
        input_shape: Shape of input images
        num_classes: Number of disease classes
        
    Returns:
        model: Compiled Keras model
    """
    # Load pre-trained MobileNetV2
    base_model = MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model weights
    base_model.trainable = False
    
    # Add custom layers
    model = models.Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(256, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    
    return model


def create_resnet50_model(input_shape=(224, 224, 3), num_classes=10):
    """
    Create a transfer learning model using ResNet50.
    More powerful but slower inference.
    
    Args:
        input_shape: Shape of input images
        num_classes: Number of disease classes
        
    Returns:
        model: Compiled Keras model
    """
    # Load pre-trained ResNet50
    base_model = ResNet50(
        input_shape=input_shape,
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model weights
    base_model.trainable = False
    
    # Add custom layers
    model = models.Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(512, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(256, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    
    return model


def compile_model(model, learning_rate=0.001):
    """
    Compile the model with appropriate optimizer and loss function.
    
    Args:
        model: Keras model to compile
        learning_rate: Learning rate for optimizer
        
    Returns:
        model: Compiled model
    """
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    
    model.compile(
        optimizer=optimizer,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.SparseTopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    return model


def get_model(model_type='custom', input_shape=(224, 224, 3), num_classes=10):
    """
    Factory function to create and compile a model.
    
    Args:
        model_type: 'custom', 'mobilenetv2', or 'resnet50'
        input_shape: Shape of input images
        num_classes: Number of disease classes
        
    Returns:
        model: Compiled Keras model
    """
    if model_type == 'custom':
        model = create_custom_cnn(input_shape, num_classes)
    elif model_type == 'mobilenetv2':
        model = create_mobilenetv2_model(input_shape, num_classes)
    elif model_type == 'resnet50':
        model = create_resnet50_model(input_shape, num_classes)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    model = compile_model(model)
    return model
