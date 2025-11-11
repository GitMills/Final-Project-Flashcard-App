from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QHBoxLayout,
    QFrame, QMessageBox, QProgressBar, QDialog
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6 import QtCore
from PyQt6.QtGui import QIcon, QPixmap
from random import shuffle, sample

from ui.visual.styles.styles import get_existing_flashcard_styles
from utils.path_helper import get_asset_path


# ========================================
# FLASHCARD WIDGET
# ========================================
class FlashcardWidget(QFrame):
    def __init__(self, question, answer, main_window=None):
        super().__init__()
        self.question = question
        self.answer = answer
        self.is_flipped = False
        self.main_window = main_window

        styles = get_existing_flashcard_styles()
        self.setStyleSheet(styles["flashcard"])

        if main_window:
            screen = main_window.screen()
            screen_size = screen.availableGeometry()
            self.setMinimumHeight(int(screen_size.height() * 0.3))
        else:
            self.setMinimumHeight(300)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel(f"Q: {self.question}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: #3E3E3E;")
        layout.addWidget(self.label)

    def mousePressEvent(self, event):
        self.is_flipped = not self.is_flipped
        self.label.setText(f"A: {self.answer}" if self.is_flipped else f"Q: {self.question}")


# ========================================
# STUDY MODE DIALOG
# ========================================
class StudyModeDialog(QDialog):
    def __init__(self, topic_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose Study Mode")
        self.setModal(True)
        self.setFixedWidth(280)
        self.setStyleSheet("""
            QDialog { background-color: #FAF3E0; border-radius: 12px; }
            QLabel { font-size: 18px; color: #4B3F2F; font-weight: bold; }
            QPushButton {
                font-size: 16px; background-color: #D3C1E5;
                color: #4B3F2F; padding: 10px; border-radius: 12px; margin-top: 10px;
            }
            QPushButton:hover { background-color: #C5AEDC; }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title = QLabel(f"Study: {topic_name}")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        sub_label = QLabel("Choose a mode to begin")
        sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sub_label)

        self.flip_btn = QPushButton("Flip Cards")
        self.mc_btn = QPushButton("Multiple Choice")
        self.view_btn = QPushButton("View/Edit Flashcards")
        self.cancel_btn = QPushButton("Cancel")
        layout.addWidget(self.flip_btn)
        layout.addWidget(self.mc_btn)
        layout.addWidget(self.view_btn)
        layout.addWidget(self.cancel_btn)
        self.cancel_btn.clicked.connect(self.reject)


# ========================================
# EXISTING FLASHCARD PAGE
# ========================================
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

        header_layout = QHBoxLayout()
        back_to_main = QPushButton("← Back to Main")
        back_to_main.setCursor(Qt.CursorShape.PointingHandCursor)
        back_to_main.setStyleSheet(self.styles["back_button"])
        if self.main_window:
            back_to_main.clicked.connect(lambda: self.main_window.show_page(0))
        header_layout.addWidget(back_to_main)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        title = QLabel("TOPICS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(self.styles["title"])
        layout.addWidget(title)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none; background-color: transparent;")
        layout.addWidget(self.scroll_area)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setSpacing(20)
        self.scroll_area.setWidget(self.scroll_widget)

        self.topics = [
            {"name": "English", "color": "#B3D9FF", "icon": get_asset_path("BookIcon.png")},
            {"name": "Math", "color": "#B9FBC0", "icon": get_asset_path("MathIcon.png")},
            {"name": "Science", "color": "#FFE6A7", "icon": get_asset_path("ScienceIcon.png")},
            {"name": "History", "color": "#FFB3B3", "icon": get_asset_path("HistoryIcon.png")},
        ]

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

        self.show_topics()

    def make_topic_handler(self, topic_name):
        return lambda checked=False, t=topic_name: self.open_topic(t)

    def clear_scroll_layout(self):
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub_item = item.layout().takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()

    def show_topics(self):
        self.clear_scroll_layout()
        for topic in self.topics:
            btn = QPushButton(topic["name"])
            btn.setIcon(QIcon(QPixmap(topic["icon"])))
            btn.setIconSize(QtCore.QSize(60, 60))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(self.styles["topic_button"].format(color=topic["color"]))
            btn.clicked.connect(self.make_topic_handler(topic["name"]))
            self.scroll_layout.addWidget(btn)

    def open_topic(self, topic_name):
        dialog = StudyModeDialog(topic_name, self)
        dialog.flip_btn.clicked.connect(lambda: (dialog.accept(), self.start_flip_mode(topic_name)))
        dialog.mc_btn.clicked.connect(lambda: (dialog.accept(), self.start_multiple_choice_mode(topic_name)))
        dialog.view_btn.clicked.connect(lambda: (dialog.accept(), QMessageBox.information(self, "View/Edit", "Feature coming soon!")))
        dialog.exec()

    # ==========================================================
    # FLIP CARD MODE (correct stays out, wrong repeats)
    # ==========================================================
    def start_flip_mode(self, topic_name):
        self.clear_scroll_layout()

        header = QHBoxLayout()
        title = QLabel(f"{topic_name}")
        title.setStyleSheet(self.styles["topic_title"])
        back_btn = QPushButton("← Back to All Cards")
        back_btn.setStyleSheet(self.styles["back_button"])
        back_btn.clicked.connect(self.show_topics)
        header.addWidget(title)
        header.addStretch()
        header.addSpacing(10)
        header.addWidget(back_btn)
        self.scroll_layout.addLayout(header)

        self.cards = self.qa_sets.get(topic_name, []).copy()
        self.remaining_cards = self.cards.copy()
        self.correct_cards = []
        self.current_index = 0

        q, a = self.remaining_cards[self.current_index]
        self.card_widget = FlashcardWidget(q, a, self.main_window)
        self.scroll_layout.addWidget(self.card_widget)

        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.addWidget(self.feedback_label)

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

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet(self.styles["progress_bar"])
        self.scroll_layout.addWidget(self.progress_bar)

        self.update_card()

    def update_card(self):
        if not self.remaining_cards:
            self.card_widget.label.setText("🎉 Set Completed!")
            self.feedback_label.setText("✅ You mastered all flashcards!")
            self.progress_bar.setValue(100)
            return

        q, a = self.remaining_cards[self.current_index]
        self.card_widget.question, self.card_widget.answer = q, a
        self.card_widget.label.setText(f"Q: {q}")
        self.card_widget.is_flipped = False

        progress = int((len(self.correct_cards) / len(self.cards)) * 100)
        self.progress_bar.setValue(progress)
        self.feedback_label.setText("")

    def mark_correct(self):
        if not self.remaining_cards:
            return
        correct_card = self.remaining_cards.pop(self.current_index)
        self.correct_cards.append(correct_card)
        if not self.remaining_cards:
            self.update_card()
            return
        self.current_index %= len(self.remaining_cards)
        self.update_card()

    def mark_wrong(self):
        if not self.remaining_cards:
            return
        self.feedback_label.setText("❌ Try again later!")
        self.current_index = (self.current_index + 1) % len(self.remaining_cards)
        self.update_card()

    def shuffle_cards(self):
        shuffle(self.remaining_cards)
        self.current_index = 0
        self.update_card()

    def reset_progress(self):
        self.remaining_cards = self.cards.copy()
        self.correct_cards = []
        self.current_index = 0
        self.update_card()

    # ==========================================================
    # MULTIPLE CHOICE MODE (accurate in-topic options)
    # ==========================================================
    def start_multiple_choice_mode(self, topic_name):
        self.topic_name = topic_name
        self.cards = self.qa_sets.get(topic_name, []).copy()
        shuffle(self.cards)
        self.remaining_cards = self.cards.copy()
        self.mastered = []
        self.current_index = 0

        self.load_mc_question()

    def load_mc_question(self):
        self.clear_scroll_layout()

        header = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setStyleSheet("background-color:#f0d6d6; border:none; border-radius:8px; padding:8px 12px; font-weight:bold;")
        back_btn.clicked.connect(self.show_topics)
        header.addWidget(back_btn)

        topic_label = QLabel(self.topic_name)
        topic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        topic_label.setStyleSheet("font-size:22px; font-weight:bold; color:#4B3F2F;")
        header.addStretch()
        header.addWidget(topic_label)
        header.addStretch()

        self.progress_label = QLabel(f"Remaining: {len(self.remaining_cards)} | Mastered: {len(self.mastered)}")
        self.progress_label.setStyleSheet("font-size:16px; color:#4B3F2F; font-weight:bold;")
        header.addWidget(self.progress_label)
        self.scroll_layout.addLayout(header)

        if not self.remaining_cards:
            done_label = QLabel("🎉 Congratulations! You've mastered all questions!")
            done_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            done_label.setStyleSheet("font-size:22px; font-weight:bold; color:#4B3F2F; margin-top:60px;")
            self.scroll_layout.addWidget(done_label)
            return

        q, correct = self.remaining_cards[self.current_index]

        q_frame = QFrame()
        q_frame.setStyleSheet("""
            QFrame {
                background-color: #FFD6E0;
                border-radius: 20px;
                padding: 40px;
            }
        """)
        q_layout = QVBoxLayout(q_frame)
        q_label = QLabel(q)
        q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_label.setWordWrap(True)
        q_label.setStyleSheet("font-size:24px; font-weight:bold; color:#4B3F2F;")
        q_layout.addWidget(q_label)
        self.scroll_layout.addWidget(q_frame)

        # choices from same topic
        topic_answers = [a for _, a in self.qa_sets[self.topic_name] if a != correct]
        options = [correct] + sample(topic_answers, min(3, len(topic_answers)))
        shuffle(options)

        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback_label.setStyleSheet("font-size:18px; font-weight:bold; margin-top:10px;")

        for ans in options:
            btn = QPushButton(ans)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #FFF6E5;
                    border: 2px solid #E8DCCC;
                    border-radius: 12px;
                    font-size:18px;
                    padding:10px;
                }
                QPushButton:hover {
                    background-color: #FCEBD0;
                }
            """)
            btn.clicked.connect(lambda checked=False, a=ans, c=correct: self.check_mc_answer(a, c))
            self.scroll_layout.addWidget(btn)

        self.scroll_layout.addWidget(self.feedback_label)

    def check_mc_answer(self, chosen, correct):
        if chosen == correct:
            self.feedback_label.setText("✅ Correct!")
            self.feedback_label.setStyleSheet("color:#4CAF50; font-size:18px; font-weight:bold; margin-top:10px;")
            self.mastered.append(self.remaining_cards[self.current_index])
            del self.remaining_cards[self.current_index]
            QTimer.singleShot(1000, self.load_mc_question)
        else:
            self.feedback_label.setText("❌ Incorrect! This will appear again.")
            self.feedback_label.setStyleSheet("color:#E53935; font-size:18px; font-weight:bold; margin-top:10px;")
            self.remaining_cards.append(self.remaining_cards.pop(self.current_index))
            QTimer.singleShot(1200, self.load_mc_question)
