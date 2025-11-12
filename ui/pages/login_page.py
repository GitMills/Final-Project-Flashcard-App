# ui/pages/login_page.py
import os, json, hashlib
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt

PROFILE_PATH = "user_profiles.json"  # renamed to support multiple users

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class LoginPage(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.is_creating_account = False
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        # Titles
        self.title = QLabel("LOG IN")
        self.title.setStyleSheet("font-size: 28px; color: #434190; font-weight: bold;")
        self.subtitle = QLabel("Welcome to Remora! Please log in or create an account.")
        self.subtitle.setStyleSheet("color: #555; font-size: 14px;")

        # Inputs
        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Name")
        self.fullname_input.setFixedWidth(250)
        self.fullname_input.hide()  # only show in create mode
        self.fullname_input.returnPressed.connect(self.handle_action)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedWidth(250)
        self.username_input.returnPressed.connect(self.handle_action)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedWidth(250)
        self.password_input.returnPressed.connect(self.handle_action)

        # Buttons
        self.login_btn = QPushButton("Login")
        self.login_btn.setFixedWidth(200)
        self.login_btn.setStyleSheet("padding: 10px; font-weight: bold; background-color: #FC483D; color: white; border-radius: 8px;")
        self.login_btn.clicked.connect(self.handle_action)

        self.switch_mode_btn = QPushButton("Create Account")
        self.switch_mode_btn.setStyleSheet("background: none; color: #555; text-decoration: underline; border: none;")
        self.switch_mode_btn.clicked.connect(self.toggle_mode)

        # Layout
        self.layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.subtitle, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.fullname_input, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.username_input, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addSpacing(15)
        self.layout.addWidget(self.login_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.switch_mode_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def toggle_mode(self):
        """Switch between Login and Create Account modes."""
        self.is_creating_account = not self.is_creating_account
        if self.is_creating_account:
            self.title.setText("CREATE ACCOUNT")
            self.login_btn.setText("Register")
            self.switch_mode_btn.setText("Back to Login")
            self.fullname_input.show()
        else:
            self.title.setText("LOG IN")
            self.login_btn.setText("Login")
            self.switch_mode_btn.setText("Create Account")
            self.fullname_input.hide()
            
    def reset_fields(self):
        """Clear input fields and reset to login mode."""
        self.username_input.clear()
        self.password_input.clear()
        self.fullname_input.clear()
        self.fullname_input.hide()
        self.is_creating_account = False
        self.title.setText("LOG IN")
        self.login_btn.setText("Login")
        self.switch_mode_btn.setText("Create Account")

    def handle_action(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Missing Info", "Please fill in all required fields.")
            return

        # Load or create user data
        if os.path.exists(PROFILE_PATH):
            with open(PROFILE_PATH, "r") as f:
                data = json.load(f)
        else:
            data = {}

        if self.is_creating_account:
            # Create account
            if username in data:
                QMessageBox.warning(self, "Error", "Username already exists.")
                return

            full_name = self.fullname_input.text().strip() or username
            data[username] = {
                "full_name": full_name,
                "password": hash_password(password)
            }

            with open(PROFILE_PATH, "w") as f:
                json.dump(data, f, indent=4)

            # Reset to login mode after successful registration
            self.reset_fields()
            self.toggle_mode()  # Switch back to login mode

        else:
            # Login
            if username not in data or data[username]["password"] != hash_password(password):
                QMessageBox.critical(self, "Login Failed", "Invalid username or password.")
                return

            full_name = data[username]["full_name"]
            self.on_login_success(username, is_new=False)
