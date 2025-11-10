#ui/pages/welcome_page.py #jose

from PyQt6.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel,
    QLineEdit, QMessageBox
    )
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QPixmap
from ui.visual.styles.styles import ( 
    APP_STYLE, APP_STYLE_LIGHT, APP_STYLE_DARK, FONT_SUBTITLE, FONT_LARGE_BOLD,
    FONT_MEDIUM, FONT_BUTTON, FONT_LABEL, MESSAGE_WARNING
    )
from ui.visual.animations import FadeWidget
from data.user_and_theme import AppData
from utils.path_helper import get_asset_path

class WelcomePage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.data = AppData()
        self.app = app
        self.apply_theme()
        
        self.setWindowTitle("Remora App Flow")
        self.setStyleSheet(APP_STYLE)
        self.setWindowIcon(QIcon(get_asset_path("AppIcon.png")))
        
        self.theme_btn = QPushButton("🌙")
        self.theme_btn.clicked.connect(self.toggle_btn)
        
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(self.theme_btn)
        
        self.stacked = QStackedWidget()
        
        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.stacked)
        self.setLayout(layout)
        
        # Pages
        self.start_page = FadeWidget(self.create_start_page(), self)
        self.name_page = FadeWidget(self.create_name_page(), self)
        self.greet_page = FadeWidget(QLabel(alignment=Qt.AlignmentFlag.AlignCenter), self)
        self.greet_page.widget.setFont(FONT_MEDIUM)
        self.welcome_page = FadeWidget(self.create_welcome_page(), self)
        self.ask_page = FadeWidget(self.create_ask_page(), self)
        
        self.main_page = FadeWidget(QWidget(), self)
        
        self.tutorial_page = FadeWidget(self.create_tutorial_page(), self)
        self.current_tutorial_step = 0  # track which tutorial slide we're on

        self.welcome_back_page = FadeWidget(QLabel(alignment=Qt.AlignmentFlag.AlignCenter), self)
        self.welcome_back_page.widget.setFont(FONT_MEDIUM)

        for page in [self.start_page, self.name_page, self.greet_page, self.welcome_page, self.ask_page, self.main_page]:
            self.stacked.addWidget(page)
            
        self.stacked.addWidget(self.tutorial_page)
        self.stacked.addWidget(self.welcome_back_page)
        
        # Connections
        self.start_btn.clicked.connect(lambda: self.start_page.fade_out(self.name_page))
        self.submit_name_btn.clicked.connect(self.show_greet)
        
        self.yes_btn.clicked.connect(self.show_tutorial)
        self.no_btn.clicked.connect(self.show_welcome_back)

        # Start page
        self.stacked.setCurrentWidget(self.start_page)
        self.start_page.fade_in()

        # Apply default theme
        self.apply_theme()
        
    def toggle_btn(self):
        """Switch between light and dark themes."""
        self.data.theme = "dark" if self.data.theme == "light" else "light"
        self.apply_theme()
        self.theme_btn.setText("☀️" if self.data.theme == "dark" else "🌙")

    def apply_theme(self):
        if self.data.theme == "dark":
            self.setStyleSheet(APP_STYLE_DARK)
        else:
            self.setStyleSheet(APP_STYLE_LIGHT)
            
        for page_name in [
            "main_page", "topics_page", "create_flashcard_page",
            "saved_flashcards_page", "existing_flashcard_page"
        ]:
            if hasattr(self, page_name):
                getattr(self, page_name).setStyleSheet(
                    APP_STYLE_DARK if self.data.theme == "dark" else APP_STYLE_LIGHT
                )
            
    def toggle_theme(self):
        if self.data.theme == "light":
            self.data.theme = "dark"
        else:
            self.data.theme = "light"
    
        self.apply_theme()

    def create_start_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        pixmap = QPixmap(get_asset_path("AppIcon.png"))
        pixmap = pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        logo = QLabel()
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("READY WHEN YOU ARE!")
        subtitle.setFont(FONT_SUBTITLE)
        subtitle.setStyleSheet("color: #FC483D; letter-spacing: 2px; font-weight: 900;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.start_btn = QPushButton("BEGIN")
        self.start_btn.setFont(FONT_LARGE_BOLD)
        
        layout.addStretch()
        layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(subtitle, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        return widget

    def create_name_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.name_label = QLabel("ENTER YOUR NAME")
        self.name_label.setFont(FONT_SUBTITLE)
        self.name_label.setStyleSheet("color: #434190")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Type it here...")
        
        self.name_input.repaint()
        self.name_input.setFont(FONT_SUBTITLE)
        
        self.submit_name_btn = QPushButton("Next")
        self.submit_name_btn.setFont(FONT_BUTTON)
        self.name_input.returnPressed.connect(self.show_greet)
        
        layout.addStretch()
        layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_input, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(15)
        layout.addWidget(self.submit_name_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        return widget

    def create_ask_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.ask_label = QLabel("New here?")
        self.ask_label.setFont(FONT_LABEL)
        self.ask_label.setStyleSheet("color: #434190")
        self.ask_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.yes_btn = QPushButton("Yes")
        self.no_btn = QPushButton("No")
        self.yes_btn.setFont(FONT_BUTTON)
        self.no_btn.setFont(FONT_BUTTON)
        layout.addStretch()
        layout.addWidget(self.ask_label)
        layout.addWidget(self.yes_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.no_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        return widget
    
    def create_tutorial_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
    
        self.tutorial_title = QLabel()
        self.tutorial_title.setFont(FONT_LARGE_BOLD)
        self.tutorial_title.setStyleSheet("color: #434190; font-weight: bold;")
        self.tutorial_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        self.tutorial_desc = QLabel()
        self.tutorial_desc.setFont(FONT_LABEL)
        self.tutorial_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tutorial_desc.setWordWrap(True)
        self.tutorial_desc.setStyleSheet("color: #555;")
    
        self.next_btn = QPushButton("Next ➜")
        self.next_btn.setFont(FONT_BUTTON)
        self.next_btn.clicked.connect(self.next_tutorial_step)
        
        self.skip_btn = QPushButton("Skip Tutorial ⏭️")
        self.skip_btn.setFont(FONT_BUTTON)
        self.skip_btn.clicked.connect(lambda: self.tutorial_page.fade_out(None, on_finish=self.app.show_main_window))
        self.tutorial_desc.setStyleSheet("color: #555; padding: 0 40px;")
        
        layout.addStretch()
        layout.addWidget(self.tutorial_title)
        layout.addWidget(self.tutorial_desc)
        layout.addSpacing(20)
        layout.addWidget(self.next_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.skip_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
    
        return widget

    def show_tutorial(self):
        self.current_tutorial_step = 0
        self.ask_page.fade_out(self.tutorial_page)
        self.update_tutorial_step()
        
    def update_tutorial_step(self):
        """Update tutorial content based on current step"""
        steps = [
            {
                "title": "Adding Flashcards",
                "desc": "Click the '+' button or 'Add Flashcard' in the main screen to create a new flashcard.\nYou can enter a question, an answer, and save it instantly."
            },
            {
                "title": "Navigating the App",
                "desc": "Use the sidebar ☰ to explore:\n🏠 Home – View your flashcards\n👤 Profile – Check your info\n⚙️ Settings – Customize your theme\n📊 Statistics – See your study progress."
            },
            {
                "title": "Using Existing Flashcards",
                "desc": "Select any flashcard to study. Flip the card to see the answer and mark if you got it right or wrong. Remora tracks your progress automatically!"
            }
        ]
    
        # Update content
        step = steps[self.current_tutorial_step]
        self.tutorial_title.setText(step["title"])
        self.tutorial_desc.setText(step["desc"])
    
        # Update button text
        if self.current_tutorial_step < len(steps) - 1:
            self.next_btn.setText("Next ➜")
        else:
            self.next_btn.setText("Finish ✅")

    def next_tutorial_step(self):
        """Handle next step or finish tutorial"""
        self.current_tutorial_step += 1
        if self.current_tutorial_step < 3:
            self.update_tutorial_step()
        else:
            # End tutorial and go to main page
            self.tutorial_page.fade_out(None, on_finish=self.app.show_main_window)

    def show_welcome_back(self):
        """Show personalized welcome back message before main content"""
        name = self.data.username or "User"
        self.welcome_back_page.widget.setText(f"Welcome back, {name}!")
        self.welcome_back_page.widget.setStyleSheet("color: #434190; font-weight: bold;")

        # Fade out 'ask_page' and fade in the welcome-back page
        self.ask_page.fade_out(self.welcome_back_page)

        # After 1.5 seconds, fade out welcome-back and show main window
        QTimer.singleShot(1500, lambda: self.welcome_back_page.fade_out(None, on_finish=self.app.show_main_window))

        
    def show_greet(self):
        name = self.name_input.text().strip()
        
        if not name:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Missing Name")
            msg.setFont(FONT_SUBTITLE)
            msg.setWindowIcon(QIcon(get_asset_path("!.png")))
            msg.setText("Enter your name before continuing.")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.setStyleSheet(MESSAGE_WARNING)
            msg.exec()
            return
    
        self.data.username = name
        self.greet_page.widget.setText(f"Hi, {name}!")
        self.greet_page.widget.setStyleSheet("color: #434190")
        self.name_page.fade_out(self.greet_page)
        QTimer.singleShot(1000, lambda: self.show_welcome())
        
    def create_welcome_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        pixmap = QPixmap(get_asset_path("AppIcon.png"))
        pixmap = pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        logo = QLabel()
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("WELCOME!")
        title.setFont(FONT_LARGE_BOLD)
        title.setStyleSheet("color: #FC483D; font-weight: 900; letter-spacing: 2px;")
        
        subtitle = QLabel("Remora is a flashcard for students")
        subtitle.setFont(FONT_LABEL)
        subtitle.setStyleSheet("color: #A0522D; font-weight: bold;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch()
        layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(subtitle, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        return widget
    
    def show_welcome(self):
        self.greet_page.fade_out(self.welcome_page)
        QTimer.singleShot(1500, lambda: self.welcome_page.fade_out(self.ask_page))