# FINAL PROJECT FLASHCARD APP / ui / pages / help_page.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class HelpPage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.current_step = 0
        self.setup_ui()
        self.update_tutorial_step()

    def setup_ui(self):
        """Set up the simple help & tutorial layout."""
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # === Title ===
        title = QLabel("📘 Help & Tutorial")
        title.setFont(QFont("Arial Rounded MT Bold", 28))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #434190; font-weight: bold; letter-spacing: 1px;")
        main_layout.addWidget(title)

        # === Scrollable area (for tutorial steps) ===
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        self.scroll_layout = QVBoxLayout(content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.setSpacing(15)

        # Tutorial labels
        self.tutorial_title = QLabel()
        self.tutorial_title.setFont(QFont("Arial Rounded MT Bold", 22))
        self.tutorial_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tutorial_title.setStyleSheet("color: #434190; font-weight: bold;")

        self.tutorial_desc = QLabel()
        self.tutorial_desc.setWordWrap(True)
        self.tutorial_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tutorial_desc.setFont(QFont("Arial", 13))
        self.tutorial_desc.setStyleSheet("color: #555; padding: 0 40px;")

        self.scroll_layout.addStretch()
        self.scroll_layout.addWidget(self.tutorial_title)
        self.scroll_layout.addWidget(self.tutorial_desc)
        self.scroll_layout.addStretch()

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        # === Navigation Buttons ===
        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.next_btn = QPushButton("Next ➜")
        self.next_btn.setFont(QFont("Arial Rounded MT Bold", 14))
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #434190;
                color: white;
                padding: 8px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #6366F1;
            }
        """)
        self.next_btn.clicked.connect(self.next_step)
        btn_layout.addWidget(self.next_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.back_btn = QPushButton("⬅ Back to Home")
        self.back_btn.setFont(QFont("Arial Rounded MT Bold", 14))
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #888;
                color: white;
                padding: 8px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        self.back_btn.clicked.connect(self.go_back_to_home)
        btn_layout.addWidget(self.back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

        # Background color
        self.setStyleSheet("background-color: #FFF6E9;")

    def update_tutorial_step(self):
        """Update tutorial content based on the current step (from WelcomePage logic)."""
        steps = [
            {
                "title": "Adding Flashcards",
                "desc": (
                    "Click the <b>'Create Flashcard'</b> button in the main screen to add a new flashcard.<br>"
                    "Type your question and answer, then click <b>Save Flashcard</b> to store it."
                )
            },
            {
                "title": "Navigating the App",
                "desc": (
                    "Use the sidebar ☰ to explore different areas:<br>"
                    "🏠 Home – See your flashcards<br>"
                    "📚 Topics – Choose subjects to study<br>"
                    "✏️ Create – Make your own cards<br>"
                    "💾 Saved – Review what you've created"
                )
            },
            {
                "title": "Using Existing Flashcards",
                "desc": (
                    "Select a topic (like English, Math, or Science) to begin studying.<br>"
                    "Click any flashcard to flip it and reveal the answer."
                )
            }
        ]

        step = steps[self.current_step]
        self.tutorial_title.setText(step["title"])
        self.tutorial_desc.setText(step["desc"])

        # Update button text
        if self.current_step < len(steps) - 1:
            self.next_btn.setText("Next ➜")
        else:
            self.next_btn.setText("Finish ✅")

    def next_step(self):
        """Advance to next tutorial step or go back."""
        self.current_step += 1
        if self.current_step < 3:
            self.update_tutorial_step()
        else:
            # Return to home page when done
            self.go_back_to_home()
    
    def go_back_to_home(self):
        """Navigate back to home page"""
        if self.main_window and hasattr(self.main_window, 'show_page'):
            self.main_window.show_page(0)  # Go to home page (index 0)
    
    def reset_tutorial(self):
        """Reset tutorial to the first step"""
        self.current_step = 0
        self.update_tutorial_step()
    
    def showEvent(self, event):
        """Called when the page is shown - reset to first step"""
        super().showEvent(event)
        self.reset_tutorial()
