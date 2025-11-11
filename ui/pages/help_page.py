# FINAL PROJECT FLASHCARD APP / ui / pages / help_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class HelpPage(QWidget):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window  # optional for navigation
        self.setup_ui()
    
    def setup_ui(self):
        # === Base Layout ===
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)

        # === Title ===
        title = QLabel("📘 Help & Support")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial Rounded MT Bold", 32))
        title.setStyleSheet("color: #434190; letter-spacing: 2px; font-weight: bold;")
        main_layout.addWidget(title)

        # === Scrollable Help Text ===
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #FFF6E9;
            }
        """)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setSpacing(20)

        # === Section: Getting Started ===
        intro = QLabel(
            "<h2>🚀 Getting Started</h2>"
            "<p>Welcome to <b>Remora</b> — your study companion that helps you learn faster using flashcards!</p>"
            "<p>When you first open the app, you'll be guided through setup and an optional tutorial explaining key features.</p>"
        )
        intro.setWordWrap(True)
        intro.setStyleSheet("color: #333; font-size: 15px;")
        content_layout.addWidget(intro)

        # === Section: Creating Flashcards ===
        create = QLabel(
            "<h2>✏️ Creating Flashcards</h2>"
            "<ul>"
            "<li>Click <b>'Create Flashcard'</b> on the main page.</li>"
            "<li>Type your question and answer, then click <b>Save Flashcard</b>.</li>"
            "<li>Your flashcards will be saved under <b>'Saved Flashcards'</b>.</li>"
            "</ul>"
        )
        create.setWordWrap(True)
        create.setStyleSheet("color: #333; font-size: 15px;")
        content_layout.addWidget(create)

        # === Section: Studying Flashcards ===
        study = QLabel(
            "<h2>📚 Studying Flashcards</h2>"
            "<ul>"
            "<li>Choose <b>'Existing Flashcards'</b> to review pre-made topics.</li>"
            "<li>Click on any topic (English, Math, Science, etc.) to start.</li>"
            "<li>Click on a card to <b>flip</b> and reveal the answer.</li>"
            "</ul>"
        )
        study.setWordWrap(True)
        study.setStyleSheet("color: #333; font-size: 15px;")
        content_layout.addWidget(study)

        # === Section: Saved Flashcards ===
        saved = QLabel(
            "<h2>💾 Viewing Saved Flashcards</h2>"
            "<p>All flashcards you create are available in the <b>Saved Flashcards</b> section."
            " You can review them at any time — just click on a card to flip it and test yourself!</p>"
        )
        saved.setWordWrap(True)
        saved.setStyleSheet("color: #333; font-size: 15px;")
        content_layout.addWidget(saved)

        # === Section: Keyboard Shortcuts ===
        shortcuts = QLabel(
            "<h2>⌨️ Keyboard Shortcuts</h2>"
            "<table style='border-collapse: collapse;'>"
            "<tr><td style='padding:4px 12px;'><b>Ctrl + Q</b></td><td>Quit the app</td></tr>"
            "<tr><td style='padding:4px 12px;'><b>Ctrl + S</b></td><td>Save data</td></tr>"
            "<tr><td style='padding:4px 12px;'><b>Ctrl + F</b></td><td>Open flashcard section</td></tr>"
            "<tr><td style='padding:4px 12px;'><b>Spacebar</b></td><td>Flip a flashcard</td></tr>"
            "<tr><td style='padding:4px 12px;'><b>Ctrl + Enter</b></td><td>Save flashcard in 'Create' page</td></tr>"
            "<tr><td style='padding:4px 12px;'><b>F1</b></td><td>Open this Help page</td></tr>"
            "</table>"
        )
        shortcuts.setWordWrap(True)
        shortcuts.setStyleSheet("color: #333; font-size: 15px;")
        content_layout.addWidget(shortcuts)

        # === Section: Theme Customization ===
        theme = QLabel(
            "<h2>🌙 Themes</h2>"
            "<p>You can switch between <b>Light</b> and <b>Dark</b> mode anytime by clicking the "
            "theme toggle button (<b>☀️ / 🌙</b>) at the top-right corner.</p>"
        )
        theme.setWordWrap(True)
        theme.setStyleSheet("color: #333; font-size: 15px;")
        content_layout.addWidget(theme)

        # === Section: Need Help? ===
        contact = QLabel(
            "<h2>📩 Need More Help?</h2>"
            "<p>If something doesn’t work or you’d like to suggest a feature, "
            "feel free to contact the Remora development team.</p>"
            "<p style='color:#434190; font-weight:bold;'>Email: remora.support@example.com</p>"
        )
        contact.setWordWrap(True)
        contact.setStyleSheet("color: #333; font-size: 15px;")
        content_layout.addWidget(contact)

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # === Back Button ===
        back_btn = QPushButton("⬅ Back to Main")
        back_btn.setFont(QFont("Arial Rounded MT Bold", 14))
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #888;
                color: white;
                border-radius: 10px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        if self.parent_window:
            back_btn.clicked.connect(lambda: self.parent_window.help_page.fade_out(self.parent_window.main_page))
        main_layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # === Background ===
        self.setStyleSheet("background-color: #FFF6E9;")
