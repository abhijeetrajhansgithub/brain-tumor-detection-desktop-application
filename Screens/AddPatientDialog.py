import sys
import sqlite3
import numpy as np
from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,
    QComboBox, QFileDialog, QTextEdit, QMessageBox, QDateEdit, QApplication
)
from PyQt5.QtGui import QPixmap, QPalette
from PyQt5.QtCore import Qt
import cv2  # OpenCV for image processing


class AddPatientDialog(QDialog):
    def __init__(self, parent, db_path, doctor_id):
        super().__init__(parent)
        self.db_path = db_path
        self.image_path = None
        self.image_array = None
        self.doctor_id = doctor_id

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add New Patient")
        self.setMinimumSize(800, 500)

        layout = QVBoxLayout()
        form_layout = QGridLayout()

        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDisplayFormat("yyyy-MM-dd")
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female", "Other"])
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QTextEdit()
        self.medical_history_input = QTextEdit()

        form_layout.addWidget(QLabel("First Name:"), 0, 0)
        form_layout.addWidget(self.first_name_input, 0, 1)
        form_layout.addWidget(QLabel("Last Name:"), 1, 0)
        form_layout.addWidget(self.last_name_input, 1, 1)
        form_layout.addWidget(QLabel("Date of Birth:"), 2, 0)
        form_layout.addWidget(self.dob_input, 2, 1)
        form_layout.addWidget(QLabel("Gender:"), 3, 0)
        form_layout.addWidget(self.gender_input, 3, 1)
        form_layout.addWidget(QLabel("Phone Number:"), 4, 0)
        form_layout.addWidget(self.phone_input, 4, 1)
        form_layout.addWidget(QLabel("Email:"), 5, 0)
        form_layout.addWidget(self.email_input, 5, 1)
        form_layout.addWidget(QLabel("Address:"), 6, 0)
        form_layout.addWidget(self.address_input, 6, 1)
        form_layout.addWidget(QLabel("Medical History:"), 7, 0)
        form_layout.addWidget(self.medical_history_input, 7, 1)

        self.image_label = QLabel("No Image Uploaded")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black;")
        self.image_label.setFixedSize(200, 200)

        image_layout = QVBoxLayout()
        image_layout.addWidget(QLabel("Patient Image:"))
        image_layout.addWidget(self.image_label)

        self.upload_button = QPushButton("Upload Image")
        self.add_patient_button = QPushButton("Add Patient")

        self.upload_button.clicked.connect(self.upload_image)
        self.add_patient_button.clicked.connect(self.add_patient_to_db)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.upload_button)
        button_layout.addWidget(self.add_patient_button)

        layout.addLayout(form_layout)
        layout.addLayout(image_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Implement light theme
        self.implement_themes()

    def upload_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg)",
                                                   options=options)

        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
            self.image_array = self.image_to_blob(file_path)

    def image_to_blob(self, image_path):
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Error loading image")
        success, encoded_image = cv2.imencode(".jpg", image)
        if not success:
            raise ValueError("Failed to encode image")
        return encoded_image.tobytes()

    def add_patient_to_db(self):
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        date_of_birth = self.dob_input.date().toString("yyyy-MM-dd").strip()
        gender = self.gender_input.currentText().strip()
        phone_number = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.toPlainText().strip() or None
        medical_history = self.medical_history_input.toPlainText().strip() or None

        if not first_name or not last_name or not date_of_birth or not phone_number or not self.image_path or not self.image_array:
            QMessageBox.warning(self, "Error", "First Name, Last Name, DOB, Phone, and Image are required!")
            return

        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO patients (first_name, last_name, date_of_birth, gender, phone_number, email, address, medical_history, doctor_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (first_name, last_name, date_of_birth, gender, phone_number, email, address, medical_history,
                  int(self.doctor_id[0])))

            patient_id = cursor.lastrowid

            if self.image_array:
                cursor.execute("""
                    INSERT INTO patient_image_vector (patient_id, image_vector)
                    VALUES (?, ?)
                """, (patient_id, self.image_array))

            connection.commit()
            QMessageBox.information(self, "Success", "Patient added successfully!")
            self.accept()
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def implement_themes(self):
        palette = QApplication.instance().palette()
        bg_color = palette.color(QPalette.Window).name()

        if bg_color in ["#2d2d2d", "#3b3b3b"]:  # Dark mode
            input_style = (
                "color: white; background-color: #2b2b2b; border: 2px solid #5a5a5a; "
                "border-radius: 8px; padding: 8px; font-size: 14px; transition: all 0.3s ease-in-out;"
                "hover { border-color: #8d8d8d; }"
            )
            button_style = (
                "color: white; background-color: #43A047; border-radius: 8px; font-size: 15px; "
                "padding: 12px 32px; border: 2px solid #388E3C; transition: background-color 0.3s ease-in-out;"
                "hover { background-color: #388E3C; }"
            )
        else:  # Light mode
            input_style = (
                "color: black; background-color: #FAFAFA; border: 2px solid #CCCCCC; "
                "border-radius: 8px; padding: 8px; font-size: 14px; transition: all 0.3s ease-in-out;"
                "hover { border-color: #999999; }"
            )
            button_style = (
                "color: black; background-color: #64B5F6; border-radius: 8px; font-size: 15px; "
                "padding: 12px 32px; border: 2px solid #42A5F5; transition: background-color 0.3s ease-in-out;"
                "hover { background-color: #42A5F5; }"
            )

        for widget in [
            self.first_name_input, self.last_name_input, self.dob_input, self.gender_input,
            self.phone_input, self.email_input, self.address_input, self.medical_history_input
        ]:
            widget.setStyleSheet(input_style)

        self.upload_button.setStyleSheet(button_style)
        self.add_patient_button.setStyleSheet(button_style)

