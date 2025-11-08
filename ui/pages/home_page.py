# FINAL PROJECT FLASHCARD APP / ui / pages / home_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from utils.path_helper import get_asset_path

# Styles
from ui.visual.styles.styles import home_page_styles 


class HomePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.btn_styles = home_page_styles()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        self.setLayout(layout)
        
        # Add some stretch at the top
        layout.addStretch()
        
        
        image_label = QLabel()
        image_path = get_asset_path("WelcomeLogo.png")  
        pixmap = QPixmap(image_path)
        
        # RESPONSIVE IMAGE SCALING - 25% of screen width
        if self.main_window:
            screen = self.main_window.screen()
            screen_size = screen.availableGeometry()
            image_width = int(screen_size.width() * 0.25)
            image_height = int(image_width * 0.5)  # Maintain 2:1 aspect ratio
        else:
            image_width = 600
            image_height = 300
            
        pixmap = pixmap.scaled(image_width, image_height, Qt.AspectRatioMode.KeepAspectRatio)
        
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image_label)
        
        # Add buttons
        self.existing_flashcard_btn = QPushButton("Existing Flashcard")
        self.existing_flashcard_btn.setMinimumHeight(50)  # CHANGED: setFixedHeight -> setMinimumHeight
        self.existing_flashcard_btn.clicked.connect(self.main_window.show_existing_flashcards)
        self.existing_flashcard_btn.setStyleSheet(self.btn_styles["home_button"])  # APPLY STYLE
        layout.addWidget(self.existing_flashcard_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.create_flashcard_btn = QPushButton("Create Flashcard")
        self.create_flashcard_btn.setMinimumHeight(50)  # CHANGED: setFixedHeight -> setMinimumHeight
        self.create_flashcard_btn.clicked.connect(self.main_window.show_create_flashcard)
        self.create_flashcard_btn.setStyleSheet(self.btn_styles["home_button"])  # APPLY STYLE
        layout.addWidget(self.create_flashcard_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add stretch at the bottom
        layout.addStretch()