import os
import cv2
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator


class DataLoader:
    """Load and preprocess plant disease images from the PlantVillage dataset."""
    
    def __init__(self, dataset_path="dataset/PlantVillage", img_size=224):
        """
        Initialize the data loader.
        
        Args:
            dataset_path: Path to the PlantVillage dataset
            img_size: Size to resize images to (img_size x img_size)
        """
        self.dataset_path = dataset_path
        self.img_size = img_size
        self.images = []
        self.labels = []
        self.class_names = []
        self.class_to_idx = {}
        
    def _discover_class_dirs(self):
        """Return disease class folders, excluding nested dataset wrappers."""
        skip = {"PlantVillage", "__MACOSX", ".git"}
        class_dirs = []
        for name in sorted(os.listdir(self.dataset_path)):
            if name in skip:
                continue
            path = os.path.join(self.dataset_path, name)
            if not os.path.isdir(path):
                continue
            has_images = any(
                f.lower().endswith((".png", ".jpg", ".jpeg"))
                for root, _, files in os.walk(path)
                for f in files
            )
            if has_images:
                class_dirs.append(name)
        return class_dirs

    def _iter_image_paths(self, class_path):
        """Yield image paths under a class folder (recursive)."""
        for root, _, files in os.walk(class_path):
            for img_file in files:
                if img_file.lower().endswith((".png", ".jpg", ".jpeg")):
                    yield os.path.join(root, img_file)

    def load_dataset(self, max_per_class=None):
        """
        Load images and labels from the dataset directory.

        Args:
            max_per_class: Cap images per class (limits RAM use on large datasets)

        Returns:
            X: numpy array of images
            y: numpy array of labels (integers)
            class_names: list of disease class names
        """
        print(f"Loading dataset from {self.dataset_path}...")
        self.images = []
        self.labels = []

        class_dirs = self._discover_class_dirs()
        self.class_names = class_dirs
        self.class_to_idx = {cls: idx for idx, cls in enumerate(class_dirs)}

        for class_idx, class_name in enumerate(class_dirs):
            class_path = os.path.join(self.dataset_path, class_name)
            paths = list(self._iter_image_paths(class_path))
            if max_per_class and len(paths) > max_per_class:
                rng = np.random.default_rng(42)
                paths = list(rng.choice(paths, size=max_per_class, replace=False))

            print(f"Loading {class_name} ({len(paths)} images)...")
            for img_path in paths:
                try:
                    img = cv2.imread(img_path)
                    if img is None:
                        continue
                    img = cv2.resize(img, (self.img_size, self.img_size))
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img = img.astype(np.float32) / 255.0
                    self.images.append(img)
                    self.labels.append(class_idx)
                except Exception as e:
                    print(f"Error loading {img_path}: {e}")

        X = np.array(self.images, dtype=np.float32)
        y = np.array(self.labels, dtype=np.int32)
        print(f"Loaded {len(X)} images across {len(class_dirs)} classes")
        return X, y, self.class_names
    
    def split_dataset(self, X, y, test_size=0.2, val_size=0.1):
        """
        Split dataset into train, validation, and test sets.
        
        Args:
            X: Images array
            y: Labels array
            test_size: Proportion of test set
            val_size: Proportion of validation set (from training data)
            
        Returns:
            X_train, X_val, X_test, y_train, y_val, y_test
        """
        # First split: separate test set
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Second split: separate validation from training
        val_size_adjusted = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_size_adjusted, 
            random_state=42, stratify=y_temp
        )
        
        print(f"Train set: {len(X_train)} images")
        print(f"Validation set: {len(X_val)} images")
        print(f"Test set: {len(X_test)} images")
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def get_data_generators(self, X_train, X_val, batch_size=32):
        """
        Create data augmentation generators for training and validation.
        
        Args:
            X_train: Training images
            X_val: Validation images
            batch_size: Batch size for training
            
        Returns:
            train_gen, val_gen: Data generators
        """
        train_datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )
        
        val_datagen = ImageDataGenerator()
        
        # Note: When using fit_generator, pass in batches
        # This is a simple approach for non-generator training
        return train_datagen, val_datagen
