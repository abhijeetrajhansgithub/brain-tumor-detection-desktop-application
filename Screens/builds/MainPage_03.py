from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame, QApplication, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class MainPage_03(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.upload_image_button = None
        self.FINAL_FILE_PATH = None
        self.IMAGE_PATH = None
        self.setWindowTitle("Main Page v3.0.0")
        self.setGeometry(100, 100, 800, 600)
        self.dark_mode = True  # Default to dark mode
        self.set_dark_mode()  # Apply dark mode

        self.username = username

        # Main layout
        self.central_widget = QWidget()
        self.main_layout = QHBoxLayout(self.central_widget)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(60)  # Initially collapsed
        self.sidebar_layout = QVBoxLayout(self.sidebar)

        # Home button
        self.home_button = QPushButton("🏠")
        self.home_button.setStyleSheet("""
            text-align: left;
            min-width: 60px;
            max-width: 300px;
            border: none;
            padding: 5px;
        """)
        self.home_button.clicked.connect(self.show_home_frame)  # Connect to frame function
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
        self.upload_button.clicked.connect(self.show_upload_frame)  # Connect to frame function
        self.sidebar_layout.addWidget(self.upload_button)

        # Theme button
        # Theme changer button
        self.theme_changer_main_wn = QPushButton("Change to Light Theme" if self.dark_mode else "Change to Dark Theme")
        self.theme_changer_main_wn.clicked.connect(self.toggle_theme_main_wn)
        self.theme_changer_main_wn.setStyleSheet(self.get_theme_button_style())
        self.sidebar_layout.addWidget(self.theme_changer_main_wn)

        # Expand/Collapse button
        self.expand_button = QPushButton("➡️")
        self.expand_button.setStyleSheet(self.get_expand_button_style())

        # Position expand button at the bottom of the sidebar
        self.sidebar_layout.addStretch()
        self.sidebar_layout.addWidget(self.expand_button, 0, Qt.AlignBottom)

        self.expand_button.clicked.connect(self.toggle_sidebar)

        # Content area
        self.content_area = QFrame()
        self.content_area.setStyleSheet("background-color: gray;")
        self.content_layout = QVBoxLayout(self.content_area)

        # Initialize with the home frame
        self.show_home_frame()

        # Add sidebar and content area to the main layout
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content_area)

        self.implement_themes()

        # Set central widget
        self.setCentralWidget(self.central_widget)
        self.toggle_theme_main_wn()

    def set_theme(self):
        if self.dark_mode:
            self.set_dark_mode()
        else:
            QApplication.instance().setPalette(QApplication.instance().style().standardPalette())

    def toggle_theme_main_wn(self):
        self.dark_mode = not self.dark_mode
        self.set_theme()
        if self.sidebar.width() == 60:
            self.theme_changer_main_wn.setText("🌞" if self.dark_mode else "🌚")
        else:
            self.theme_changer_main_wn.setText("🐙 Change to Light Theme" if self.dark_mode else "🐙 Change to Dark Theme")
        self.implement_themes()

    def implement_themes(self):
        if type(self.home_button) == QPushButton:
            self.home_button.setStyleSheet(self.get_button_style())
        if type(self.upload_button) == QPushButton:
            self.upload_button.setStyleSheet(self.get_button_style())
        if type(self.theme_changer_main_wn) == QPushButton:
            self.theme_changer_main_wn.setStyleSheet(self.get_theme_button_style())
        if type(self.expand_button) == QPushButton:
            self.expand_button.setStyleSheet(self.get_expand_button_style())

    def toggle_sidebar(self):
        """Toggle the sidebar's width between collapsed and expanded."""
        if self.sidebar.width() == 60:
            self.sidebar.setFixedWidth(int(self.width() / 4))  # Expand
            if type(self.expand_button) == QPushButton:
                self.expand_button.setStyleSheet(self.get_expand_button_style())
                self.expand_button.setText("⬅️")

            if type(self.home_button) == QPushButton:
                self.home_button.setStyleSheet(self.get_button_style())
                self.home_button.setText("🏠 Home")

            if type(self.upload_button) == QPushButton:
                self.upload_button.setStyleSheet(self.get_button_style())
                self.upload_button.setText("📤 Upload")

            if type(self.theme_changer_main_wn) == QPushButton:
                self.theme_changer_main_wn.setStyleSheet(self.get_theme_button_style())
                self.theme_changer_main_wn.setText("🐙 Change to Light Theme" if self.dark_mode else "🐙 Change to Dark Theme")
        else:
            self.sidebar.setFixedWidth(60)  # Collapse
            if type(self.expand_button) == QPushButton:
                self.expand_button.setStyleSheet(self.get_expand_button_style())
                self.expand_button.setText("➡️")

            if type(self.home_button) == QPushButton:
                self.home_button.setStyleSheet(self.get_button_style())
                self.home_button.setText("🏠")

            if type(self.upload_button) == QPushButton:
                self.upload_button.setStyleSheet(self.get_button_style())
                self.upload_button.setText("📤")

            if type(self.theme_changer_main_wn) == QPushButton:
                self.theme_changer_main_wn.setStyleSheet(self.get_theme_button_style())
                self.theme_changer_main_wn.setText("🌞" if self.dark_mode else "🌚")

    def show_home_frame(self):
        """Display the Home frame in the content area."""
        self.clear_content_area()
        home_label = QLabel("Welcome to the Home Page! You are logged in as " + self.username)
        home_label.setAlignment(Qt.AlignCenter)

        self.content_layout.addWidget(home_label)

    def show_upload_frame(self):
        """Display the Upload frame in the content area."""
        self.clear_content_area()
        upload_label = QLabel("Upload your files here!")
        upload_label.setAlignment(Qt.AlignCenter)

        # Image display area
        self.image_view = QLabel(self)
        self.image_view.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(self.image_view)

        # Upload button
        self.upload_image_button = QPushButton("Upload Image")
        self.upload_image_button.clicked.connect(self.upload_image)
        self.upload_image_button.setStyleSheet(self.get_button_style())
        self.content_layout.addWidget(self.upload_image_button)

        # Classification button (Initially hidden)
        self.classify_button = QPushButton("Classify Image")
        self.classify_button.clicked.connect(self.classify_image)
        self.classify_button.setVisible(False)
        self.classify_button.setStyleSheet(self.get_button_style())
        self.content_layout.addWidget(self.classify_button)

        # Output label
        self.output_label = QLabel(self)
        self.output_label.setAlignment(Qt.AlignCenter)

        # font style
        self.output_label.setStyleSheet("font-weight: bold; color: black; font-size: 20px;")
        self.content_layout.addWidget(self.output_label)


        self.content_layout.addWidget(upload_label)

    def upload_image(self):
        print("Uploading image...")
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image File", "",
                                                   "Images (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)

        print("file path: ", file_path)
        if file_path:
            self.image_view.setPixmap(QPixmap(file_path).scaled(300, 300, Qt.KeepAspectRatio))
            self.classify_button.setVisible(True)

            self.FINAL_FILE_PATH = file_path

    def classify_image(self):
        # image path
        from Image.load_image import return_image_path
        print(return_image_path())
        self.IMAGE_PATH = return_image_path()

        # Access the Model APIs if necessary
        from API.ModelAPI.clf_model_connection_api import CLASSIFY_IMAGE_wBOTH_MODELS__for_btcm_mdl_v01s, access_BOTH_models__for_btcm_mdl_v01s
        h5_model, keras_model = access_BOTH_models__for_btcm_mdl_v01s()

        image_path = self.FINAL_FILE_PATH
        result = CLASSIFY_IMAGE_wBOTH_MODELS__for_btcm_mdl_v01s(h5_model, keras_model, image_path)

        print("RESULT: ", result)
        map = {0: 'no_tumor', 1: 'glioma_tumor', 2: 'meningioma_tumor', 3: 'pituitary_tumor'}
        revmap = {v: k for k, v in map.items()}
        proper_naming_convention_map = {0: 'No Tumor', 1: 'Glioma Tumor', 2: 'Meningioma Tumor', 3: 'Pituitary Tumor'}
        result = proper_naming_convention_map[revmap[result[1][0]]]
        self.output_label.setText(result)
        pass

    def clear_content_area(self):
        """Clear all widgets from the content area."""
        while self.content_layout.count():
            widget = self.content_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

    def set_dark_mode(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(45, 45, 45))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        QApplication.instance().setPalette(palette)

    def get_input_style(self):
        return (
            "color: white; background-color: #2b2b2b; border: 1px solid #5a5a5a; border-radius: 5px; padding: 5px;"
            if self.dark_mode else
            "color: black; background-color: #f5f5f5; border: 1px solid #cccccc; border-radius: 5px; padding: 5px;"
        )

    def get_button_style(self):
        return (
            "color: white; background-color: #4caf50; border-radius: 5px; font-size: 14px; padding: 10px 30px 10px 30px;"
            if self.dark_mode else
            "color: black; background-color: #87ceeb; border-radius: 5px; font-size: 14px; padding: 10px 30px 10px 30px;"
        )

    def get_theme_button_style(self):
        return (
            "color: white; background-color: #9c27b0; font-size: 12px; radius: 5px; border-radius: 5px; max-height: 30px; min-height: 30px; padding-left: 8px; padding-right: 8px;"
            if self.dark_mode else
            "color: black; background-color: #ffb74d; font-size: 12px; radius: 5px; border-radius: 5px; max-height: 30px; min-height: 30px; padding-left: 8px; padding-right: 8px;"
        )

    def get_expand_button_style(self):
        return (
            "color: white; background-color: #4caf50; border-radius: 5px; font-size: 14px; padding: 10px 30px 10px 30px; margin-bottom: 10px; margin-top: 10px;"
            if self.dark_mode else
            "color: black; background-color: #87ceeb; border-radius: 5px; font-size: 14px; padding: 10px 30px 10px 30px; margin-bottom: 10px; margin-top: 10px;"
        )
