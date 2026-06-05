from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login Page")
        self.setGeometry(100, 100, 400, 300)
        self.dark_mode = True  # Default to dark mode
        self.set_dark_mode()  # Apply dark mode

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Input layout for username and password
        input_layout = QVBoxLayout()

        # Username input field
        self.username_layout = QHBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet(self.get_input_style())
        self.username_input.setMaximumWidth(560)

        # Add username input field to username_layout
        self.username_layout.addWidget(self.username_input)
        self.username_layout.setAlignment(Qt.AlignCenter)

        # Add username_layout to input_layout
        input_layout.addLayout(self.username_layout)

        # Password layout (horizontal layout for password input and peek button)
        self.password_layout = QHBoxLayout()

        # Password input field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)  # Start with password hidden
        self.password_input.setStyleSheet(self.get_input_style())
        self.password_input.setMaximumWidth(500)

        # Create a small button for peeking the password (with eye symbol)
        self.peek_button = QPushButton("😎")
        self.peek_button.setStyleSheet(
            "width: 30px; height: 30px; font-size: 16px; padding: 0;")  # 30px width and eye symbol
        self.peek_button.setMaximumWidth(50)
        self.peek_button.clicked.connect(self.peek_password)
        # transparent background
        self.peek_button.setStyleSheet("background-color: transparent; border: none; font-size: 36px;")

        # Add password input and peek button to password_layout
        self.password_layout.addWidget(self.password_input)
        self.password_layout.addWidget(self.peek_button)
        self.password_layout.setAlignment(Qt.AlignCenter)

        # Add password layout to input_layout
        input_layout.addLayout(self.password_layout)  # Add the password layout instead of input field
        input_layout.setAlignment(Qt.AlignCenter)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        self.login_button = QPushButton("Login")
        self.signup_button = QPushButton("Signup")
        self.forgot_password_button = QPushButton("Forgot Password")

        # set max width
        self.login_button.setMaximumWidth(400)
        self.signup_button.setMaximumWidth(400)
        self.forgot_password_button.setMaximumWidth(800)

        # set min width
        self.login_button.setMinimumWidth(100)
        self.signup_button.setMinimumWidth(100)
        self.forgot_password_button.setMinimumWidth(200)

        # Set button styles
        for button in [self.login_button, self.signup_button, self.forgot_password_button]:
            button.setStyleSheet(self.get_button_style())

        buttons_layout.addWidget(self.login_button)
        buttons_layout.addWidget(self.signup_button)
        buttons_layout.setAlignment(Qt.AlignCenter)

        outer_buttons_layout = QVBoxLayout()
        outer_buttons_layout.addLayout(buttons_layout)
        outer_buttons_layout.addWidget(self.forgot_password_button)
        outer_buttons_layout.setAlignment(Qt.AlignCenter)

        # Button functions
        self.login_button.clicked.connect(self.check_user_credentials_for_login)

        # Add layouts to main layout
        main_layout.addLayout(input_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addLayout(outer_buttons_layout)

        # Theme changer button
        self.theme_changer = QPushButton("Switch to Light Mode")
        self.theme_changer.clicked.connect(self.toggle_theme)
        self.theme_changer.setStyleSheet(self.get_theme_button_style())
        main_layout.addWidget(self.theme_changer, alignment=Qt.AlignRight | Qt.AlignBottom)

    def peek_password(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            # change the text of peek button
            self.peek_button.setText("🙂")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            # change the text of peek button
            self.peek_button.setText("😎")

    def get_input_style(self):
        if self.dark_mode:
            return "color: white; background-color: #2b2b2b; border: 1px solid #5a5a5a; border-radius: 5px; padding: 5px;"
        else:
            return "color: black; background-color: #f5f5f5; border: 1px solid #cccccc; border-radius: 5px; padding: 5px;"

    def get_button_style(self):
        if self.dark_mode:
            return (
                "color: white; background-color: #4caf50; border: none; padding: 10px 30px 10px 30px;"
                "border-radius: 5px; font-size: 14px;"
            )
        else:
            return (
                "color: black; background-color: #87ceeb; border: none; padding: 10px 30px 10px 30px;"
                "border-radius: 5px; font-size: 14px;"
            )

    def get_theme_button_style(self):
        if self.dark_mode:
            return (
                "color: white; background-color: #9c27b0; border: none; padding: 8px;"
                "border-radius: 5px; font-size: 12px;"
            )
        else:
            return (
                "color: black; background-color: #ffb74d; border: none; padding: 8px;"
                "border-radius: 5px; font-size: 12px;"
            )

    def set_dark_mode(self):
        self.dark_mode = True
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(45, 45, 45))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(35, 35, 35))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.Highlight, QColor(142, 45, 197))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        QApplication.instance().setPalette(palette)

        try:
            if type(self.theme_changer) == QPushButton:
                self.theme_changer.setStyleSheet(self.get_theme_button_style())
            if type(self.login_button) == QPushButton:
                self.login_button.setStyleSheet(self.get_button_style())
            if type(self.signup_button) == QPushButton:
                self.signup_button.setStyleSheet(self.get_button_style())
            if type(self.forgot_password_button) == QPushButton:
                self.forgot_password_button.setStyleSheet(self.get_button_style())
            if type(self.username_input) == QLineEdit:
                self.username_input.setStyleSheet(self.get_input_style())
            if type(self.password_input) == QLineEdit:
                self.password_input.setStyleSheet(self.get_input_style())
        except AttributeError:
            pass

        self.update_styles()

    def set_light_mode(self):
        self.dark_mode = False
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.Base, QColor(240, 240, 240))
        palette.setColor(QPalette.AlternateBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
        palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.Highlight, QColor(30, 144, 255))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

        # change the color of self.theme_changer QPushButton
        try:
            if type(self.theme_changer) == QPushButton:
                self.theme_changer.setStyleSheet(self.get_theme_button_style())
            if type(self.login_button) == QPushButton:
                self.login_button.setStyleSheet(self.get_button_style())
            if type(self.signup_button) == QPushButton:
                self.signup_button.setStyleSheet(self.get_button_style())
            if type(self.forgot_password_button) == QPushButton:
                self.forgot_password_button.setStyleSheet(self.get_button_style())
            if type(self.username_input) == QLineEdit:
                self.username_input.setStyleSheet(self.get_input_style())
            if type(self.password_input) == QLineEdit:
                self.password_input.setStyleSheet(self.get_input_style())
        except AttributeError:
            pass

        QApplication.instance().setPalette(palette)

        self.update_styles()

    def toggle_theme(self):
        if self.dark_mode:
            self.set_light_mode()
            self.theme_changer.setText("Switch to Dark Mode")
        else:
            self.set_dark_mode()
            self.theme_changer.setText("Switch to Light Mode")

    def update_styles(self):
        print("Updating styles...")

    def get_username(self):
        return self.username_input.text()

    def get_password(self):
        return self.password_input.text()

    def check_user_credentials_for_login(self):
        print("Checking user credentials...")
        username = self.get_username()
        password = self.get_password()
        print(f"Username: {username}, Password: {password}")


class MainApplication(QApplication):
    def __init__(self):
        super().__init__([])
        self.main_window = MainWindow()
        self.main_window.show()


if __name__ == "__main__":
    app = MainApplication()
    app.exec_()
