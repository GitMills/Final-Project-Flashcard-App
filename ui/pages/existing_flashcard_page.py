# FINAL PROJECT FLASHCARD APP / ui / pages / existing_flashcard_page.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QHBoxLayout,
    QProgressBar, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from random import shuffle


class FlashcardWidget(QFrame):
    """Single clickable flashcard that flips between question and answer."""
    def __init__(self, question, answer, main_window=None):
        super().__init__()
        self.question = question
        self.answer = answer
        self.is_flipped = False
        self.main_window = main_window

        self.setStyleSheet("""
            QFrame {
                background-color: #FDE3E3;
                border-radius: 20px;
            }
            QLabel {
                font-size: 16px;
                color: #333;
            }
        """)
        
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
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: #FFF7EB;")
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)
        self.setLayout(layout)

        # Header area with Back to Main button
        header_layout = QHBoxLayout()
        back_to_main = QPushButton("← Back to Main")
        back_to_main.setCursor(Qt.CursorShape.PointingHandCursor)
        back_to_main.setStyleSheet("""
            QPushButton {
                background-color: #F27D72;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #d25a50; }
        """)
        if self.main_window:
            back_to_main.clicked.connect(lambda: self.main_window.show_page(0))
        header_layout.addWidget(back_to_main)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Title
        title = QLabel("TOPICS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                background-color: #F27D72;
                color: white;
                border-radius: 15px;
                padding: 15px;
            }
        """)
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

        # Topic list
        self.topics = [
            {"name": "English", "color": "#B3D9FF", "icon": "📘"},
            {"name": "Math", "color": "#B9FBC0", "icon": "🧮"},
            {"name": "Science", "color": "#FFE6A7", "icon": "🔬"},
            {"name": "History", "color": "#FFB3B3", "icon": "🌎"},
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
        # Bind topic name to open the topic layout.
        return lambda checked=False, t=topic_name: self.open_topic(t)

    def clear_scroll_layout(self):
        # Utility to clear the scroll layout cleanly.
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
                # Remove the layout itself
                sub_layout.setParent(None)

    def show_topics(self):
        # Restore the original topic list.
        self.clear_scroll_layout()

        for topic in self.topics:
            btn = QPushButton(f"{topic['icon']}   {topic['name']}")
            
            # RESPONSIVE SIZING - 10% of screen height
            if self.main_window:
                screen = self.main_window.screen()
                screen_size = screen.availableGeometry()
                btn.setMinimumHeight(int(screen_size.height() * 0.1))
            else:
                btn.setMinimumHeight(60)  # Fallback
                
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {topic['color']};
                    border: none;
                    border-radius: 25px;
                    font-size: 20px;
                    font-weight: bold;
                    color: #333;
                    text-align: left;
                    padding-left: 30px;
                }}
                QPushButton:hover {{
                    background-color: #dfefff;
                }}
            """)
            btn.clicked.connect(self.make_topic_handler(topic["name"]))
            self.scroll_layout.addWidget(btn)

    def open_topic(self, topic_name):
        # Show the single-study layout for a topic.
        self.clear_scroll_layout()

        # Header layout
        header = QHBoxLayout()
        header.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel(f"{topic_name}")
        title.setStyleSheet("font-weight: bold; color: #9C9AC2; font-size: 20px;")
        timer_label = QLabel("Study: 25:00")
        timer_label.setStyleSheet("color: #5f5f5f; font-size: 14px;")

        back_btn = QPushButton("← Back to Topics")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #F27D72;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #d25a50; }
        """)
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
        self.card_widget = FlashcardWidget(q, a, self.main_window)  # Pass main_window for responsive sizing
        self.scroll_layout.addWidget(self.card_widget)

        # Control buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        shuffle_btn = QPushButton("Shuffle")
        correct_btn = QPushButton("Correct")
        wrong_btn = QPushButton("Wrong")
        reset_btn = QPushButton("Reset Progress")

        for btn, color in [
            (shuffle_btn, "#55556A"),
            (correct_btn, "#A7F3A7"),
            (wrong_btn, "#F9A6A6"),
            (reset_btn, "#55556A"),
        ]:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumSize(130, 50)  # MINIMUM SIZE - functional requirement
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                    color: black;
                }}
                QPushButton:hover {{
                    opacity: 0.8;
                }}
            """)
            btn_layout.addWidget(btn)

        self.scroll_layout.addLayout(btn_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                height: 18px;
                border-radius: 8px;
                background-color: #DDD;
            }
            QProgressBar::chunk {
                background-color: #55556A;
                border-radius: 8px;
            }
        """)
        self.scroll_layout.addWidget(self.progress_bar)

        # Button logic
        shuffle_btn.clicked.connect(lambda: self.shuffle_cards(topic_name))
        correct_btn.clicked.connect(self.mark_correct)
        wrong_btn.clicked.connect(self.mark_wrong)
        reset_btn.clicked.connect(self.reset_progress)

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

    def shuffle_cards(self, topic_name):
        shuffle(self.remaining_cards)
        self.current_index = 0
        self.update_card()

    def reset_progress(self):
        self.remaining_cards = self.cards.copy()
        self.correct_count = 0
        self.current_index = 0
        self.update_card()