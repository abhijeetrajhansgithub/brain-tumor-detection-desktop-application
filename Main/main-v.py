from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QStackedWidget, QLabel, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

from Screens.ErrorDialog import ErrorDialog
from tkinter.messagebox import showinfo


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.signup_peek_button_pwd2 = None
        self.confirm_password_input = None
        self.signup_password_layout_2 = None
        self.signup_peek_button_pwd1 = None
        self.signup_password_input = None
        self.signup_password_layout_1 = None
        self.signup_user_email_input = None
        self.signup_username_input = None
        self.main_page = None
        self.theme_changer = None
        self.setWindowTitle("Login Page")
        self.setGeometry(100, 100, 900, 650)
        self.dark_mode = True  # Default to dark mode
        self.set_dark_mode()  # Apply dark mode

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a stacked widget
        self.stacked_widget = QStackedWidget()
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.stacked_widget)
        central_widget.setLayout(central_layout)

        # Create login and signup pages
        self.create_login_page()
        self.create_signup_page()

        # Set the initial page to be the login page
        self.stacked_widget.setCurrentWidget(self.login_page)


    def create_login_page(self):
        self.login_page = QWidget()

        # Main layout for login page
        main_layout = QVBoxLayout()
        self.login_page.setLayout(main_layout)

        # Input layout for username and password
        input_layout = QVBoxLayout()

        # Username input field
        self.username_layout = QHBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet(self.get_input_style())
        self.username_input.setMaximumWidth(560)

        self.username_layout.addWidget(self.username_input)
        self.username_layout.setAlignment(Qt.AlignCenter)
        input_layout.addLayout(self.username_layout)

        # Password layout
        self.password_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.get_input_style())
        self.password_input.setMaximumWidth(500)

        self.peek_button = QPushButton("😎")
        self.peek_button.setStyleSheet("background-color: transparent; border: none; font-size: 36px;")
        self.peek_button.setMaximumWidth(50)
        self.peek_button.clicked.connect(self.peek_password)

        self.password_layout.addWidget(self.password_input)
        self.password_layout.addWidget(self.peek_button)
        self.password_layout.setAlignment(Qt.AlignCenter)
        input_layout.addLayout(self.password_layout)
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

        self.login_button.clicked.connect(self.check_user_credentials_for_login)
        self.signup_button.clicked.connect(self.show_signup_page)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addLayout(outer_buttons_layout)

        # Theme changer button
        self.theme_changer_login = QPushButton("Change to Light Theme" if self.dark_mode else "Change to Dark Theme")
        self.theme_changer_login.clicked.connect(self.toggle_theme_login)
        self.theme_changer_login.setStyleSheet(self.get_theme_button_style())
        main_layout.addWidget(self.theme_changer_login, alignment=Qt.AlignRight | Qt.AlignBottom)

        self.stacked_widget.addWidget(self.login_page)

        # check the focus of username field
        # then if entered in clicked, focus on password
        self.username_input.returnPressed.connect(self.password_input.setFocus)

        # if return is pressed on password field, then login
        self.password_input.returnPressed.connect(self.check_user_credentials_for_login)
        self.override_keyPressEvent(self.username_input)
        self.override_keyPressEvent(self.password_input)

    def create_signup_page(self):
        self.signup_page = QWidget()

        # Main layout for signup page
        main_layout = QVBoxLayout()
        self.signup_page.setLayout(main_layout)

        # Input fields for signup
        input_layout = QVBoxLayout()

        self.signup_username_input = QLineEdit()
        self.signup_username_input.setPlaceholderText("Username")
        self.signup_username_input.setStyleSheet(self.get_input_style() + "margin-top: 30px;")
        self.signup_username_input.setMaximumWidth(560)
        input_layout.addWidget(self.signup_username_input)

        self.signup_user_email_input = QLineEdit()
        self.signup_user_email_input.setPlaceholderText("Email")
        self.signup_user_email_input.setStyleSheet(self.get_input_style() + "margin-bottom: 20px;")
        self.signup_user_email_input.setMaximumWidth(560)
        input_layout.addWidget(self.signup_user_email_input)

        self.fname_lname_layout = QVBoxLayout()

        self.fname_input = QLineEdit()
        self.fname_input.setPlaceholderText("First Name")
        self.fname_input.setStyleSheet(self.get_input_style())
        self.fname_input.setMaximumWidth(560)

        self.lname_input = QLineEdit()
        self.lname_input.setPlaceholderText("Last Name")
        self.lname_input.setStyleSheet(self.get_input_style() + "margin-bottom: 20px;")
        self.lname_input.setMaximumWidth(560)

        self.fname_lname_layout.addWidget(self.fname_input)
        self.fname_lname_layout.addWidget(self.lname_input)
        input_layout.addLayout(self.fname_lname_layout)

        self.specialization_licence_layout = QVBoxLayout()

        specializations = [
            "Neuro-oncology",
            "Neurosurgeon",
            "Neuroradiologist",
            "Neurologist",
            "Radiation Oncologist",
            "Medical Oncologist",
            "Pediatric Neuro-oncologist",
            "Pathologist",
            "Neuropsychologist",
            "Endocrinologist"
        ]

        # Dropdown menu for specializations
        self.specialization_input = QComboBox()
        self.specialization_input.addItems(specializations)
        self.specialization_input.setPlaceholderText("Select Specialization")
        self.specialization_input.setStyleSheet(self.get_input_style())
        self.specialization_input.setMaximumWidth(560)

        # Dropdown menu for licences
        self.licence_input = QLineEdit()
        self.licence_input.setPlaceholderText("Licence")
        self.licence_input.setStyleSheet(self.get_input_style() + "margin-bottom: 20px;")
        self.licence_input.setMaximumWidth(560)

        # Add specializations and licences to layout
        self.specialization_licence_layout.addWidget(self.specialization_input)
        self.specialization_licence_layout.addWidget(self.licence_input)

        input_layout.addLayout(self.specialization_licence_layout)

        self.signup_password_layout_1 = QHBoxLayout()

        self.signup_password_input = QLineEdit()
        self.signup_password_input.setPlaceholderText("Password")
        self.signup_password_input.setEchoMode(QLineEdit.Password)
        self.signup_password_input.setStyleSheet(self.get_input_style())
        self.signup_password_input.setMaximumWidth(500)

        self.signup_peek_button_pwd1 = QPushButton("😎")
        self.signup_peek_button_pwd1.setStyleSheet("background-color: transparent; border: none; font-size: 36px;")
        self.signup_peek_button_pwd1.setMaximumWidth(50)
        self.signup_peek_button_pwd1.clicked.connect(self.signup_peek_password_pw1_func)

        self.signup_password_layout_1.addWidget(self.signup_password_input)
        self.signup_password_layout_1.addWidget(self.signup_peek_button_pwd1)

        self.signup_password_layout_2 = QHBoxLayout()

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm Password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet(self.get_input_style())
        self.confirm_password_input.setMaximumWidth(500)

        self.signup_peek_button_pwd2 = QPushButton("😎")
        self.signup_peek_button_pwd2.setStyleSheet("background-color: transparent; border: none; font-size: 36px;")
        self.signup_peek_button_pwd2.setMaximumWidth(50)
        self.signup_peek_button_pwd2.clicked.connect(self.signup_peek_password_pw2_func)

        self.signup_password_layout_2.addWidget(self.confirm_password_input)
        self.signup_password_layout_2.addWidget(self.signup_peek_button_pwd2)

        input_layout.addLayout(self.signup_password_layout_1)
        input_layout.addLayout(self.signup_password_layout_2)
        input_layout.setAlignment(Qt.AlignCenter)

        main_layout.addLayout(input_layout)

        # Signup buttons
        button_layout = QHBoxLayout()
        self.login_button_signup = QPushButton("Already have an account? Login!")
        self.signup_button_signup = QPushButton("Sign Up")

        self.login_button_signup.setStyleSheet(self.get_button_style())
        self.signup_button_signup.setStyleSheet(self.get_button_style())

        self.login_button_signup.clicked.connect(self.show_login_page)
        self.signup_button_signup.clicked.connect(self.signup)

        button_layout.addWidget(self.login_button_signup)
        button_layout.addWidget(self.signup_button_signup)
        button_layout.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(button_layout)

        # Theme changer button
        self.theme_changer_signup = QPushButton("Change to Light Theme" if self.dark_mode else "Change to Dark Theme")
        self.theme_changer_signup.clicked.connect(self.toggle_theme_signup)
        self.theme_changer_signup.setStyleSheet(self.get_theme_button_style())
        main_layout.addWidget(self.theme_changer_signup, alignment=Qt.AlignRight | Qt.AlignBottom)

        self.stacked_widget.addWidget(self.signup_page)

        # check the focus of username field
        # then if entered in clicked, focus on password
        self.signup_username_input.returnPressed.connect(self.signup_user_email_input.setFocus)
        self.signup_user_email_input.returnPressed.connect(self.fname_input.setFocus)
        self.fname_input.returnPressed.connect(self.lname_input.setFocus)
        self.lname_input.returnPressed.connect(self.licence_input.setFocus)
        self.licence_input.returnPressed.connect(self.signup_password_input.setFocus)
        self.signup_password_input.returnPressed.connect(self.confirm_password_input.setFocus)
        self.confirm_password_input.returnPressed.connect(self.signup)

        # Override keyPressEvent for up and down arrow navigation
        self.override_keyPressEvent(self.signup_username_input)
        self.override_keyPressEvent(self.signup_user_email_input)

        self.override_keyPressEvent(self.fname_input)
        self.override_keyPressEvent(self.lname_input)
        self.override_keyPressEvent(self.licence_input)

        self.override_keyPressEvent(self.signup_password_input)
        self.override_keyPressEvent(self.confirm_password_input)


    def override_keyPressEvent(self, widget):
        original_keyPressEvent = widget.keyPressEvent

        def custom_keyPressEvent(event):
            if event.key() == Qt.Key_Up:
                # login page
                if widget == self.password_input:
                    self.username_input.setFocus()
                elif widget == self.username_input:
                    self.password_input.setFocus()

                # signup page
                if widget == self.confirm_password_input:
                    self.signup_password_input.setFocus()
                elif widget == self.signup_password_input:
                    self.licence_input.setFocus()
                elif widget == self.licence_input:
                    self.lname_input.setFocus()
                elif widget == self.lname_input:
                    self.fname_input.setFocus()
                elif widget == self.fname_input:
                    self.signup_user_email_input.setFocus()
                elif widget == self.signup_user_email_input:
                    self.signup_username_input.setFocus()
                elif widget == self.signup_username_input:
                    self.confirm_password_input.setFocus()

            elif event.key() == Qt.Key_Down:
                # login page
                if widget == self.username_input:
                    self.password_input.setFocus()
                elif widget == self.password_input:
                    self.username_input.setFocus()

                # signup page
                if widget == self.signup_username_input:
                    self.signup_user_email_input.setFocus()
                elif widget == self.signup_user_email_input:
                    self.fname_input.setFocus()
                elif widget == self.fname_input:
                    self.lname_input.setFocus()
                elif widget == self.lname_input:
                    self.licence_input.setFocus()
                elif widget == self.licence_input:
                    self.signup_password_input.setFocus()
                elif widget == self.signup_password_input:
                    self.confirm_password_input.setFocus()
                elif widget == self.confirm_password_input:
                    self.signup_username_input.setFocus()
            else:
                # Call the original keyPressEvent for default behavior
                original_keyPressEvent(event)

        # Replace the keyPressEvent method with the custom one
        widget.keyPressEvent = custom_keyPressEvent


    def signup_peek_password_pw1_func(self):
        if self.signup_password_input.echoMode() == QLineEdit.Password:
            self.signup_password_input.setEchoMode(QLineEdit.Normal)
            self.signup_peek_button_pwd1.setText("🙂")
        else:
            self.signup_password_input.setEchoMode(QLineEdit.Password)
            self.signup_peek_button_pwd1.setText("😎")
        pass

    def signup_peek_password_pw2_func(self):
        if self.confirm_password_input.echoMode() == QLineEdit.Password:
            self.confirm_password_input.setEchoMode(QLineEdit.Normal)
            self.signup_peek_button_pwd2.setText("🙂")
        else:
            self.confirm_password_input.setEchoMode(QLineEdit.Password)
            self.signup_peek_button_pwd2.setText("😎")
        pass

    def peek_password(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.peek_button.setText("🙂")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.peek_button.setText("😎")

    def toggle_theme_login(self):
        self.dark_mode = not self.dark_mode
        self.set_theme()
        self.theme_changer_login.setStyleSheet(self.get_theme_button_style())
        self.theme_changer_login.setText("Change to Light Theme" if self.dark_mode else "Change to Dark Theme")

        self.implement_themes()

    def toggle_theme_signup(self):
        self.dark_mode = not self.dark_mode
        self.set_theme()
        self.theme_changer_signup.setStyleSheet(self.get_theme_button_style())
        self.theme_changer_signup.setText("Change to Light Theme" if self.dark_mode else "Change to Dark Theme")

        self.implement_themes()


    def set_theme(self):
        if self.dark_mode:
            self.set_dark_mode()
        else:
            QApplication.instance().setPalette(QApplication.instance().style().standardPalette())

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

    def get_username(self):
        return self.username_input.text()

    def get_password(self):
        return self.password_input.text()

    def check_user_credentials_for_login(self):
        from API.DatabaseAPI.client_database_connection import check_username_existence, get_details, authenticate
        from .utils import get_current_system_path, change_path_to_db
        username = self.get_username()
        password = self.get_password()

        print(f"Username: {username}, Password: {password}")

        if len(username) == 0 or len(password) == 0:
            dialog = ErrorDialog("Please enter username and password!")
            dialog.exec_()
        else:
            PATH_ = get_current_system_path()
            dbPATH_ = change_path_to_db(PATH_)

            print("PATH:", PATH_)
            print("dbPATH:", dbPATH_)

            data = check_username_existence(username, dbPATH_)
            if data["status"] == "success":
                data_auth = authenticate(username, password, dbPATH_)
                if data_auth["status"] == "success":
                    showinfo("Success", f"User {username} authenticated successfully!")
                    user_data = get_details(username, dbPATH_)

                    self.close()

                    from Screens.builds.MainPage_13 import MainPage_13  # Temporary

                    self.main_page = MainPage_13(username)  # Temporary
                    self.main_page.show()
                elif data_auth["status"] == "error":
                    dialog = ErrorDialog(data_auth["message"])
                    dialog.exec_()
            elif data["status"] == "error":
                dialog = ErrorDialog(data["message"])
                dialog.exec_()

    def show_signup_page(self):
        # Switch to signup page
        self.stacked_widget.setCurrentWidget(self.signup_page)
        self.signup_username_input.setFocus()

    def show_login_page(self):
        # Switch to login page
        self.stacked_widget.setCurrentWidget(self.login_page)
        self.username_input.setFocus()

    def signup(self):
        from API.DatabaseAPI.client_database_connection import register_user, check_username_uniqueness, check_email_uniqueness, check_licence_uniqueness
        from Main.utils import get_current_system_path, change_path_to_db

        PATH_ = get_current_system_path()
        print("PATH:", PATH_)

        dbPATH_ = change_path_to_db(PATH_)
        print("dbPATH:", dbPATH_)

        # Logic to handle signup
        print("Signup logic BETA implemented")
        username = self.signup_username_input.text()
        email = self.signup_user_email_input.text()
        password = self.signup_password_input.text()
        confirm_password = self.confirm_password_input.text()

        fname = self.fname_input.text()
        lname = self.lname_input.text()
        specialization = self.specialization_input.currentText()
        licence = self.licence_input.text()

        print(f"Username: {username}, Email: {email}, Password: {password}, Confirm Password: {confirm_password}")
        print(f"First Name: {fname}, Last Name: {lname}, Specialization: {specialization}, Licence: {licence}")
        if len(username) == 0 or len(email) == 0 or len(password) == 0 or len(confirm_password) == 0 or len(fname) == 0 or len(lname) == 0 or len(specialization) == 0 or len(licence) == 0:
            dialog = ErrorDialog("Please enter all details!")
            dialog.exec_()
        else:
            if check_username_uniqueness(username, dbPATH_) and check_licence_uniqueness(licence, dbPATH_) and check_email_uniqueness(email, dbPATH_) and password == confirm_password:
                print("Signup logic to be implemented -- 1")
                result = register_user(username=username, email=email, password=password, first_name=fname, last_name=lname, specialization=specialization, licence=licence, PATH_=dbPATH_) # edit
                if result["boolean"] and result["status"] == "success":
                    showinfo("Success", f"User {username} added successfully!")
                    self.show_login_page()
                else:
                    dialog = ErrorDialog(result["message"])
                    dialog.exec_()

    def implement_themes(self):
        if type(self.login_button_signup) == QPushButton:
            self.login_button_signup.setStyleSheet(self.get_button_style())
        if type(self.signup_button_signup) == QPushButton:
            self.signup_button_signup.setStyleSheet(self.get_button_style())
        if type(self.signup_username_input) == QLineEdit:
            self.signup_username_input.setStyleSheet(self.get_input_style() + "margin-top: 30px;")
        if type(self.signup_password_input) == QLineEdit:
            self.signup_password_input.setStyleSheet(self.get_input_style())
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
        if type(self.confirm_password_input) == QLineEdit:
            self.confirm_password_input.setStyleSheet(self.get_input_style())
        if type(self.signup_user_email_input) == QLineEdit:
            self.signup_user_email_input.setStyleSheet(self.get_input_style() + "margin-bottom: 20px;")
        pass

    def show_main_page(self, username):
        # Switch to main page
        self.stacked_widget.setCurrentWidget(self.main_page)
        pass


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # show error messages as well
    sys.exit(app.exec_())
