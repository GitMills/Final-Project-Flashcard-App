# FINAL PROJECT FLASHCARD APP / ui / pages / existing_flashcard_page.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QHBoxLayout,
    QProgressBar, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from PyQt6.QtGui import QFont, QIcon, QPixmap
from random import shuffle

from ui.visual.styles.styles import get_existing_flashcard_styles
from utils.path_helper import get_asset_path


class FlashcardWidget(QFrame):
    """Single clickable flashcard that flips between question and answer."""
    def __init__(self, question, answer, main_window=None):
        super().__init__()
        self.question = question
        self.answer = answer
        self.is_flipped = False
        self.main_window = main_window

        styles = get_existing_flashcard_styles()
        self.setStyleSheet(styles["flashcard"])

        # RESPONSIVE SIZING - 30% of screen height
        if main_window:
            screen = main_window.screen()
            screen_size = screen.availableGeometry()
            self.setMinimumHeight(int(screen_size.height() * 0.3))
        else:
            self.setMinimumHeight(300)  # Fallback

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel(f"Q: {self.question}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

    def mousePressEvent(self, event):
        # Flip the card between question and answer.
        self.is_flipped = not self.is_flipped
        self.label.setText(f"A: {self.answer}" if self.is_flipped else f"Q: {self.question}")


class ExistingFlashcard(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.styles = get_existing_flashcard_styles()
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(self.styles["page"])
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)
        self.setLayout(layout)

        # Header area with Back to Main button
        header_layout = QHBoxLayout()
        back_to_main = QPushButton("← Back to Main")
        back_to_main.setCursor(Qt.CursorShape.PointingHandCursor)
        back_to_main.setStyleSheet(self.styles["back_button"])
        if self.main_window:
            back_to_main.clicked.connect(lambda: self.main_window.show_page(0))
        header_layout.addWidget(back_to_main)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Title
        title = QLabel("TOPICS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(self.styles["title"])
        layout.addWidget(title)

        # Scroll area for topics
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none; background-color: transparent;")
        layout.addWidget(self.scroll_area)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setSpacing(20)
        self.scroll_area.setWidget(self.scroll_widget)

        # Topic list with icon images
        self.topics = [
            {"name": "English", "color": "#B3D9FF", "icon": get_asset_path("BookIcon.png")},
            {"name": "Math", "color": "#B9FBC0", "icon": get_asset_path("MathIcon.png")},
            {"name": "Science", "color": "#FFE6A7", "icon": get_asset_path("ScienceIcon.png")},
            {"name": "History", "color": "#FFB3B3", "icon": get_asset_path("HistoryIcon.png")},
        ]

        # Flashcard question/answer sets
        self.qa_sets = {
            "English": [
                ("What is the plural form of the word child?", "Children"),
                ("What is the past tense of eat?", "Ate"),
                ("What is the opposite of cold?", "Hot"),
                ("What is the plural of dog?", "Dogs"),
                ("What is the past tense of see?", "Saw"),
            ],
            "Math": [
                ("1+1", "2"), ("2+2", "4"), ("3+3", "6"), ("4+4", "8"), ("5+5", "10")
            ],
            "Science": [
                ("Who discovered gravity?", "Isaac Newton"),
                ("What gas do humans need to breathe?", "Oxygen"),
                ("What is the center of the Solar System?", "The Sun"),
                ("What do plants need to make food?", "Sunlight"),
                ("What part of the body pumps blood?", "Heart"),
            ],
            "History": [
                ("Who killed Magellan?", "Lapu-Lapu"),
                ("Who was the first President of the United States?", "George Washington"),
                ("What ship famously sank in 1912?", "Titanic"),
                ("Who was known as the national hero of the Philippines?", "Dr. Jose Rizal"),
                ("Who was the first man to walk on the Moon?", "Neil Armstrong"),
            ],
        }

        # Show the initial topic list
        self.show_topics()

    def make_topic_handler(self, topic_name):
        return lambda checked=False, t=topic_name: self.open_topic(t)

    def clear_scroll_layout(self):
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                widget = item.widget()
                widget.setParent(None)
                widget.deleteLater()
            elif item.layout():
                # Clear sub-layout
                sub_layout = item.layout()
                while sub_layout.count():
                    sub_item = sub_layout.takeAt(0)
                    if sub_item.widget():
                        sub_widget = sub_item.widget()
                        sub_widget.setParent(None)
                        sub_widget.deleteLater()
                sub_layout.setParent(None)

    def show_topics(self):
        self.clear_scroll_layout()

        for topic in self.topics:
            btn = QPushButton(topic["name"])
            btn.setIcon(QIcon(QPixmap(topic["icon"])))
            btn.setIconSize(QtCore.QSize(60, 60))

            if self.main_window:
                screen = self.main_window.screen()
                screen_size = screen.availableGeometry()
                btn.setMinimumHeight(int(screen_size.height() * 0.1))
            else:
                btn.setMinimumHeight(60)

            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(self.styles["topic_button"].format(color=topic["color"]))
            btn.clicked.connect(self.make_topic_handler(topic["name"]))
            self.scroll_layout.addWidget(btn)

    def open_topic(self, topic_name):
        self.clear_scroll_layout()

        # Header layout
        header = QHBoxLayout()
        header.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel(f"{topic_name}")
        title.setStyleSheet(self.styles["topic_title"])
        timer_label = QLabel("Study: 25:00")
        timer_label.setStyleSheet(self.styles["timer_label"])

        back_btn = QPushButton("← Back to Topics")
        back_btn.setStyleSheet(self.styles["back_button"])
        back_btn.clicked.connect(self.show_topics)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(timer_label)
        header.addSpacing(10)
        header.addWidget(back_btn)
        self.scroll_layout.addLayout(header)

        # Flashcards
        self.cards = self.qa_sets.get(topic_name, []).copy()
        self.remaining_cards = self.cards.copy()
        self.current_index = 0
        self.correct_count = 0

        q, a = self.remaining_cards[self.current_index]
        self.card_widget = FlashcardWidget(q, a, self.main_window)
        self.scroll_layout.addWidget(self.card_widget)

        # Control buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        buttons = [
            ("Shuffle", "#55556A", self.shuffle_cards),
            ("Correct", "#A7F3A7", self.mark_correct),
            ("Wrong", "#F9A6A6", self.mark_wrong),
            ("Reset Progress", "#55556A", self.reset_progress),
        ]

        for text, color, handler in buttons:
            btn = QPushButton(text)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumSize(130, 50)
            btn.setStyleSheet(self.styles["control_button"].format(color=color))
            btn.clicked.connect(handler)
            btn_layout.addWidget(btn)

        self.scroll_layout.addLayout(btn_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet(self.styles["progress_bar"])
        self.scroll_layout.addWidget(self.progress_bar)

        self.update_card()

    # === Flashcard Logic ===
    def update_card(self):
        if not self.remaining_cards:
            self.card_widget.label.setText("🎉 Set Completed!")
            self.progress_bar.setValue(100)
            QMessageBox.information(self, "Set Completed", "Congratulations! You've completed this set.")
            return

        q, a = self.remaining_cards[self.current_index]
        self.card_widget.question, self.card_widget.answer = q, a
        self.card_widget.label.setText(f"Q: {q}")
        self.card_widget.is_flipped = False

        progress = int((self.correct_count / len(self.cards)) * 100)
        self.progress_bar.setValue(progress)

    def mark_correct(self):
        if not self.remaining_cards:
            return

        self.correct_count += 1
        del self.remaining_cards[self.current_index]
        if not self.remaining_cards:
            self.update_card()
            return

        self.current_index %= len(self.remaining_cards)
        self.update_card()

    def mark_wrong(self):
        if not self.remaining_cards:
            return
        self.current_index = (self.current_index + 1) % len(self.remaining_cards)
        self.update_card()

    def shuffle_cards(self, topic_name=None):
        shuffle(self.remaining_cards)
        self.current_index = 0
        self.update_card()

    def reset_progress(self):
        self.remaining_cards = self.cards.copy()
        self.correct_count = 0
        self.current_index = 0
        self.update_card()
