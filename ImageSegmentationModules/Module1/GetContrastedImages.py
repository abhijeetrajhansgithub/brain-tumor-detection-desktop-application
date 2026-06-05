import PyQt5
import cv2
import numpy as np
from PyQt5.QtGui import QPixmap, QImage


def get_contrasting_images(image_path: str):
    print("------------------- IMAGE SEGMENTATION -------------------")
    """
    :param image_path: Path to the input image
    :return: A dictionary containing the original, segmented, highlighted, and contrast-enhanced images.
    """

    def enhance_contrast(image, levels=12):
        """Generate contrast-enhanced versions of an image at different levels using CLAHE."""
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        contrast_images = []
        for i in range(1, levels + 1):
            clip_limit = i * 1.5  # Increasing contrast intensity
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
            l_enhanced = clahe.apply(l)
            enhanced_lab = cv2.merge([l_enhanced, a, b])
            enhanced_image = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
            contrast_images.append(enhanced_image)

        return contrast_images

    def segment_and_highlight(image):
        """Apply K-Means clustering and highlight segmented regions."""
        blurred = cv2.GaussianBlur(image, (5, 5), 0)

        # Apply K-Means Clustering
        pixel_values = blurred.reshape((-1, 3))
        pixel_values = np.float32(pixel_values)
        k = 3  # Number of clusters
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)
        segmented_image = centers[labels.flatten()].reshape(image.shape)

        # Convert to Grayscale and Threshold
        gray = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2GRAY)
        _, binary_mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Apply Morphological Operations
        kernel = np.ones((5, 5), np.uint8)
        mask_cleaned = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)
        mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_OPEN, kernel)

        # Find Contours
        contours, _ = cv2.findContours(mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw Contours with Different Colors
        output = image.copy()
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
        for i, contour in enumerate(contours):
            color = colors[i % len(colors)]
            cv2.drawContours(output, [contour], -1, color, 2)

        return segmented_image, output

    def process_images(image_path_):
        """Process the image, generate contrast variations, and return them."""
        # Load and Resize Image
        image = cv2.imread(image_path_)
        image = cv2.resize(image, (256, 256))  # Resize for uniformity
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB

        # Generate 12 Contrast-Enhanced Images
        contrast_images = enhance_contrast(image)

        # Process Original Image for Segmentation
        segmented, highlighted = segment_and_highlight(image)

        # Store all images in a dictionary
        processed_images = {
            "original": image_rgb,
            "segmented": segmented,
            "highlighted": highlighted,
            "contrast_images": contrast_images  # List of 12 contrast-enhanced images
        }

        return processed_images

    return process_images(image_path_=image_path)


def cv2_get_contrasting_images(qpixmap_image: PyQt5.QtGui.QPixmap):
    print("------------------- IMAGE SEGMENTATION -------------------")

    def qpixmap_to_cv2(qpixmap):
        """Convert QPixmap to OpenCV (BGR) format."""
        qimage = qpixmap.toImage()
        qimage = qimage.convertToFormat(QImage.Format_RGB888)
        width, height = qimage.width(), qimage.height()
        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())
        arr = np.array(ptr).reshape((height, width, 3))
        return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)  # Convert to OpenCV BGR

    def enhance_contrast(image, levels=12):
        """Generate contrast-enhanced versions of an image at different levels using CLAHE."""
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        contrast_images = []
        for i in range(1, levels + 1):
            clip_limit = i * 1.5  # Increasing contrast intensity
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
            l_enhanced = clahe.apply(l)
            enhanced_lab = cv2.merge([l_enhanced, a, b])
            enhanced_image = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
            contrast_images.append(enhanced_image)

        return contrast_images

    def segment_and_highlight(image):
        """Apply K-Means clustering and highlight segmented regions."""
        blurred = cv2.GaussianBlur(image, (5, 5), 0)

        # Apply K-Means Clustering
        pixel_values = blurred.reshape((-1, 3))
        pixel_values = np.float32(pixel_values)
        k = 3  # Number of clusters
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)
        segmented_image = centers[labels.flatten()].reshape(image.shape)

        # Convert to Grayscale and Threshold
        gray = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2GRAY)
        _, binary_mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Apply Morphological Operations
        kernel = np.ones((5, 5), np.uint8)
        mask_cleaned = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)
        mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_OPEN, kernel)

        # Find Contours
        contours, _ = cv2.findContours(mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw Contours with Different Colors
        output = image.copy()
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
        for i, contour in enumerate(contours):
            color = colors[i % len(colors)]
            cv2.drawContours(output, [contour], -1, color, 2)

        return segmented_image, output

    def process_images(cv2_image_):
        """Process the image, generate contrast variations, and return them."""
        image = cv2.resize(cv2_image_, (256, 256))  # Resize for uniformity
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB

        # Generate 12 Contrast-Enhanced Images
        contrast_images = enhance_contrast(image)

        # Process Original Image for Segmentation
        segmented, highlighted = segment_and_highlight(image)

        # Store all images in a dictionary
        processed_images = {
            "original": image_rgb,
            "segmented": segmented,
            "highlighted": highlighted,
            "contrast_images": contrast_images  # List of 12 contrast-enhanced images
        }

        return processed_images

    # Convert QPixmap to OpenCV format
    cv2_image = qpixmap_to_cv2(qpixmap_image)

    return process_images(cv2_image)
