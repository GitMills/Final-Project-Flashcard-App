# FINAL PROJECT FLASHCARD APP / ui / pages / profile_page.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QLineEdit, QFormLayout, QSpinBox
)

class ProfilePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("<h1>Profile Settings</h1>")
        
        # Form layout
        form_layout = QFormLayout()
        
        # Form fields
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter yours name")
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        
        self.age_spinbox = QSpinBox()
        self.age_spinbox.setRange(1, 100)
        
        self.save_btn = QPushButton("Save Profile")
        
        # Add to form
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Age:", self.age_spinbox)
        form_layout.addRow("", self.save_btn)
        
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def save_profile_data(self):
        # You can access the form data like this:
        name = self.name_input.text()
        email = self.email_input.text()
        age = self.age_spinbox.value()