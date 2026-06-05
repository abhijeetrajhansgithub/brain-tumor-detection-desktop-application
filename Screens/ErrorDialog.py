from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

class ErrorDialog(QDialog):
    def __init__(self, message):
        super().__init__()

        # Configure the dialog
        self.setWindowTitle("Error")
        self.setFixedSize(450, 180)
        self.setStyleSheet("""
            background-color: #1E1E2F;
            border-radius: 12px;
        """)

        # Fonts
        header_font = QFont("Arial", 14, QFont.Bold)
        message_font = QFont("Arial", 12)

        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Add label for the message
        label = QLabel(message)
        label.setFont(message_font)
        label.setStyleSheet("""
            color: #FF6B6B;
            font-size: 16px;
            font-weight: bold;
            padding: 15px;
        """)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Add a modern styled button
        button = QPushButton("OK")
        button.setFont(header_font)
        button.setStyleSheet("""
            QPushButton {
                background-color: #3D5A80;
                color: white;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #98C1D9;
            }
            QPushButton:pressed {
                background-color: #EE6C4D;
            }
        """)
        button.clicked.connect(self.accept)  # Close the dialog when clicked
        layout.addWidget(button)

        # Set the layout
        self.setLayout(layout)

        # Center the dialog on the screen
        self.setWindowModality(Qt.ApplicationModal)
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.move(screen_geometry.center() - self.rect().center())

# # Example usage
# if __name__ == "__main__":
#     import sys
#
#     app = QApplication(sys.argv)
#     dialog = ErrorDialog("Please enter username and password!")
#     dialog.exec_()  # Show the dialog