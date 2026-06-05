import os
import tempfile

import numpy as np
from PyQt5 import sip
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame, QApplication, QFileDialog,
    QRadioButton, QLineEdit, QMessageBox, QDialog, QAction, QTextEdit, QScrollArea, QButtonGroup
)
from fpdf import FPDF
from plyer import notification


class MainPage_11(QMainWindow):
    def __init__(self, username):
        super().__init__()

        self.contrast_image_segmentation_dialog = None
        self.notification_settings = None
        self.output_label = None
        self.image_view = None
        self.classify_button = None
        self.add_patient_button = None
        self.search_button = None
        self.add_patient_dialog = None
        self.add_patient_window = None
        self.DOCTOR_USERNAME = username

        self.search_by_phone = None
        self.search_by_id = None
        self.search_by_email = None
        self.search_input = None
        self.upload_image_button = None
        self.FINAL_FILE_PATH = None
        self.IMAGE_PATH = None
        self.setWindowTitle("Main Page v4.2.1")
        self.setGeometry(100, 100, 800, 600)
        self.dark_mode = True  # Default to dark mode
        self.fSet_Dark_Mode()  # Apply dark mode

        self.username = username

        # Main layout
        self.central_widget = QWidget()
        self.main_layout = QHBoxLayout(self.central_widget)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(60)  # Initially collapsed
        self.sidebar_layout = QVBoxLayout(self.sidebar)

        self.fInit_Menubar()

        # Home button
        self.home_button = QPushButton("🏠")
        self.home_button.setStyleSheet("""
            text-align: left;
            min-width: 60px;
            max-width: 300px;
            border: none;
            padding: 5px;
        """)
        self.home_button.clicked.connect(self.fShow_Home_Frame)  # Connect to frame function
        self.sidebar_layout.addWidget(self.home_button)

        # Upload button
        self.upload_button = QPushButton("📤")
        self.upload_button.setStyleSheet("""
            text-align: left;
            min-width: 60px;
            max-width: 300px;
            border: none;
            padding: 5px;
        """)
        self.upload_button.clicked.connect(self.fShow_Upload_Frame)  # Connect to frame function
        self.sidebar_layout.addWidget(self.upload_button)

        # diagnose button
        self.diagnose_button = QPushButton("🩺")
        self.diagnose_button.setStyleSheet("""
            text-align: left;
            min-width: 60px;
            max-width: 300px;
            border: none;
            padding: 5px;
        """)
        self.diagnose_button.clicked.connect(self.fShow_Diagnose_Frame)  # Connect to frame function
        self.sidebar_layout.addWidget(self.diagnose_button)

        # Theme button
        # Theme changer button
        self.theme_changer_main_wn = QPushButton("Change to Light Theme" if self.dark_mode else "Change to Dark Theme")
        self.theme_changer_main_wn.clicked.connect(self.fToggle_Theme_Main_WN)
        self.theme_changer_main_wn.setStyleSheet(self.fGet_Theme_Button_Style())
        self.sidebar_layout.addWidget(self.theme_changer_main_wn)

        # Expand/Collapse button
        self.expand_button = QPushButton("➡️")
        self.expand_button.setStyleSheet(self.fGet_Expand_Button_Style())

        self.document_button = QPushButton("📄")
        self.document_button.setStyleSheet("""
            text-align: left;
            min-width: 60px;
            max-width: 300px;
            border: none;
            padding: 5px;
        """)
        # Create a container layout for the buttons
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.document_button)
        button_layout.addWidget(self.expand_button)
        button_layout.setAlignment(Qt.AlignBottom)

        # Connect the document button to its function
        self.document_button.clicked.connect(self.fShow_Document_WN)  # Connect to frame function

        # Add the button layout to the sidebar
        self.sidebar_layout.addStretch()
        self.sidebar_layout.addLayout(button_layout)

        self.expand_button.clicked.connect(self.fToggle_Sidebar)

        # Content area
        self.content_area = QFrame()
        self.content_area.setStyleSheet("background-color: gray;")
        self.content_layout = QVBoxLayout(self.content_area)

        # Initialize with the home frame
        self.fShow_Home_Frame()

        # Add sidebar and content area to the main layout
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content_area)

        self.fImplement_Themes()

        # Set central widget
        self.setCentralWidget(self.central_widget)
        self.fToggle_Theme_Main_WN()

    def fInit_Menubar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.fFile_Open_Action)
        file_menu.addAction(open_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        ############################################################################
        ############################################################################
        ############################################################################

        settings_menu = menubar.addMenu("Preferences")
        # Create a Notification submenu
        notification_menu = settings_menu.addMenu("Notification")

        # Add an action to enable/disable notifications
        self.notification_settings = QAction("Enable Notifications", self, checkable=True)
        self.notification_settings.setChecked(True)  # Set default state as enabled
        self.notification_settings.triggered.connect(self.fToggle_Notifications)
        notification_menu.addAction(self.notification_settings)

        ############################################################################
        ############################################################################
        ############################################################################

        # Image Segmentation
        segmentation_menu = menubar.addMenu("Image Segmentation")

        contrast_segmentation_action = QAction("Contrast Segmentation", self)
        contrast_segmentation_action.triggered.connect(self.fContrast_Segmentation)

        segmentation_menu.addAction(contrast_segmentation_action)

        ############################################################################
        ############################################################################
        ############################################################################

        color_segmentation_action = QAction("Color Segmentation", self)
        color_segmentation_action.triggered.connect(self.fColor_Segmentation)

        segmentation_menu.addAction(color_segmentation_action)

        ############################################################################
        ############################################################################
        ############################################################################

        view_diagnosis = menubar.addMenu("View Diagnosis")

        view_diagnosis_action = QAction("View Diagnosis", self)
        view_diagnosis_action.triggered.connect(self.fShow_Patient_Diagnosis)

        view_diagnosis.addAction(view_diagnosis_action)

        ############################################################################
        ############################################################################
        ############################################################################

    from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QRadioButton, QPushButton, QButtonGroup

    def fShow_Patient_Diagnosis(self):
        print("Showing Diagnosis...")

        # Create a dialog window
        self.dialog_for_diagnosis_search = QDialog(self)
        self.dialog_for_diagnosis_search.setWindowTitle("Search Patient Diagnosis")

        # Create a vertical layout
        layout_for_diagnosis_search = QVBoxLayout()

        # Create input field
        self.input_field_for_diagnosis_search = QLineEdit()
        self.input_field_for_diagnosis_search.setPlaceholderText("Enter search value...")
        layout_for_diagnosis_search.addWidget(self.input_field_for_diagnosis_search)

        # Create radio button group
        self.radio_group_for_diagnosis_search = QButtonGroup(self)


        self.radio_email_for_diagnosis_search = QRadioButton("Email")
        self.radio_email_for_diagnosis_search.setChecked(True)
        self.radio_patient_id_for_diagnosis_search = QRadioButton("Patient ID")
        self.radio_phone_for_diagnosis_search = QRadioButton("Phone")

        self.radio_group_for_diagnosis_search.addButton(self.radio_patient_id_for_diagnosis_search)
        self.radio_group_for_diagnosis_search.addButton(self.radio_email_for_diagnosis_search)
        self.radio_group_for_diagnosis_search.addButton(self.radio_phone_for_diagnosis_search)


        layout_for_diagnosis_search.addWidget(self.radio_email_for_diagnosis_search)
        layout_for_diagnosis_search.addWidget(self.radio_patient_id_for_diagnosis_search)
        layout_for_diagnosis_search.addWidget(self.radio_phone_for_diagnosis_search)

        # Create search button
        self.search_button_for_diagnosis_search = QPushButton("Search")
        self.search_button_for_diagnosis_search.clicked.connect(self.fSearch_Patient_Diagnosis)
        layout_for_diagnosis_search.addWidget(self.search_button_for_diagnosis_search)

        # Set layout and display dialog
        self.dialog_for_diagnosis_search.setLayout(layout_for_diagnosis_search)
        self.dialog_for_diagnosis_search.exec_()

    def fSearch_Patient_Diagnosis(self):
        """Function to handle search logic."""
        print("Search triggered...")

        # Get the input value
        search_value_for_diagnosis_search = self.input_field_for_diagnosis_search.text().strip()

        # Identify which radio button is checked
        if self.radio_patient_id_for_diagnosis_search.isChecked():
            checked_criteria_for_diagnosis_search = "patient_id"
        elif self.radio_email_for_diagnosis_search.isChecked():
            checked_criteria_for_diagnosis_search = "email"
        elif self.radio_phone_for_diagnosis_search.isChecked():
            checked_criteria_for_diagnosis_search = "phone"
        else:
            QMessageBox.warning(self, "Error", "Please select a search criteria (Patient ID, Email, or Phone).")
            return

        # Ensure input is provided
        if not search_value_for_diagnosis_search:
            QMessageBox.warning(self, "Error", f"Please enter a valid {checked_criteria_for_diagnosis_search}.")
            return

        print(f"Searching by {checked_criteria_for_diagnosis_search}: {search_value_for_diagnosis_search}")

        # Call function to fetch patient diagnosis details
        from API.DatabaseAPI.client_database_connection import get_patient_details, get_tumor_diagnosis_details
        from Main.utils import get_current_system_path, change_path_to_db

        PATH_ = get_current_system_path()
        dbPATH_ = change_path_to_db(PATH_)

        print("------------- PATH:", PATH_)
        print("------------- dbPATH:", dbPATH_)

        patient_data = get_patient_details(search_value=search_value_for_diagnosis_search, criteria=checked_criteria_for_diagnosis_search, PATH_=dbPATH_)
        print("-->> PATIENT DATA:", patient_data)

        patient_id = patient_data["patient_id"]
        diagnosis_data = get_tumor_diagnosis_details(patient_id=patient_id, PATH_=dbPATH_)

        self.fExtract_Diagnosis_and_Patient_Details(diagnosis_data=diagnosis_data)

    def fColor_Segmentation(self):
        from Screens.ContrastedColorSegmentationDialog import ContrastedColorImageSegmentationDialog

        self.contrasted_color_segmentation_dialog = ContrastedColorImageSegmentationDialog()
        self.contrasted_color_segmentation_dialog.exec_()
        pass


    def fContrast_Segmentation(self):
        from Screens.ContrastImageSegmentationDialog import ContrastImageSegmentationDialog

        self.contrast_image_segmentation_dialog = ContrastImageSegmentationDialog()
        self.contrast_image_segmentation_dialog.exec_()
        pass

    def fFile_Open_Action(self):
        self.fClear_Content_Area()
        self.fShow_Upload_Frame()
        self.fUpload_Image_To_Check_Classification()
        pass

    @staticmethod
    def fToggle_Notifications(state):
        if state:
            print("Notifications enabled")
        else:
            print("Notifications disabled")
        pass

    def fSet_Theme(self):
        if self.dark_mode:
            self.fSet_Dark_Mode()
        else:
            QApplication.instance().setPalette(QApplication.instance().style().standardPalette())

    def fToggle_Theme_Main_WN(self):
        self.dark_mode = not self.dark_mode
        self.fSet_Theme()
        if self.sidebar.width() == 60:
            self.theme_changer_main_wn.setText("🌞" if self.dark_mode else "🌚")
        else:
            self.theme_changer_main_wn.setText(
                "🐙 Change to Light Theme" if self.dark_mode else "🐙 Change to Dark Theme")
        self.fImplement_Themes()

    def fImplement_Themes(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QMessageBox {
                    background-color: #333; /* Dark background */
                    color: #EEE; /* Light text */
                }
                QMenuBar { 
                    background-color: #333;  /* Dark background */
                    color: #EEE;  /* Light text */
                }

                QMenuBar::item { 
                    background-color: transparent; 
                    padding: 5px 10px;
                }

                QMenuBar::item:selected { 
                    background-color: #555;  /* Slightly lighter hover effect */
                }

                QMenu {
                    background-color: #222; /* Darker dropdown menu */
                    color: #EEE;
                    border: 1px solid #444;
                }

                QMenu::item { 
                    padding: 5px 20px;
                    background-color: transparent; 
                }

                QMenu::item:selected { 
                    background-color: #444; /* Darker highlight when hovering */
                }

                QMenu::separator {
                    background: #666; /* Subtle separator line */
                    height: 1px;
                }
            """)
        else:
            self.setStyleSheet("""
                QMessageBox {
                    background-color: #FFFFFF; /* White background */
                    color: #333; /* Dark text */
                }
                QMenuBar { 
                    background-color: #F8F9FA; /* Light background */
                    color: #333;  /* Dark text */
                }

                QMenuBar::item { 
                    background-color: transparent; 
                    padding: 5px 10px;
                }

                QMenuBar::item:selected { 
                    background-color: #D6D8DB; /* Light hover */
                }

                QMenu {
                    background-color: #FFFFFF; /* White dropdown menu */
                    color: #333;
                    border: 1px solid #CCC;
                }

                QMenu::item { 
                    padding: 5px 20px;
                    background-color: transparent; 
                }

                QMenu::item:selected { 
                    background-color: #E9ECEF; /* Soft highlight */
                }

                QMenu::separator {
                    background: #CCC; /* Light gray separator */
                    height: 1px;
                }
            """)

        if type(self.home_button) == QPushButton:
            self.home_button.setStyleSheet(self.fGet_Button_Style())
        if type(self.upload_button) == QPushButton:
            self.upload_button.setStyleSheet(self.fGet_Button_Style())
        if type(self.diagnose_button) == QPushButton:
            self.diagnose_button.setStyleSheet(self.fGet_Button_Style())
        if type(self.document_button) == QPushButton:
            self.document_button.setStyleSheet(self.fGet_Button_Style())
        if type(self.theme_changer_main_wn) == QPushButton:
            self.theme_changer_main_wn.setStyleSheet(self.fGet_Theme_Button_Style())
        if type(self.expand_button) == QPushButton:
            self.expand_button.setStyleSheet(self.fGet_Expand_Button_Style())

        if hasattr(self, "add_patient_button") and self.add_patient_button is not None:
            if isinstance(self.add_patient_button, QPushButton) and not sip.isdeleted(self.add_patient_button):
                self.add_patient_button.setStyleSheet(self.fGet_Button_Style())

        if hasattr(self, "search_button") and self.search_button is not None:
            if isinstance(self.search_button, QPushButton) and not sip.isdeleted(self.search_button):
                self.search_button.setStyleSheet(self.fGet_Button_Style())

        if hasattr(self, "classify_button") and self.classify_button is not None:
            if isinstance(self.classify_button, QPushButton) and not sip.isdeleted(self.classify_button):
                self.classify_button.setStyleSheet(self.fGet_Button_Style())

        if hasattr(self, "upload_image_button") and self.upload_image_button is not None:
            if isinstance(self.upload_image_button, QPushButton) and not sip.isdeleted(self.upload_image_button):
                self.upload_image_button.setStyleSheet(self.fGet_Button_Style())

    def fToggle_Sidebar(self):
        """Toggle the sidebar's width between collapsed and expanded."""
        if self.sidebar.width() == 60:
            self.sidebar.setFixedWidth(int(self.width() / 4))  # Expand
            if type(self.expand_button) == QPushButton:
                self.expand_button.setStyleSheet(self.fGet_Expand_Button_Style())
                self.expand_button.setText("⬅️")

            if type(self.home_button) == QPushButton:
                self.home_button.setStyleSheet(self.fGet_Button_Style())
                self.home_button.setText("🏠 Home")

            if type(self.upload_button) == QPushButton:
                self.upload_button.setStyleSheet(self.fGet_Button_Style())
                self.upload_button.setText("📤 Upload")

            if type(self.diagnose_button) == QPushButton:
                self.diagnose_button.setStyleSheet(self.fGet_Button_Style())
                self.diagnose_button.setText("🩺 Diagnose")

            if type(self.document_button) == QPushButton:
                self.document_button.setStyleSheet(self.fGet_Button_Style())
                self.document_button.setText("📄 Document")

            if type(self.theme_changer_main_wn) == QPushButton:
                self.theme_changer_main_wn.setStyleSheet(self.fGet_Theme_Button_Style())
                self.theme_changer_main_wn.setText(
                    "🐙 Change to Light Theme" if self.dark_mode else "🐙 Change to Dark Theme")
        else:
            self.sidebar.setFixedWidth(60)  # Collapse
            if type(self.expand_button) == QPushButton:
                self.expand_button.setStyleSheet(self.fGet_Expand_Button_Style())
                self.expand_button.setText("➡️")

            if type(self.home_button) == QPushButton:
                self.home_button.setStyleSheet(self.fGet_Button_Style())
                self.home_button.setText("🏠")

            if type(self.upload_button) == QPushButton:
                self.upload_button.setStyleSheet(self.fGet_Button_Style())
                self.upload_button.setText("📤")

            if type(self.diagnose_button) == QPushButton:
                self.diagnose_button.setStyleSheet(self.fGet_Button_Style())
                self.diagnose_button.setText("🩺")

            if type(self.document_button) == QPushButton:
                self.document_button.setStyleSheet(self.fGet_Button_Style())
                self.document_button.setText("📄")

            if type(self.theme_changer_main_wn) == QPushButton:
                self.theme_changer_main_wn.setStyleSheet(self.fGet_Theme_Button_Style())
                self.theme_changer_main_wn.setText("🌞" if self.dark_mode else "🌚")

    def fClear_Content_Area(self):
        """Ensure all widgets from the content area are completely removed."""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()  # Ensure widget is properly deleted
            elif item.layout():
                self.fClear_Layout(item.layout())  # Recursively clear nested layouts

        # Ensure layout refresh
        self.content_area.update()
        self.content_area.repaint()

    def fClear_Layout(self, layout):
        """Recursively remove all widgets from a layout."""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.fClear_Layout(item.layout())  # Clear nested layouts

    def fShow_Document_WN(self):
        """Display the Document frame in the content area."""

        # Check if the document window is already open
        if hasattr(self, 'doc_wn') and self.doc_wn.isVisible():
            self.doc_wn.activateWindow()  # Bring the existing window to the front
            return

        # Open a new QDialog window
        self.doc_wn = QDialog(self)
        self.doc_wn.setWindowTitle("Document")
        self.doc_wn.setFixedSize(700, 400)

        # Create a QTextEdit widget to display the project details
        doc_text = QTextEdit(self.doc_wn)
        doc_text.setReadOnly(True)  # Make it read-only
        doc_text.setText("""
        Brain Tumor Classification and Segmentation – PyQT5 Application

        Developer: Abhijeet Rajhans  
        University: Manipal University Jaipur  
        Course: Computer Science & Engineering (3rd Year)  
        Version: 4.2.1

        Overview  
        This PyQT5-based application provides an interface for brain tumor classification and segmentation. It allows users to analyze medical images and determine the presence of tumors while also segmenting affected areas for better visualization.  

        Features  
        - Tumor Classification: The model predicts whether a brain MRI scan contains a tumor.  
        - Tumor Segmentation: Highlights and separates tumor regions within the scan.  
        - User-Friendly Interface: Built using PyQT5 for smooth navigation and usability.  
        - Modal Windows: The application includes pop-up windows for displaying documents and results.  

        Technical Details  
        - Framework: PyQT5 for GUI  
        - Machine Learning: Uses a deep learning model for classification and segmentation  
        - Python Version: Compatible with Python 3.x  
        - Libraries Used: TensorFlow/Keras, OpenCV, NumPy, PyQt5, and others  

        How It Works  
        1. The user uploads an MRI scan.  
        2. The model processes the image and provides classification results.  
        3. If segmentation is enabled, the system highlights the tumor region.  
        4. Results are displayed on the application interface.  

        Future Improvements  
        - Enhancing accuracy with better datasets.  
        - Adding more model interpretability features.  
        - Optimizing performance for real-time classification.  

        This project serves as a useful tool for assisting in medical diagnosis, with an emphasis on simplicity and efficiency.
        """)

        # Set up layout and add text widget
        layout = QVBoxLayout()
        layout.addWidget(doc_text)
        self.doc_wn.setLayout(layout)

        # Show the dialog
        self.doc_wn.show()

    from PyQt5.QtWidgets import (
        QLabel, QVBoxLayout, QLineEdit, QRadioButton, QHBoxLayout, QPushButton,
        QScrollArea, QWidget, QMessageBox
    )
    from PyQt5.QtGui import QPixmap

    def fShow_Diagnose_Frame(self):
        """Display the Diagnose frame in the content area."""
        self.fClear_Content_Area()

        # Make the content layout scrollable
        scroll_area_for_diagnosis = QScrollArea()
        scroll_area_for_diagnosis.setWidgetResizable(True)

        content_widget_for_diagnosis = QWidget()
        diagnosis_content_layout = QVBoxLayout(content_widget_for_diagnosis)

        # Search Bar Layout
        search_layout_for_diagnosis = QVBoxLayout()

        # Label Styling
        search_label_for_diagnosis = QLabel("Search Patient Record:")
        search_label_for_diagnosis.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")

        # Search Input Styling
        self.search_input_for_diagnosis = QLineEdit()
        self.search_input_for_diagnosis.setPlaceholderText("Enter search value...")
        self.search_input_for_diagnosis.setStyleSheet("""
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    padding: 6px;
                    font-size: 14px;
                    margin-bottom: 30px;
                """)
        self.search_input_for_diagnosis.setFocus()

        # Search Options (Modern Radio Buttons)
        self.search_by_email_for_diagnosis = QRadioButton("Email")
        self.search_by_id_for_diagnosis = QRadioButton("Patient ID")
        self.search_by_phone_for_diagnosis = QRadioButton("Phone")
        self.search_by_email_for_diagnosis.setChecked(True)  # Default selection

        # Styling for Modern Look
        radio_style_for_diagnosis = """
                    QRadioButton {
                        font-size: 14px;
                        color: #333;
                        padding: 4px;
                        font-weight: bold;
                    }
                    QRadioButton::indicator {
                        width: 18px;
                        height: 18px;
                        border-radius: 9px;
                        border: 2px solid #0078D7;
                        background: white;
                    }
                    QRadioButton::indicator:checked {
                        background: yellow;
                        border: 2px solid #005A9E;
                    }
                """

        # Apply Styles
        self.search_by_email_for_diagnosis.setStyleSheet(radio_style_for_diagnosis)
        self.search_by_id_for_diagnosis.setStyleSheet(radio_style_for_diagnosis)
        self.search_by_phone_for_diagnosis.setStyleSheet(radio_style_for_diagnosis)

        # Radio Button Layout (Horizontal)
        radio_layout_for_diagnosis = QHBoxLayout()
        radio_layout_for_diagnosis.setSpacing(15)  # Adds spacing between buttons
        radio_layout_for_diagnosis.addWidget(self.search_by_email_for_diagnosis)
        radio_layout_for_diagnosis.addWidget(self.search_by_id_for_diagnosis)
        radio_layout_for_diagnosis.addWidget(self.search_by_phone_for_diagnosis)

        # Increase the bottom margin for radio buttons
        radio_layout_for_diagnosis.setContentsMargins(0, 0, 0, 20)

        # Search Button
        self.search_button_for_diagnosis = QPushButton("Search")
        self.search_button_for_diagnosis.setStyleSheet(self.fGet_Button_Style())
        self.search_button_for_diagnosis.clicked.connect(self.fPerform_Search_For_Diagnosis)

        # Add Widgets to Search Layout
        search_layout_for_diagnosis.addWidget(search_label_for_diagnosis)
        search_layout_for_diagnosis.addWidget(self.search_input_for_diagnosis)
        search_layout_for_diagnosis.addLayout(radio_layout_for_diagnosis)
        search_layout_for_diagnosis.addWidget(self.search_button_for_diagnosis)

        # Image Layout with Placeholder
        self.image_placeholder_for_diagnosis = QLabel("No Image Available")
        self.image_placeholder_for_diagnosis.setStyleSheet("border: 2px dashed #ccc; padding: 10px;")
        self.image_placeholder_for_diagnosis.setAlignment(Qt.AlignCenter)

        # Classify Button (Initially Hidden)
        self.classify_button_for_diagnosis = QPushButton("Classify Tumor")
        self.classify_button_for_diagnosis.setStyleSheet(self.fGet_Button_Style())
        self.classify_button_for_diagnosis.clicked.connect(self.fClassify_Tumor)
        self.classify_button_for_diagnosis.setVisible(False)  # Hide by default

        self.output_label_for_diagnosis = QLabel(self)
        self.output_label_for_diagnosis.setAlignment(Qt.AlignCenter)

        self.output_label_for_diagnosis.setStyleSheet("font-weight: bold; color: black; font-size: 20px;")

        # Accept and Reject Buttons (Initially Hidden)
        self.accept_button = QPushButton("Accept")
        self.accept_button.clicked.connect(self.fAccept_Tumor)
        self.reject_button = QPushButton("Reject")
        self.reject_button.clicked.connect(self.fReject_Tumor)

        self.accept_button.setStyleSheet(self.fGet_Button_Style())
        self.reject_button.setStyleSheet(self.fGet_Button_Style())

        self.accept_button.setVisible(False)
        self.reject_button.setVisible(False)

        # Layout for Accept and Reject Buttons
        self.button_layout_for_diagnosis = QHBoxLayout()
        self.button_layout_for_diagnosis.addWidget(self.accept_button)
        self.button_layout_for_diagnosis.addWidget(self.reject_button)

        # Add Widgets to Diagnosis Content Layout
        diagnosis_content_layout.addLayout(search_layout_for_diagnosis)
        diagnosis_content_layout.addWidget(self.image_placeholder_for_diagnosis)
        diagnosis_content_layout.addWidget(self.classify_button_for_diagnosis)
        diagnosis_content_layout.addWidget(self.output_label_for_diagnosis)
        diagnosis_content_layout.addLayout(self.button_layout_for_diagnosis)

        # Set Scroll Area Content
        scroll_area_for_diagnosis.setWidget(content_widget_for_diagnosis)

        # Add Scroll Area to the Main Layout
        self.content_layout.addWidget(scroll_area_for_diagnosis)

    def fReject_Tumor(self):
        print("Rejecting Tumor")

        # ask a confirmation
        reply = QMessageBox.question(self, "Confirmation", "Are you sure you want to reject the tumor?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # notify
            notification.notify(
                title="Tumor Rejected",
                message="Tumor has been rejected."
            )
            self.fShow_Home_Frame()

    def fAccept_Tumor(self):
        from Main.utils import get_current_system_path, change_path_to_db
        from API.DatabaseAPI.client_database_connection import make_tumor_diagnosis, get_tumor_diagnosis_details
        print("Accepting Tumor")

        PATH_ = get_current_system_path()
        dbPATH_ = change_path_to_db(PATH_)

        print("------------- PATH:", PATH_)
        print("------------- dbPATH:", dbPATH_)

        print("TUMOR TYPE:", self.TUMOR_TYPE)

        # ask a confirmation
        reply = QMessageBox.question(self, "Confirmation", "Are you sure you want to accept the tumor?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # notify
            notification.notify(
                title="Tumor Accepted",
                message="Tumor has been accepted."
            )

            make_tumor_diagnosis(patient_id=self.PATIENT_ID_FOR_DIAGNOSIS, tumor_type=self.TUMOR_TYPE, PATH_=dbPATH_)

            diagnosis_data = get_tumor_diagnosis_details(patient_id=self.PATIENT_ID_FOR_DIAGNOSIS, PATH_=dbPATH_)
            print("DIAGNOSIS DATA:", diagnosis_data)

            self.fExtract_Diagnosis_and_Patient_Details(diagnosis_data)

    def fExtract_Diagnosis_and_Patient_Details(self, diagnosis_data):
        """Extracts and prints diagnosis and patient details, then displays them in a message box."""

        # Extract diagnosis and patient details
        diagnosis, patient_data = diagnosis_data

        # Extract diagnosis details
        diagnosis_id = diagnosis[0]
        tumor_type = diagnosis[1]
        created_at: str = diagnosis[2]

        print("DIAGNOSIS ID:", diagnosis_id)
        print("TUMOR TYPE:", tumor_type)
        print("CREATED AT:", created_at)

        # Extract patient details
        patient_id = patient_data['patient_id']
        first_name = patient_data['first_name']
        last_name = patient_data['last_name']
        date_of_birth = patient_data['date_of_birth']
        gender = patient_data['gender']
        phone_number = patient_data['phone_number']
        email = patient_data['email']

        print("PATIENT ID:", patient_id)

        # Display message box with patient and tumor details
        QMessageBox.information(
            self, "Patient Details",
            f"Patient ID: {patient_id}\n"
            f"Name: {first_name} {last_name}\n"
            f"Date of Birth: {date_of_birth}\n"
            f"Gender: {gender}\n"
            f"Phone: {phone_number}\n"
            f"Email: {email}\n"
            f"Tumor Type: {tumor_type}\n"
            f"Diagnosis ID: {diagnosis_id}\n"
            f"Created At: {created_at}"
        )

        self.fShow_Home_Frame()

    def fPerform_Search_For_Diagnosis(self):
        """Perform search based on selected criteria."""
        search_value_for_diagnosis = self.search_input_for_diagnosis.text().strip()

        # Ensure input is not empty
        if not search_value_for_diagnosis:
            QMessageBox.warning(self, "Input Error", "Please enter a search value.")
            return

        # Determine Search Criteria
        if self.search_by_email_for_diagnosis.isChecked():
            criteria_for_diagnosis = "email"
        elif self.search_by_id_for_diagnosis.isChecked():
            criteria_for_diagnosis = "patient_id"
        elif self.search_by_phone_for_diagnosis.isChecked():
            criteria_for_diagnosis = "phone"
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a search criteria.")
            return

        # Fetch Patient Record (Replace with actual database/query logic)
        patient_record_for_diagnosis = self.fGet_Patient_Record(search_value_for_diagnosis, criteria_for_diagnosis)

        if patient_record_for_diagnosis:
            print("DEBUG ============ PATIENT DATA ============\n", patient_record_for_diagnosis)

            patient_id = patient_record_for_diagnosis["patient_id"]
            first_name = patient_record_for_diagnosis["first_name"]
            last_name = patient_record_for_diagnosis["last_name"]
            date_of_birth = patient_record_for_diagnosis["date_of_birth"]
            gender = patient_record_for_diagnosis["gender"]
            phone_number = patient_record_for_diagnosis["phone_number"]
            email = patient_record_for_diagnosis["email"]
            image = patient_record_for_diagnosis["image"]

            print("Image: ", image)

            self.IMAGE_FOR_DIAGNOSIS = image
            self.PATIENT_ID_FOR_DIAGNOSIS = patient_id

            if isinstance(patient_record_for_diagnosis["image"], QPixmap):
                self.image_placeholder_for_diagnosis.setPixmap(
                    patient_record_for_diagnosis["image"].scaled(300, 300))
                self.classify_button_for_diagnosis.setVisible(True)  # Show classification button
            else:
                self.image_placeholder_for_diagnosis = QLabel("No Image Available")
                self.classify_button_for_diagnosis.setVisible(False)

        else:
            QMessageBox.information(self, "No Record Found", "No matching patient record was found.")

    def fClassify_Tumor(self, image):
        import queue
        import threading
        """Dummy function to classify a tumor."""

        # convert image to pixmap
        pixmap_image = QPixmap(self.IMAGE_FOR_DIAGNOSIS)
        # Access the Model APIs if necessary
        from API.ModelAPI.clf_model_connection_api import CLASSIFY_IMAGE_wBOTH_MODELS__for_btcm_mdl_v01s_using_direct_pixmap, \
            access_BOTH_models__for_btcm_mdl_v01s, CLASSIFY_IMAGE_wBOTH_MODELS__for_btcm_mdl_21ms_using_direct_pixmap, \
            access_BOTH_models__for_btcm_mdl_21ms
        h5_model__for_btcm_mdl_v01, keras_model__for_btcm_mdl_v01 = access_BOTH_models__for_btcm_mdl_v01s()
        h5_model__for_btcm_mdl_21m, keras_model__for_btcm_mdl_21m = access_BOTH_models__for_btcm_mdl_21ms()

        result_queue = queue.Queue()  # Thread-safe queue to store results

        def classify_v01s(image_pixmap: QPixmap):
            result = CLASSIFY_IMAGE_wBOTH_MODELS__for_btcm_mdl_v01s_using_direct_pixmap(
                h5_MODEL_path=h5_model__for_btcm_mdl_v01, keras_MODEL_path=keras_model__for_btcm_mdl_v01, image_pixmap=image_pixmap
            )
            result_queue.put(("v01s", result))

        def classify_21ms(image_pixmap: QPixmap):
            result = CLASSIFY_IMAGE_wBOTH_MODELS__for_btcm_mdl_21ms_using_direct_pixmap(
                h5_MODEL_path=h5_model__for_btcm_mdl_21m, keras_MODEL_path=keras_model__for_btcm_mdl_21m, image_pixmap=image_pixmap
            )
            result_queue.put(("21ms", result))

        # Create threads
        thread1 = threading.Thread(target=classify_v01s, args=(pixmap_image,))
        thread2 = threading.Thread(target=classify_21ms, args=(pixmap_image,))

        # Start threads
        thread1.start()
        thread2.start()

        # Wait for both threads to complete
        thread1.join()
        thread2.join()

        # Retrieve results
        results = {}
        while not result_queue.empty():
            key, value = result_queue.get()
            results[key] = value

        result__for_btcm_mdl_v01s = results.get("v01s")
        result__for_btcm_mdl_21ms = results.get("21ms")

        # Next part of the code executes only after both functions complete
        print("Both classifications are complete.")

        print("======================= * * * * * =======================")
        print("======================= * * * * * =======================")

        print("RESULT: ", result__for_btcm_mdl_v01s)
        print("RESULT: ", result__for_btcm_mdl_21ms)

        print("======================= * * * * * =======================")
        print("======================= * * * * * =======================")

        conf_score__for_btcm_mdl_v01s: float = result__for_btcm_mdl_v01s[2]
        print("CONFIDENCE SCORE: ", conf_score__for_btcm_mdl_v01s)

        conf_score__for_btcm_mdl_21ms: float = result__for_btcm_mdl_21ms[2]
        print("CONFIDENCE SCORE: ", conf_score__for_btcm_mdl_21ms)

        max_conf_score: float = max(conf_score__for_btcm_mdl_v01s, conf_score__for_btcm_mdl_21ms)
        print("MAX CONF SCORE:", max_conf_score)

        map_ = {0: 'no_tumor', 1: 'glioma_tumor', 2: 'meningioma_tumor', 3: 'pituitary_tumor'}

        revmap = {v: k for k, v in map_.items()}

        proper_naming_convention_map = {0: 'No Tumor', 1: 'Glioma Tumor', 2: 'Meningioma Tumor', 3: 'Pituitary Tumor'}
        result__for_btcm_mdl_v01s = proper_naming_convention_map[revmap[result__for_btcm_mdl_v01s[1][0]]]
        result__for_btcm_mdl_21ms = proper_naming_convention_map[revmap[result__for_btcm_mdl_21ms[1][0]]]

        print("DEBUG: ", result__for_btcm_mdl_v01s, result__for_btcm_mdl_21ms)

        result_text = None
        self.TUMOR_TYPE = None

        if result__for_btcm_mdl_21ms == result__for_btcm_mdl_v01s:
            self.output_label_for_diagnosis.setText("Result: " + result__for_btcm_mdl_v01s + f"\nCS: {round(max_conf_score, 6)}")
            result_text = f"Tumor Result\n{result__for_btcm_mdl_v01s}\nConfidence Score: {round(max_conf_score, 6)}"
            self.TUMOR_TYPE = result__for_btcm_mdl_v01s
        else:
            if conf_score__for_btcm_mdl_v01s > conf_score__for_btcm_mdl_21ms:
                self.output_label_for_diagnosis.setText(
                    "Result: " + result__for_btcm_mdl_v01s + f"\nCS: {round(conf_score__for_btcm_mdl_v01s, 6)}")
                result_text = f"Tumor Result\n{result__for_btcm_mdl_v01s}\nConfidence Score: {round(conf_score__for_btcm_mdl_v01s, 6)}"
                self.TUMOR_TYPE = result__for_btcm_mdl_v01s
            if conf_score__for_btcm_mdl_21ms > conf_score__for_btcm_mdl_v01s:
                self.output_label_for_diagnosis.setText(
                    "Result: " + result__for_btcm_mdl_21ms + f"\nCS: {round(conf_score__for_btcm_mdl_21ms, 6)}")
                result_text = f"Tumor Result\n{result__for_btcm_mdl_21ms}\nConfidence Score: {round(conf_score__for_btcm_mdl_21ms, 6)}"
                self.TUMOR_TYPE = result__for_btcm_mdl_21ms

        # check if self.output_label_for_diagnosis is not empty ot none
        if self.output_label_for_diagnosis.text():
            self.accept_button.setVisible(True)
            self.reject_button.setVisible(True)
        # Notify
        if self.notification_settings.isChecked():
            print("TRUE - checked")
            notification.notify(
                title="Computation Result",
                message=result_text,
                app_name="YourAppName",
                timeout=5  # Notification duration in seconds
            )

        print("DONE * DONE * DONE * DONE * DONE")

    def fShow_Home_Frame(self):
        """Display the Home frame in the content area with search functionality."""
        self.fClear_Content_Area()

        # Welcome Message
        home_label = QLabel(f"Welcome to the Home Page! Hello Dr. {self.username.title()}")
        home_label.setAlignment(Qt.AlignCenter)

        # Search Bar Layout with White Theme
        search_layout = QVBoxLayout()

        # Label Styling
        search_label = QLabel("Search Patient Record:")
        search_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")

        # Search Input Styling
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search value...")
        self.search_input.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 6px;
            font-size: 14px;
            margin-bottom: 30px;
        """)
        self.search_input.setFocus()

        # Search Options (Modern Radio Buttons)
        self.search_by_email = QRadioButton("Email")
        self.search_by_id = QRadioButton("Patient ID")
        self.search_by_phone = QRadioButton("Phone")
        self.search_by_email.setChecked(True)  # Default selection

        # Styling for Modern Look
        radio_style = """
            QRadioButton {
                font-size: 14px;
                color: #333;
                padding: 4px;
                font-weight: bold;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid #0078D7;
                background: white;
            }
            QRadioButton::indicator:checked {
                background: yellow;
                border: 2px solid #005A9E;
            }
        """

        # Apply Styles
        self.search_by_email.setStyleSheet(radio_style)
        self.search_by_id.setStyleSheet(radio_style)
        self.search_by_phone.setStyleSheet(radio_style)

        # Radio Button Layout (Horizontal)
        radio_layout = QHBoxLayout()
        radio_layout.setSpacing(15)  # Adds spacing between buttons
        radio_layout.addWidget(self.search_by_email)
        radio_layout.addWidget(self.search_by_id)
        radio_layout.addWidget(self.search_by_phone)

        # increase the bottom margin for radio buttons
        radio_layout.setContentsMargins(0, 0, 0, 20)

        # Search Button
        self.search_button = QPushButton("Search")
        self.search_button.setStyleSheet(self.fGet_Button_Style())
        self.search_button.clicked.connect(self.fPerform_Search)

        # Add Widgets to Search Layout
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addLayout(radio_layout)
        search_layout.addWidget(self.search_button)

        # add patient button
        self.add_patient_button = QPushButton("Add Patient")
        self.add_patient_button.clicked.connect(self.fAdd_Patient)
        self.add_patient_button.setStyleSheet(self.fGet_Button_Style())
        self.content_layout.addWidget(self.add_patient_button)

        # Add Widgets to Content Layout
        self.content_layout.addWidget(home_label)
        self.content_layout.addLayout(search_layout)

    def fShow_Upload_Frame(self):
        """Display the Upload frame in the content area."""
        self.fClear_Content_Area()
        upload_label = QLabel("Upload your files here!")
        upload_label.setAlignment(Qt.AlignCenter)

        # Image display area
        self.image_view = QLabel(self)
        self.image_view.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(self.image_view)

        # Upload button
        self.upload_image_button = QPushButton("Upload Image")
        self.upload_image_button.clicked.connect(self.fUpload_Image_To_Check_Classification)
        self.upload_image_button.setStyleSheet(self.fGet_Button_Style())
        self.content_layout.addWidget(self.upload_image_button)

        # Classification button (Initially hidden)
        self.classify_button = QPushButton("Classify Image")
        self.classify_button.clicked.connect(self.fClassify_Image)
        self.classify_button.setVisible(False)
        self.classify_button.setStyleSheet(self.fGet_Button_Style())
        self.content_layout.addWidget(self.classify_button)

        # Output label
        self.output_label = QLabel(self)
        self.output_label.setAlignment(Qt.AlignCenter)

        # font style
        self.output_label.setStyleSheet("font-weight: bold; color: black; font-size: 20px;")
        self.content_layout.addWidget(self.output_label)

        self.content_layout.addWidget(upload_label)

    def fUpload_Image_To_Check_Classification(self):
        print("Uploading image...")
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image File", "",
                                                   "Images (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)

        print("file path: ", file_path)
        if file_path:
            self.image_view.setPixmap(QPixmap(file_path).scaled(300, 300, Qt.KeepAspectRatio))
            self.classify_button.setVisible(True)

            self.FINAL_FILE_PATH = file_path

    def fClassify_Image(self):
        import threading
        import queue

        # image path
        from Image.load_image import return_image_path
        print(return_image_path())
        self.IMAGE_PATH = return_image_path()

        # Access the Model APIs if necessary
        from API.ModelAPI.clf_model_connection_api import CLASSIFY_IMAGE_wBOTH_MODELS__for_btcm_mdl_v01s, access_BOTH_models__for_btcm_mdl_v01s, CLASSIFY_IMAGE_wBOTH_MODELS__for_btcm_mdl_21ms, access_BOTH_models__for_btcm_mdl_21ms
        h5_model__for_btcm_mdl_v01, keras_model__for_btcm_mdl_v01 = access_BOTH_models__for_btcm_mdl_v01s()
        h5_model__for_btcm_mdl_21m, keras_model__for_btcm_mdl_21m = access_BOTH_models__for_btcm_mdl_21ms()

        image_path = self.FINAL_FILE_PATH
        result_queue = queue.Queue()  # Thread-safe queue to store results

        def classify_v01s(image_path_):
            result = CLASSIFY_IMAGE_wBOTH_MODELS__for_btcm_mdl_v01s(
                h5_model__for_btcm_mdl_v01, keras_model__for_btcm_mdl_v01, image_path_
            )
            result_queue.put(("v01s", result))

        def classify_21ms(image_path_):
            result = CLASSIFY_IMAGE_wBOTH_MODELS__for_btcm_mdl_21ms(
                h5_model__for_btcm_mdl_21m, keras_model__for_btcm_mdl_21m, image_path_
            )
            result_queue.put(("21ms", result))

        # Create threads
        thread1 = threading.Thread(target=classify_v01s, args=(image_path,))
        thread2 = threading.Thread(target=classify_21ms, args=(image_path,))

        # Start threads
        thread1.start()
        thread2.start()

        # Wait for both threads to complete
        thread1.join()
        thread2.join()

        # Retrieve results
        results = {}
        while not result_queue.empty():
            key, value = result_queue.get()
            results[key] = value

        result__for_btcm_mdl_v01s = results.get("v01s")
        result__for_btcm_mdl_21ms = results.get("21ms")

        # Next part of the code executes only after both functions complete
        print("Both classifications are complete.")

        print("======================= * * * * * =======================")
        print("======================= * * * * * =======================")

        print("RESULT: ", result__for_btcm_mdl_v01s)
        print("RESULT: ", result__for_btcm_mdl_21ms)

        print("======================= * * * * * =======================")
        print("======================= * * * * * =======================")

        conf_score__for_btcm_mdl_v01s: float = result__for_btcm_mdl_v01s[2]
        print("CONFIDENCE SCORE: ", conf_score__for_btcm_mdl_v01s)

        conf_score__for_btcm_mdl_21ms: float = result__for_btcm_mdl_21ms[2]
        print("CONFIDENCE SCORE: ", conf_score__for_btcm_mdl_21ms)

        max_conf_score: float = max(conf_score__for_btcm_mdl_v01s, conf_score__for_btcm_mdl_21ms)
        print("MAX CONF SCORE:", max_conf_score)

        map_ = {0: 'no_tumor', 1: 'glioma_tumor', 2: 'meningioma_tumor', 3: 'pituitary_tumor'}

        revmap = {v: k for k, v in map_.items()}

        proper_naming_convention_map = {0: 'No Tumor', 1: 'Glioma Tumor', 2: 'Meningioma Tumor', 3: 'Pituitary Tumor'}
        result__for_btcm_mdl_v01s = proper_naming_convention_map[revmap[result__for_btcm_mdl_v01s[1][0]]]
        result__for_btcm_mdl_21ms = proper_naming_convention_map[revmap[result__for_btcm_mdl_21ms[1][0]]]

        print("DEBUG: ", result__for_btcm_mdl_v01s, result__for_btcm_mdl_21ms)

        ####################################################################################################
        ####################################################################################################
        ####################################################################################################

        result_text = None

        if result__for_btcm_mdl_21ms == result__for_btcm_mdl_v01s:
            self.output_label.setText("Result: " + result__for_btcm_mdl_v01s + f"\nCS: {round(max_conf_score, 6)}")
            result_text = f"Tumor Result\n{result__for_btcm_mdl_v01s}\nConfidence Score: {round(max_conf_score, 6)}"
        else:
            if conf_score__for_btcm_mdl_v01s > conf_score__for_btcm_mdl_21ms:
                self.output_label.setText("Result: " + result__for_btcm_mdl_v01s + f"\nCS: {round(conf_score__for_btcm_mdl_v01s, 6)}")
                result_text = f"Tumor Result\n{result__for_btcm_mdl_v01s}\nConfidence Score: {round(conf_score__for_btcm_mdl_v01s, 6)}"
            if conf_score__for_btcm_mdl_21ms > conf_score__for_btcm_mdl_v01s:
                self.output_label.setText("Result: " + result__for_btcm_mdl_21ms + f"\nCS: {round(conf_score__for_btcm_mdl_21ms, 6)}")
                result_text = f"Tumor Result\n{result__for_btcm_mdl_21ms}\nConfidence Score: {round(conf_score__for_btcm_mdl_21ms, 6)}"

        # Notify
        if self.notification_settings.isChecked():
            print("TRUE - checked")
            notification.notify(
                title="Computation Result",
                message=result_text,
                app_name="YourAppName",
                timeout=5  # Notification duration in seconds
            )

    @staticmethod
    def fSet_Dark_Mode():
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(45, 45, 45))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        QApplication.instance().setPalette(palette)

    def fGet_Input_Style(self):
        return (
            "color: white; background-color: #2b2b2b; border: 1px solid #5a5a5a; border-radius: 5px; padding: 5px;"
            if self.dark_mode else
            "color: black; background-color: #f5f5f5; border: 1px solid #cccccc; border-radius: 5px; padding: 5px;"
        )

    def fGet_Button_Style(self):
        return (
            "QPushButton{color: white; background-color: #388E3C; border-radius: 8px; font-size: 15px; padding: 12px 32px; "
            "border: 2px solid #2E7D32; transition: background-color 0.3s ease-in-out;}"
            "QPushButton:hover { background-color: #2E7D32; }"
            if self.dark_mode else
            "QPushButton{color: black; background-color: #64B5F6; border-radius: 8px; font-size: 15px; padding: 12px 32px; "
            "border: 2px solid #42A5F5; transition: background-color 0.3s ease-in-out;}"
            "QPushButton:hover { background-color: #42A5F5; }"
        )

    def fGet_Theme_Button_Style(self):
        return (
            "QPushButton{color: white; background-color: #8E24AA; border-radius: 8px; font-size: 13px; height: 32px; "
            "padding: 0 12px; border: 2px solid #7B1FA2; transition: background-color 0.3s ease-in-out;}"
            "QPushButton:hover { background-color: #7B1FA2; }"
            if self.dark_mode else
            "QPushButton{color: black; background-color: #FF9800; border-radius: 8px; font-size: 13px; height: 32px; "
            "padding: 0 12px; border: 2px solid #FB8C00; transition: background-color 0.3s ease-in-out;}"
            "QPushButton:hover { background-color: #FB8C00; }"
        )

    def fGet_Expand_Button_Style(self):
        return (
            "QPushButton{color: white; background-color: #43A047; border-radius: 8px; font-size: 15px; padding: 12px 32px; "
            "margin: 12px 0; border: 2px solid #388E3C; transition: background-color 0.3s ease-in-out;}"
            "QPushButton:hover { background-color: #388E3C; }"
            if self.dark_mode else
            "QPushButton{color: black; background-color: #4FC3F7; border-radius: 8px; font-size: 15px; padding: 12px 32px; "
            "margin: 12px 0; border: 2px solid #29B6F6; transition: background-color 0.3s ease-in-out;}"
            "QPushButton:hover { background-color: #29B6F6; }"
        )

    def fPerform_Search(self):
        """Perform search based on selected criteria."""
        search_value = self.search_input.text().strip()

        # Ensure input is not empty
        if not search_value:
            QMessageBox.warning(self, "Input Error", "Please enter a search value.")
            return

        # Determine Search Criteria
        if self.search_by_email.isChecked():
            criteria = "email"
        elif self.search_by_id.isChecked():
            criteria = "patient_id"
        elif self.search_by_phone.isChecked():
            criteria = "phone"
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a search criteria.")
            return

        # Fetch Patient Record (Replace with actual database/query logic)
        patient_record = self.fGet_Patient_Record(search_value, criteria)

        if patient_record:
            self.fDisplay_Patient_Record(patient_record)
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

        print("------------- PATH:", PATH_)
        print("------------- dbPATH:", dbPATH_)

        # Retrieve patient details
        patient_data = get_patient_details(search_value=search_value, criteria=criteria, PATH_=dbPATH_)

        print("DEBUG ============ PATIENT DATA ============\n", patient_data)

        print("True/False: ", patient_data is not None)

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

            print("DEBUG ============ PATIENT RECORD ============\n", patient_record)

            # Fetch tumor image, image_vector is BLOB
            image_vector = get_tumor_image(patient_id=patient_record["patient_id"], PATH_=dbPATH_)

            print("DEBUG ============ IMAGE VECTOR ============\n", type(image_vector),
                  len(image_vector) if image_vector else 0)

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

            print("DEBUG ============ PATIENT RECORD ============\n", patient_record)

            return patient_record  # Return structured dictionary
        else:
            print("No patient record found.")
            return None

    def fDisplay_Patient_Record(self, patient_record):
        print("PATIENT --> ", patient_record)
        """Display patient details along with the image in a QDialog."""
        if not patient_record:
            QMessageBox.warning(self, "Error", "No patient record found.")
            return

        # Create a dialog window
        dialog = QDialog(self)
        dialog.setWindowTitle("Patient Record")
        dialog.setMinimumWidth(400)

        # Layout for patient details
        layout = QVBoxLayout()

        # Patient details
        record_info = (
            f"Patient ID: {patient_record['patient_id']}\n"
            f"Name: {patient_record['first_name']} {patient_record['last_name']}\n"
            f"Date of Birth: {patient_record['date_of_birth']}\n"
            f"Gender: {patient_record['gender']}\n"
            f"Phone: {patient_record['phone_number']}\n"
            f"Email: {patient_record['email']}"
        )

        _image = patient_record["image"]

        # to-pdf button
        to_pdf_button = QPushButton("To PDF")
        to_pdf_button.clicked.connect(lambda: self.fTo_PDF(patient_record))

        # generate report button
        generate_report_button = QPushButton("Generate Report")
        generate_report_button.clicked.connect(lambda: self.fGenerate_Report(patient_record))

        details_label = QLabel(record_info)

        layout.addWidget(details_label)
        layout.addWidget(to_pdf_button)
        layout.addWidget(generate_report_button)

        # Display image if available
        if isinstance(patient_record["image"], QPixmap):
            image_label = QLabel()
            image_label.setPixmap(patient_record["image"].scaled(200, 200))  # Resize for display
            layout.addWidget(image_label)
        else:
            no_image_label = QLabel("No Image Available")
            layout.addWidget(no_image_label)

        # Set layout and show dialog
        dialog.setLayout(layout)
        dialog.exec_()

    @staticmethod
    def fTo_PDF(patient_record):
        """Generate a PDF file with patient details and image."""
        file_path, _ = QFileDialog.getSaveFileName(None, "Save PDF", "", "PDF Files (*.pdf)")
        if not file_path:
            return

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Title
        pdf.cell(200, 10, "Patient Record", ln=True, align="C")
        pdf.ln(10)

        # Patient details
        details = (
            f"Patient ID: {patient_record['patient_id']}\n"
            f"Name: {patient_record['first_name']} {patient_record['last_name']}\n"
            f"Date of Birth: {patient_record['date_of_birth']}\n"
            f"Gender: {patient_record['gender']}\n"
            f"Phone: {patient_record['phone_number']}\n"
            f"Email: {patient_record['email']}\n"
        )

        pdf.multi_cell(0, 10, details)
        pdf.ln(5)  # Space before image

        # Handle the image
        if isinstance(patient_record["image"], QPixmap):
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_image:
                temp_path = temp_image.name  # Get temporary file path
                patient_record["image"].save(temp_path, "PNG")  # Save QPixmap to file

            # Add image to PDF
            pdf.image(temp_path, x=10, w=60)  # Position & width (adjust as needed)

            # Remove temporary file after adding to PDF
            os.remove(temp_path)

        else:
            pdf.cell(200, 10, "No Image Available", ln=True, align="C")

        # Save PDF
        pdf.output(file_path)
        QMessageBox.information(None, "Success", f"PDF saved at {file_path}")

    @staticmethod
    def fGenerate_Report(patient_record):
        """Generate a text report with patient details."""
        file_path, _ = QFileDialog.getSaveFileName(None, "Save Report", "", "Text Files (*.txt)")
        if not file_path:
            return

        report_content = (
            f"Patient ID: {patient_record['patient_id']}\n"
            f"Name: {patient_record['first_name']} {patient_record['last_name']}\n"
            f"Date of Birth: {patient_record['date_of_birth']}\n"
            f"Gender: {patient_record['gender']}\n"
            f"Phone: {patient_record['phone_number']}\n"
            f"Email: {patient_record['email']}\n"
            f"Medical History: {patient_record.get('medical_history', 'Not Available')}\n"
        )

        try:
            with open(file_path, "w") as file:
                file.write(report_content)
            QMessageBox.information(None, "Success", f"Report saved at {file_path}")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to save report: {str(e)}")

    def fAdd_Patient(self):
        from API.DatabaseAPI.client_database_connection import get_doctor_id
        from Main.utils import get_current_system_path, change_path_to_db
        from Screens.AddPatientDialog import AddPatientDialog

        PATH_ = get_current_system_path()
        dbPATH_ = change_path_to_db(PATH_)

        doctor_id = get_doctor_id(username=self.username, PATH_=dbPATH_)

        print("doctor_id:", doctor_id)

        if doctor_id:
            # self.add_patient_window = AddPatientPage(db_path=dbPATH_, doctor_id=doctor_id)
            # self.add_patient_window.show()

            is_dark_model = self.dark_mode
            print("DARK MODE: ", is_dark_model)

            self.add_patient_dialog = AddPatientDialog(self, db_path=dbPATH_, doctor_id=doctor_id)
            self.add_patient_dialog.exec_()
        else:
            QMessageBox.critical(self, "Error", "Failed to retrieve doctor ID.")
        pass
