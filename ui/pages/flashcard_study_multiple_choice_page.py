# FINAL PROJECT FLASHCARD APP / ui / pages / flashcard_study_multiple_choice_page.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QMessageBox, QFrame, QButtonGroup,
                            QRadioButton, QGridLayout)
from PyQt6.QtCore import Qt, QTimer
import random
from ui.visual.styles.styles import get_multiple_choice_styles

class MultipleChoiceStudy(QWidget):
    def __init__(self, main_window, flashcard_set=None):
        super().__init__()
        self.main_window = main_window
        self.flashcard_set = flashcard_set
        self.correct_answers = 0
        self.total_questions = 0
        self.styles = get_multiple_choice_styles()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header frame - KEEP YOUR STYLES
        header_frame = QFrame()
        header_frame.setStyleSheet(self.styles["header_frame"])
        header_layout = QHBoxLayout(header_frame)
        
        if self.flashcard_set:
            set_name_text = f"MC: {self.flashcard_set['set_name']}"
        else:
            set_name_text = "Multiple Choice"
        
        self.set_name_label = QLabel(set_name_text)
        self.set_name_label.setStyleSheet(self.styles["set_name_label"])
        header_layout.addWidget(self.set_name_label)
        
        self.stats_label = QLabel("0/0 | Rem: 0/0")
        self.stats_label.setStyleSheet(self.styles["stats_label"])
        header_layout.addWidget(self.stats_label)
        
        header_layout.addStretch()
        
        back_btn = QPushButton("← Back")
        back_btn.setStyleSheet(self.styles["back_button"])
        back_btn.clicked.connect(self.go_back)
        back_btn.setMinimumSize(80, 30)
        header_layout.addWidget(back_btn)
        
        layout.addWidget(header_frame)
        
        # Question frame - KEEP YOUR STYLES
        question_frame = QFrame()
        question_frame.setStyleSheet(self.styles["question_frame"])
        question_frame.setMinimumHeight(60)
        question_frame.setMaximumHeight(150)
        
        question_layout = QVBoxLayout(question_frame)
        
        if self.flashcard_set:
            initial_question_text = "Click Next Question to start"
        else:
            initial_question_text = "Please select a flashcard set first"
            
        self.question_label = QLabel(initial_question_text)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet(self.styles["question_label"])  # YOUR STYLE
        question_layout.addWidget(self.question_label)
        
        layout.addWidget(question_frame)
        
        # Options - KEEP YOUR STYLES
        self.options_layout = QGridLayout()
        self.options_layout.setSpacing(8)
        
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        
        self.option_buttons = []
        for i in range(4):
            option_btn = QRadioButton()
            option_btn.setMinimumHeight(45)
            option_btn.setVisible(False)
            option_btn.setStyleSheet(self.styles["option_button"])  # YOUR STYLE
            self.button_group.addButton(option_btn, i)
            self.option_buttons.append(option_btn)
            
            row = i // 2
            col = i % 2
            self.options_layout.addWidget(option_btn, row, col)
        
        options_container = QWidget()
        options_container_layout = QVBoxLayout(options_container)
        options_container_layout.addStretch()
        options_container_layout.addLayout(self.options_layout)
        options_container_layout.addStretch()
        
        layout.addWidget(options_container)
        
        # Result label - KEEP YOUR STYLES
        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setMinimumHeight(25)
        self.result_label.setStyleSheet(self.styles["result_label"])  # YOUR STYLE
        layout.addWidget(self.result_label)
        
        # Next button - KEEP YOUR STYLES
        self.next_btn = QPushButton("Next Question")
        self.next_btn.setStyleSheet(self.styles["next_button"])  # YOUR STYLE
        self.next_btn.clicked.connect(self.show_next_question)
        self.next_btn.setMinimumHeight(35)
        self.next_btn.setMaximumWidth(200)
            
        if not self.flashcard_set:
            self.next_btn.setEnabled(False)
        
        button_container = QHBoxLayout()
        button_container.addStretch()
        button_container.addWidget(self.next_btn)
        button_container.addStretch()
        layout.addLayout(button_container)
        
        self.setLayout(layout)
        self.button_group.buttonClicked.connect(self.on_option_selected)

    # ALL YOUR EXISTING METHODS BELOW - NO CHANGES TO FUNCTIONALITY
    def update_flashcard_set(self, flashcard_set):
        self.flashcard_set = flashcard_set
        self.correct_answers = 0
        self.total_questions = 0
        
        self.remaining_cards = self.flashcard_set['cards'].copy()
        self.mastered_cards = []
        self.attempted_cards = {}
        
        self.set_name_label.setText(f"MC: {self.flashcard_set['set_name']}")
        remaining_count = len(self.remaining_cards)
        total_cards = len(self.flashcard_set['cards'])
        self.stats_label.setText(f"0/{total_cards} | Rem: {remaining_count}/{total_cards}")
        self.next_btn.setEnabled(True)
        
        self.show_next_question()

    def show_next_question(self):
        if not self.remaining_cards:
            self.show_completion_message()
            return
        
        self.result_label.clear()
        self.next_btn.hide()
        self.button_group.setExclusive(False)
        for button in self.option_buttons:
            button.setChecked(False)
            button.setEnabled(True)
            button.setVisible(True)
        self.button_group.setExclusive(True)
        
        self.current_card = random.choice(self.remaining_cards)
        correct_answer = self.current_card['answer']
        
        options = [correct_answer]
        all_other_cards = [card for card in self.flashcard_set['cards'] if card['answer'] != correct_answer]
        wrong_answers = random.sample([card['answer'] for card in all_other_cards], min(3, len(all_other_cards)))
        
        while len(wrong_answers) < 3:
            wrong_answers.append("Not enough options")
        
        options.extend(wrong_answers)
        random.shuffle(options)
        
        self.correct_answer_index = options.index(correct_answer)
        self.question_label.setText(f"{self.current_card['question']}")
        
        for i, option in enumerate(options):
            self.option_buttons[i].setText(option)
            self.option_buttons[i].setVisible(True)

    def on_option_selected(self, button):
        if not self.flashcard_set:
            return
            
        selected_index = self.button_group.id(button)
        current_question = self.current_card['question']
        is_first_attempt = current_question not in self.attempted_cards
        
        if selected_index == self.correct_answer_index:
            if is_first_attempt:
                self.remaining_cards.remove(self.current_card)
                self.mastered_cards.append(self.current_card)
                self.attempted_cards[current_question] = 'mastered'
                self.correct_answers += 1
                self.result_label.setText("Correct! First try - this question is mastered!")
            else:
                self.result_label.setText("Correct! But since you got it wrong before, it will appear again.")
            
            for btn in self.option_buttons:
                btn.setEnabled(False)
            self.next_btn.show()
        
        else:
            self.attempted_cards[current_question] = 'failed'
            button.setEnabled(False)
            self.result_label.setText("Wrong! This question will appear again until you master it.")
        
        remaining_count = len(self.remaining_cards)
        total_cards = len(self.flashcard_set['cards'])
        self.stats_label.setText(f"{self.correct_answers}/{total_cards} | Rem: {remaining_count}/{total_cards}")
        
        if not self.remaining_cards:
            self.result_label.setText("All questions mastered on first try! Quiz complete!")

    def show_completion_message(self):
        self.question_label.setText("Quiz Complete!")
        
        for button in self.option_buttons:
            button.setVisible(False)
        
        total_cards = len(self.flashcard_set['cards'])
        self.result_label.setText(f"Perfect! You mastered all {total_cards} cards!")
        self.next_btn.setText("Restart Quiz")
        self.next_btn.clicked.disconnect()
        self.next_btn.clicked.connect(self.restart_quiz)
        self.next_btn.show()

    def restart_quiz(self):
        self.update_flashcard_set(self.flashcard_set)
        self.next_btn.setText("Next Question")
        self.next_btn.clicked.disconnect()
        self.next_btn.clicked.connect(self.show_next_question)
    
    def go_back(self):
        try:
            self.main_window.show_page(3)
        except Exception as e:
            import traceback
            traceback.print_exc()