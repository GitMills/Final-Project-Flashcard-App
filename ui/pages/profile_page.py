# ui/pages/profile_page.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QLineEdit, QFormLayout, QSpinBox
)
from ui.visual.styles.styles import get_profile_page_styles  # Added

class ProfilePage(QWidget):
    def __init__(self, parent=None, switch_account_callback=None):
        super().__init__(parent)

        # Load and apply profile page styles from styles.py
        self.styles = get_profile_page_styles()
        self.setStyleSheet(self.styles["page"])

        self.switch_account_callback = switch_account_callback
        self.username = None
        self.setup_ui()
    
    def setup_ui(self):
        self.layout = QVBoxLayout()
        
        self.title = QLabel("<h1>Profile Settings</h1>")
        self.user_label = QLabel("")  # will show the logged-in user
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.age_spinbox = QSpinBox()
        self.save_btn = QPushButton("Save Profile")
        self.switch_btn = QPushButton("Switch Account")
        self.switch_btn.clicked.connect(self.confirm_switch)

        # apply the color/text styles from styles.py
        self.title.setStyleSheet(self.styles["title"])
        self.user_label.setStyleSheet(self.styles["label"])
        self.name_input.setStyleSheet(self.styles["input"])
        self.email_input.setStyleSheet(self.styles["input"])
        self.save_btn.setStyleSheet(self.styles["button"])
        self.switch_btn.setStyleSheet(self.styles["switch_button"])

        # Setup form layout
        form_layout = QFormLayout()
        self.name_input.setPlaceholderText("Enter your name")
        self.email_input.setPlaceholderText("Enter your email")
        self.age_spinbox.setRange(1, 100)
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Age:", self.age_spinbox)
        form_layout.addRow("", self.save_btn)

        # Assemble main layout
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.user_label)
        self.layout.addLayout(form_layout)
        self.layout.addWidget(self.switch_btn)
        self.layout.addStretch()
        self.setLayout(self.layout)
        
    def confirm_switch(self):
        """Ask for confirmation before switching accounts."""
        from PyQt6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to switch accounts?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            if callable(self.switch_account_callback):
                self.switch_account_callback()
            
    def save_profile(self):
        """Save profile information to a local JSON file."""
        import json, os
        profile_data = {
            "full_name": self.name_input.text(),
            "email": self.email_input.text(),
            "age": self.age_spinbox.value()
        }

        path = "user_profiles.json"
        all_data = {}
        if os.path.exists(path):
            with open(path, "r") as f:
                all_data = json.load(f)

        all_data[self.username or "unknown"] = profile_data
        with open(path, "w") as f:
            json.dump(all_data, f, indent=4)
        print(f"✅ Saved profile for {self.username or 'unknown'}")

    def load_profile(self, username, full_name):
        """Pre-fill name and display current logged-in user."""
        import json, os
        self.username = username
        self.user_label.setText(f"Logged in as: {full_name} ({username})")

        path = "user_profiles.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                all_profiles = json.load(f)
            profile = all_profiles.get(username, {})
            self.name_input.setText(profile.get("full_name", full_name))
            self.email_input.setText(profile.get("email", ""))
            self.age_spinbox.setValue(profile.get("age", 0))
        else:
            self.name_input.setText(full_name)
            self.email_input.clear()
            self.age_spinbox.setValue(0)
            
    def switch_account(self):
        """Go to the Accounts Page."""
        if callable(self.switch_account_callback):
            self.switch_account_callback()
        else:
            print("⚠️ switch_account_callback not set in ProfilePage")
