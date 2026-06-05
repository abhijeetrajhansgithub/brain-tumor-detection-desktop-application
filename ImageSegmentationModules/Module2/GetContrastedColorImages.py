import PyQt5
import cv2
import numpy as np
from PyQt5.QtGui import QPixmap, QImage


def enhance_contrast(image, levels=24):
    """Generate contrast-enhanced versions of an image using CLAHE."""
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    contrast_images = []
    for i in range(1, levels + 1):
        clip_limit = i * 1.5  # Increase contrast progressively
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
        l_enhanced = clahe.apply(l)
        enhanced_lab = cv2.merge([l_enhanced, a, b])
        enhanced_image = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        contrast_images.append(enhanced_image)

    return contrast_images


def segment_and_highlight(image):
    """Apply K-Means clustering after filtering."""
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    median_blurred = cv2.medianBlur(blurred, 5)
    bilateral_filtered = cv2.bilateralFilter(median_blurred, 9, 75, 75)

    # K-Means Clustering
    pixel_values = bilateral_filtered.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)

    k = 3  # Number of clusters
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    segmented_image = centers[labels.flatten()].reshape(image.shape)

    return segmented_image


def apply_color_buckets(image):
    """Color shade pixels based on contrast similarity buckets."""
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    max_val = grayscale.max()
    bucket_size = 10

    output = np.zeros_like(image)

    # Bright, contrasting colors
    colors = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255),  # Red, Green, Blue
        (255, 165, 0), (255, 255, 0), (0, 255, 255),  # Orange, Yellow, Cyan
        (128, 0, 128), (75, 0, 130), (0, 191, 255),  # Purple, Indigo, Deep Sky Blue
        (255, 105, 180), (255, 223, 0), (50, 205, 50),  # Hot Pink, Gold, Lime Green
    ]

    for i in range(0, max_val + 1, bucket_size):
        mask = (grayscale >= i) & (grayscale < i + bucket_size)
        output[mask] = colors[(i // bucket_size) % len(colors)]

    return output


def process_images(image_path):
    """Process the image, generate contrast variations, apply segmentation, and color bucket the pixels."""
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image could not be loaded. Check the file path.")

    image = cv2.resize(image, (256, 256))

    original = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    contrast_images = enhance_contrast(image)
    segmented_images = [segment_and_highlight(img) for img in contrast_images]
    bucketed_images = [apply_color_buckets(img) for img in segmented_images]

    return {
        "original": original,
        "contrast_images": contrast_images,
        "segmented_images": segmented_images,
        "bucketed_images": bucketed_images
    }


def get_contrasted_color_images(image_path: str):
    """Wrapper function to process an image and return enhanced contrast images."""
    return process_images(image_path)


