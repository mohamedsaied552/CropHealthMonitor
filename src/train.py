import os
import sys
import json
import tensorflow as tf
import numpy as np
from tensorflow.keras.callbacks import (
    EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import DataLoader
from src.model import get_model

AUTOTUNE = tf.data.AUTOTUNE


def _build_datasets(dataset_path, img_size, batch_size, validation_split=0.2):
    """Build memory-efficient train/validation datasets from disk."""
    loader = DataLoader(dataset_path=dataset_path, img_size=img_size)
    class_names = loader._discover_class_dirs()

    if not class_names:
        raise RuntimeError(
            f"No image classes found in {dataset_path}. "
            "Ensure PlantVillage disease folders are present."
        )

    common = dict(
        directory=dataset_path,
        class_names=class_names,
        labels="inferred",
        label_mode="int",
        color_mode="rgb",
        batch_size=batch_size,
        image_size=(img_size, img_size),
        shuffle=True,
        seed=42,
        validation_split=validation_split,
    )

    train_ds = tf.keras.utils.image_dataset_from_directory(
        subset="training", **common
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        subset="validation", **common
    )

    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.2),
        tf.keras.layers.RandomZoom(0.2),
    ], name="augmentation")

    def preprocess_train(image, label):
        image = tf.cast(image, tf.float32) / 255.0
        image = data_augmentation(image, training=True)
        return image, label

    def preprocess_val(image, label):
        image = tf.cast(image, tf.float32) / 255.0
        return image, label

    train_ds = (
        train_ds.map(preprocess_train, num_parallel_calls=AUTOTUNE)
        .prefetch(AUTOTUNE)
    )
    val_ds = (
        val_ds.map(preprocess_val, num_parallel_calls=AUTOTUNE)
        .prefetch(AUTOTUNE)
    )

    return train_ds, val_ds, class_names


def train_model(
    dataset_path="dataset/PlantVillage",
    model_type="mobilenetv2",
    epochs=50,
    batch_size=32,
    learning_rate=0.001,
    model_save_path="../models/plant_model.h5",
):
    print("=" * 60)
    print("SMART CROP HEALTH MONITOR - MODEL TRAINING")
    print("=" * 60)

    print("\n[1/4] Building datasets from disk...")
    train_ds, val_ds, class_names = _build_datasets(
        dataset_path, img_size=224, batch_size=batch_size, validation_split=0.2
    )
    print(f"Classes ({len(class_names)}): {class_names}")
    print(f"Training batches: {len(train_ds)}, Validation batches: {len(val_ds)}")

    print(f"\n[2/4] Creating {model_type} model...")
    model = get_model(model_type=model_type, num_classes=len(class_names))
    model.summary()

    os.makedirs(os.path.dirname(model_save_path) or ".", exist_ok=True)

    print("\n[3/4] Setting up callbacks...")
    callbacks = [
        EarlyStopping(
            monitor="val_loss",
            patience=8,
            restore_best_weights=True,
            verbose=1,
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=4,
            min_lr=1e-7,
            verbose=1,
        ),
        ModelCheckpoint(
            model_save_path,
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1,
        ),
    ]

    print("\n[4/4] Training model...")
    print(f"Batch size: {batch_size}, Epochs: {epochs}")

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks,
        verbose=1,
    )

    print("\n" + "=" * 60)
    print("VALIDATION RESULTS")
    print("=" * 60)
    val_loss, val_accuracy, val_top3 = model.evaluate(val_ds, verbose=0)
    print(f"Val Loss: {val_loss:.4f}")
    print(f"Val Accuracy: {val_accuracy:.4f} ({val_accuracy * 100:.2f}%)")
    print(f"Val Top-3 Accuracy: {val_top3:.4f} ({val_top3 * 100:.2f}%)")

    class_names_path = os.path.join(
        os.path.dirname(model_save_path), "class_names.json"
    )
    with open(class_names_path, "w", encoding="utf-8") as f:
        json.dump(class_names, f, indent=2)

    print("\n" + "=" * 60)
    print(f"Model saved to: {model_save_path}")
    print(f"Class names saved to: {class_names_path}")
    print("=" * 60)

    return model, history, class_names


if __name__ == "__main__":
    model, history, class_names = train_model(
        dataset_path="dataset/PlantVillage",
        model_type="mobilenetv2",
        epochs=12,
        batch_size=32,
        learning_rate=0.001,
        model_save_path="../models/plant_model.h5",
    )

    print("\nTraining completed successfully!")
    print(f"Trained model can classify {len(class_names)} disease classes")
