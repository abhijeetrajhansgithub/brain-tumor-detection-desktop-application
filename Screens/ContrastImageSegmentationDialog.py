import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QPalette
from PyQt5.QtWidgets import (
    QDialog, QPushButton, QVBoxLayout, QRadioButton, QFileDialog,
    QLabel, QGridLayout, QScrollArea, QWidget, QLineEdit, QMessageBox, QApplication
)


class HoverLabel(QLabel):
    """ Custom QLabel to handle hover events for image enlargement """

    def __init__(self, pixmap, size=600, parent=None):
        super().__init__(parent)
        self.original_pixmap = pixmap
        self.size = size  # Base size for square images
        self.setFixedSize(self.size, self.size)
        self.setPixmap(self.original_pixmap.scaled(self.size, self.size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setScaledContents(True)

    def enterEvent(self, event):
        """ Enlarge image by 150% on hover """
        enlarged_size = int(self.size * 1.5)
        self.setFixedSize(enlarged_size, enlarged_size)
        enlarged_pixmap = self.original_pixmap.scaled(enlarged_size, enlarged_size, Qt.KeepAspectRatio,
                                                      Qt.SmoothTransformation)
        self.setPixmap(enlarged_pixmap)

    def leaveEvent(self, event):
        """ Restore image size when not hovered """
        self.setFixedSize(self.size, self.size)
        self.setPixmap(self.original_pixmap.scaled(self.size, self.size, Qt.KeepAspectRatio, Qt.SmoothTransformation))


class ContrastImageSegmentationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.search_button_GCI = None
        self.search_by_phone_GCI = None
        self.search_by_id_GCI = None
        self.search_by_email_GCI = None
        self.upload_image_button = None
        self.search_patient_button = None
        self.search_input = None
        self.setWindowTitle("Functional Contrast Segmentation")
        self.setGeometry(100, 100, 400, 200)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # First Option: Search Patient
        self.search_patient_button = QPushButton("Search Patient for Image Segmentation")
        self.search_patient_button.setStyleSheet(self.fGet_Button_Style())
        self.search_patient_button.clicked.connect(self.show_search_options)
        layout.addWidget(self.search_patient_button)

        # Second Option: Upload Image Directly
        self.upload_image_button = QPushButton("Upload Image Directly")
        self.upload_image_button.setStyleSheet(self.fGet_Button_Style())
        self.upload_image_button.clicked.connect(self.upload_and_process_image)
        layout.addWidget(self.upload_image_button)

        self.setLayout(layout)

    def show_search_options(self):
        """ Displays search options and a search button """
        search_dialog = QDialog(self)
        search_dialog.setWindowTitle("Choose Search Criteria")
        search_dialog.setFixedSize(400, 300)
        search_dialog.setWindowTitle("Search Patient")
        layout = QVBoxLayout()

        # Search Input Styling
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search value...")

        self.search_by_email_GCI = QRadioButton("Email")
        self.search_by_id_GCI = QRadioButton("Patient ID")
        self.search_by_phone_GCI = QRadioButton("Phone")
        self.search_by_email_GCI.setChecked(True)

        layout.addWidget(self.search_input)

        layout.addWidget(self.search_by_email_GCI)
        layout.addWidget(self.search_by_id_GCI)
        layout.addWidget(self.search_by_phone_GCI)

        self.search_button_GCI = QPushButton("Search")
        self.search_button_GCI.setStyleSheet(self.fGet_Button_Style())
        self.search_button_GCI.clicked.connect(self.fPerform_Search_for_Segmentation)
        layout.addWidget(self.search_button_GCI)

        search_dialog.setLayout(layout)
        search_dialog.exec_()

    def fPerform_Search_for_Segmentation(self):
        search_value = self.search_input.text().strip()

        # Ensure input is not empty
        if not search_value:
            QMessageBox.warning(self, "Input Error", "Please enter a search value.")
            return

        # Determine Search Criteria
        if self.search_by_email_GCI.isChecked():
            criteria = "email"
        elif self.search_by_id_GCI.isChecked():
            criteria = "patient_id"
        elif self.search_by_phone_GCI.isChecked():
            criteria = "phone"
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a search criteria.")
            return

        # Fetch Patient Record (Replace with actual database/query logic)
        patient_record = self.fGet_Patient_Record(search_value, criteria)

        if patient_record:
            print("Patient record found!")
            image_ = patient_record["image"]

            from ImageSegmentationModules.Module1.GetContrastedImages import cv2_get_contrasting_images

            print(type(image_))
            images = cv2_get_contrasting_images(qpixmap_image=image_)
            self.display_images(images)

        else:
            QMessageBox.information(self, "No Record Found", "No matching patient record was found.")

    @staticmethod
    def fGet_Patient_Record(search_value, criteria):
        from Main.utils import get_current_system_path, change_path_to_db
        from API.DatabaseAPI.client_database_connection import get_patient_details, get_tumor_image

        """Fetch patient details and tumor image from the database."""
        # Get system and database paths
        PATH_ = get_current_system_path()
        dbPATH_ = change_path_to_db(PATH_)

        print("------------- (new) PATH:", PATH_)
        print("------------- (new) dbPATH:", dbPATH_)

        patient_data = get_patient_details(search_value=search_value, criteria=criteria, PATH_=dbPATH_)

        if patient_data is not None:
            patient_record = {
                "patient_id": patient_data['patient_id'],
                "first_name": patient_data['first_name'].title(),
                "last_name": patient_data['last_name'].title(),
                "date_of_birth": patient_data['date_of_birth'],
                "gender": patient_data['gender'],
                "phone_number": patient_data['phone_number'],
                "email": patient_data['email'],
                "image": None  # Placeholder for the image
            }

            image_vector = get_tumor_image(patient_id=patient_record["patient_id"], PATH_=dbPATH_)

            if image_vector:
                try:
                    import cv2

                    # Convert BLOB to NumPy array
                    image_array = np.frombuffer(image_vector, np.uint8)
                    if image_array.size == 0:
                        raise ValueError("Empty image data received.")

                    # Debug: Print first few bytes to check the integrity of the image data
                    print("DEBUG: First 20 bytes of image data:", image_array[:20])

                    # Decode image using OpenCV
                    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                    if image is None:
                        raise ValueError(
                            "Failed to decode image. The image data may be corrupted or incorrectly stored.")

                    # Convert OpenCV image (BGR) to RGB
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                    # Convert to QImage (requires bytesPerLine for correct alignment)
                    height, width, channel = image.shape
                    bytes_per_line = channel * width
                    qImage = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)

                    # Convert to QPixmap
                    patient_record["image"] = QPixmap.fromImage(qImage)

                except Exception as e:
                    print("Error decoding image:", e)
                    patient_record["image"] = "No Image Found"

            else:
                print("DEBUG: No image found for this patient.")
                patient_record["image"] = "No Image Found"

            print(patient_record)

            return patient_record  # Return structured dictionary

        else:
            print("No patient record found.")
            return None

    def upload_and_process_image(self):
        from ImageSegmentationModules.Module1.GetContrastedImages import get_contrasting_images
        """ Opens a file dialog, processes the image, and displays results. """
        file_path, _ = QFileDialog.getOpenFileName(self, "Select an Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            images = get_contrasting_images(image_path=file_path)
            self.display_images(images)

    def display_images(self, images):
        """ Displays the processed images in a 3-column grid layout with hover effects """
        display_dialog = QDialog(self)
        display_dialog.setWindowTitle("Processed Images")
        display_dialog.setGeometry(100, 100, 1200, 900)

        scroll_area = QScrollArea(display_dialog)
        scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()
        grid_layout = QGridLayout(scroll_widget)

        def convert_cv_to_qpixmap(cv_image):
            """ Converts an OpenCV image to QPixmap for PyQt display, making it square """
            height, width, _ = cv_image.shape
            size = max(height, width)  # Ensuring square aspect ratio
            square_image = np.zeros((size, size, 3), dtype=np.uint8)
            x_offset = (size - width) // 2
            y_offset = (size - height) // 2
            square_image[y_offset:y_offset + height, x_offset:x_offset + width] = cv_image
            bytes_per_line = 3 * size
            q_image = QImage(square_image.data, size, size, bytes_per_line, QImage.Format_RGB888)
            return QPixmap.fromImage(q_image)

        grid_layout.setSpacing(20)
        img_size = 300

        image_types = ["original", "segmented", "highlighted"]
        for i, img_type in enumerate(image_types):
            img_label = QLabel(img_type.capitalize())
            img_pixmap = HoverLabel(convert_cv_to_qpixmap(images[img_type]), img_size)
            grid_layout.addWidget(img_label, 0, i)
            grid_layout.addWidget(img_pixmap, 1, i)

        for i, img in enumerate(images["contrast_images"]):
            img_label = QLabel(f"Contrast {i + 1}")
            img_pixmap = HoverLabel(convert_cv_to_qpixmap(img), img_size)
            row, col = divmod(i, 3)
            grid_layout.addWidget(img_label, row * 2 + 2, col)
            grid_layout.addWidget(img_pixmap, row * 2 + 3, col)

        scroll_area.setWidget(scroll_widget)
        main_layout = QVBoxLayout(display_dialog)
        main_layout.addWidget(scroll_area)
        display_dialog.setLayout(main_layout)

        display_dialog.exec_()

    def fGet_Button_Style(self):
        palette = QApplication.instance().palette()
        bg_color = palette.color(QPalette.Window).name()

        if bg_color in ["#2d2d2d", "#3b3b3b"]:  # Dark mode
            return (
                "color: white; background-color: #43A047; border-radius: 8px; font-size: 15px; "
                "padding: 12px 32px; border: 2px solid #388E3C; transition: background-color 0.3s ease-in-out;"
                "hover { background-color: #388E3C; }"
            )
        else:  # Light mode
            return (
                "color: black; background-color: #64B5F6; border-radius: 8px; font-size: 15px; "
                "padding: 12px 32px; border: 2px solid #42A5F5; transition: background-color 0.3s ease-in-out;"
                "hover { background-color: #42A5F5; }"
            )
