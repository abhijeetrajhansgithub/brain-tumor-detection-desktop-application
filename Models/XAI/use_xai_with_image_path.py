import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt


def preprocess_image(img_path, target_size=(150, 150)):
    """Load and preprocess the image for model input."""
    img = image.load_img(img_path, target_size=target_size)
    print("1. type(img):", type(img))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize
    return img_array


def make_gradcam_heatmap(model, img_array, last_conv_layer_name):
    """Generate Grad-CAM heatmap for explainability."""
    grad_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        top_class = tf.argmax(predictions[0])
        class_channel = predictions[:, top_class]

    grads = tape.gradient(class_channel, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]

    heatmap = tf.reduce_mean(tf.multiply(pooled_grads, conv_outputs), axis=-1)
    heatmap = np.maximum(heatmap, 0)  # ReLU
    heatmap /= np.max(heatmap)

    return heatmap


def overlay_heatmap(img_path, heatmap, alpha=0.4):
    """Overlay the heatmap on the original image."""

    img = cv2.imread(img_path)
    print("30. type(img):", type(img))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))

    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    overlayed_img = cv2.addWeighted(img, 1 - alpha, heatmap, alpha, 0)

    plt.figure(figsize=(8, 8))
    plt.imshow(overlayed_img)
    plt.axis('off')
    plt.show()


def classify_and_explain(h5_model, keras_model, image_path):
    """Classify image and generate explainability heatmap using Grad-CAM."""
    try:
        model = load_model(h5_model)  # Try loading .h5 model
    except:
        model = load_model(keras_model)  # Fallback to .keras model

    img_array = preprocess_image(image_path)

    print("2. type(img_array):", type(img_array))

    # Make prediction
    preds = model.predict(img_array)
    predicted_class = np.argmax(preds)

    # Generate Grad-CAM heatmap
    last_conv_layer = "conv2d_5"  # Last convolutional layer in your model
    heatmap = make_gradcam_heatmap(model, img_array, last_conv_layer)

    # Display results
    print(f"Predicted class: {predicted_class} (Confidence: {preds[0][predicted_class]:.2f})")
    overlay_heatmap(image_path, heatmap)


# ✅ Example Usage
classify_and_explain(
    "../model_v01_xai/btcm-mdl-v01-xai.h5",
    "../model_v01_xai/btcm-mdl-v01-xai.keras",
    "../../Image/image.jpg"
)
