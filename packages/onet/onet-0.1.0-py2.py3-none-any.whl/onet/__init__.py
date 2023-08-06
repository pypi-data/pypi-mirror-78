"""Core module of the project."""

from pathlib import Path
from typing import Iterable, NewType, Tuple

import numpy as np
import tensorflow as tf
from tensorflow.keras import Model

tf.get_logger().setLevel('ERROR')

# %% TYPES

Proba = NewType('Proba', float)
Prediction = Tuple[Path, Proba]

# %% DEFAULTS

DEFAULT_EPOCHS = 3
DEFAULT_BATCH_SIZE = 32
DEFAULT_COLOR_MODE = "rgb"
DEFAULT_BASE_MODEL = "EfficientNetB0"

# %% CONSTANTS

COLOR_MODES = [
    "rgb",
    "rgba",
    "grayscale",
]
BASE_MODELS = [
    "EfficientNetB0",
    "EfficientNetB1",
    "EfficientNetB2",
    "EfficientNetB3",
    "EfficientNetB4",
    "EfficientNetB5",
    "EfficientNetB6",
    "EfficientNetB7",
]
INPUT_MODES = {
    3: "rgb",
    4: "rgba",
    1: "grayscale",
}
INPUT_SIZES = {
    "efficientnetb0": (224, 224),
    "efficientnetb1": (240, 240),
    "efficientnetb2": (260, 260),
    "efficientnetb3": (300, 300),
    "efficientnetb4": (380, 380),
    "efficientnetb5": (456, 456),
    "efficientnetb6": (528, 528),
    "efficientnetb7": (600, 600),
}


# %% PROCEDURES

def train(
        directory: Path,
        epochs: int = DEFAULT_EPOCHS,
        batch_size: int = DEFAULT_BATCH_SIZE,
        base_model: str = DEFAULT_BASE_MODEL,
        color_mode: str = DEFAULT_COLOR_MODE,
) -> Model:
    """Train a machine learning model for binary image classification."""
    # configure the model
    image_size = INPUT_SIZES[base_model.lower()]
    application = getattr(tf.keras.applications, base_model)
    base_model = application(weights="imagenet", include_top=False)
    base_model.trainable = False
    metrics = [
        tf.keras.metrics.Recall(),
        tf.keras.metrics.Accuracy(),
        tf.keras.metrics.Precision(),
    ]
    optimizer = tf.keras.optimizers.Adam()
    loss = tf.keras.losses.BinaryCrossentropy()

    # initialize the model
    model = tf.keras.Sequential(
        [
            base_model,
            # rebuild the top layer from the base model
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(rate=0.2),
            # set the final prediction layer
            tf.keras.layers.Dense(1, activation='sigmoid'),
        ]
    )
    model.compile(
        loss=loss,
        metrics=metrics,
        optimizer=optimizer,
    )
    model.summary()

    # load the dataset
    train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        directory=directory,
        color_mode=color_mode,
        image_size=image_size,
        batch_size=batch_size,
        label_mode="binary",
        labels="inferred",
        shuffle=True,
    ).prefetch(tf.data.experimental.AUTOTUNE)
    # TODO: allow to change valid dataset
    valid_dataset = train_dataset

    # train the model
    model.fit(
        train_dataset,
        epochs=epochs,
        validation_data=valid_dataset,
    )

    return model


def predict(model: Path, directory: Path) -> Iterable[Prediction]:
    """Predict the labels for binary image classification."""
    # load the model
    model = tf.keras.models.load_model(model)

    # infer the input
    base_model = model.input.name.split('_')[0]
    mode = INPUT_MODES[model.input.shape[3]]
    size = INPUT_SIZES[base_model]

    # generate predictions
    for path in Path(directory).rglob('*.*'):
        image = tf.keras.preprocessing.image.load_img(
            path,
            color_mode=mode,
            target_size=size,
        )
        array = tf.keras.preprocessing.image.img_to_array(image)
        batch = np.expand_dims(array, axis=0)
        predictions = model.predict(batch)
        prediction = predictions[0][0]
        yield path, prediction
