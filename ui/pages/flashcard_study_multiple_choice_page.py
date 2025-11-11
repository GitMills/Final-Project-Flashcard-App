# FINAL PROJECT FLASHCARD APP / ui / pages / flashcard_study_multiple_choice_page.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QFrame, QRadioButton, QButtonGroup)
from PyQt6.QtCore import Qt
from ui.visual.styles.styles import get_multiple_choice_styles
import random

class MultipleChoiceStudy(QWidget):
    def __init__(self, main_window, flashcard_set):
        super().__init__()
        self.main_window = main_window
        self.flashcard_set = flashcard_set or {'set_name': 'No Set', 'cards': []}
        self.current_card_index = 0
        self.correct_count = 0
        self.wrong_count = 0
        self.styles = get_multiple_choice_styles()
        
        # Card deck system to prevent infinite loops
        self.card_deck = []
        self.mastered_cards = []
        self.total_cards = 0
        
        self.setup_ui()
    
    def keyPressEvent(self, event):
        """Override to prevent space bar from triggering buttons"""
        from PyQt6.QtCore import Qt
        if event.key() == Qt.Key.Key_Space:
            # Ignore space bar to prevent accidental navigation
            event.ignore()
        else:
            super().keyPressEvent(event)
        
    def update_flashcard_set(self, flashcard_set):
        """Update the flashcard set and reset the study session"""
        self.flashcard_set = flashcard_set
        self.current_card_index = 0
        self.correct_count = 0
        self.wrong_count = 0
        
        # Initialize card deck system
        if self.flashcard_set and self.flashcard_set.get('cards'):
            import copy
            self.card_deck = copy.deepcopy(self.flashcard_set['cards'])
            self.mastered_cards = []
            self.total_cards = len(self.card_deck)
            self.last_answer_correct = False
            random.shuffle(self.card_deck)
            
            # Force uncheck all radio buttons before loading
            if hasattr(self, 'option_buttons'):
                for btn in self.option_buttons:
                    btn.setAutoExclusive(False)
                    btn.setChecked(False)
                for btn in self.option_buttons:
                    btn.setAutoExclusive(True)
            
            self.load_question()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)
        self.setLayout(layout)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setStyleSheet(self.styles["back_button"])
        back_btn.clicked.connect(lambda: self.main_window.show_page(3))
        back_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # Prevent space bar activation
        header_layout.addWidget(back_btn)
        
        header_layout.addStretch()
        
        # Set name
        self.set_name_label = QLabel("Multiple Choice")
        self.set_name_label.setStyleSheet(self.styles["set_name_label"])
        header_layout.addWidget(self.set_name_label)
        
        header_layout.addStretch()
        
        # Stats
        self.stats_label = QLabel("Question 1 of 1")
        self.stats_label.setStyleSheet(self.styles["stats_label"])
        header_layout.addWidget(self.stats_label)
        
        layout.addLayout(header_layout)
        
        # Question frame
        self.question_frame = QFrame()
        self.question_frame.setStyleSheet(self.styles["question_frame"])
        question_layout = QVBoxLayout(self.question_frame)
        
        self.question_label = QLabel("Question will appear here")
        self.question_label.setStyleSheet(self.styles["question_label"])
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        question_layout.addWidget(self.question_label)
        
        layout.addWidget(self.question_frame)
        
        # Options
        self.options_layout = QVBoxLayout()
        self.options_layout.setSpacing(10)
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(False)  # Allow unchecking all
        self.option_buttons = []
        
        for i in range(4):
            option = QRadioButton(f"Option {i+1}")
            option.setStyleSheet(self.styles["option_button"])
            option.setAutoExclusive(False)  # Allow manual unchecking
            option.setChecked(False)  # Ensure not checked by default
            self.button_group.addButton(option, i)
            self.option_buttons.append(option)
            # Auto-check when option is clicked
            option.clicked.connect(self.on_option_clicked)
            # Disable space bar activation
            option.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.options_layout.addWidget(option)
        
        layout.addLayout(self.options_layout)
        
        # Result label
        self.result_label = QLabel("")
        self.result_label.setStyleSheet(self.styles["result_label"])
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.hide()
        layout.addWidget(self.result_label)
        
        # Next button (initially hidden since we auto-check)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.next_btn = QPushButton("Next Question")
        self.next_btn.setStyleSheet(self.styles["next_button"])
        self.next_btn.clicked.connect(self.next_question)
        self.next_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # Prevent space bar activation
        self.next_btn.hide()  # Hidden until answer is checked
        button_layout.addWidget(self.next_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        layout.addStretch()

        
    def load_question(self):
        """Load current question with multiple choice options using card deck system"""
        # Check if deck is empty
        if not self.card_deck:
            self.show_completion()
            return
        
        # Get current card from deck
        current_card = self.card_deck[0]
        self.question_label.setText(current_card['question'])
        
        # Reset mistake tracker for THIS NEW appearance
        self.had_mistake_this_appearance = False
        
        # Update stats - show progress through total cards
        remaining = len(self.card_deck)
        mastered = len(self.mastered_cards)
        self.stats_label.setText(f"Remaining: {remaining} | Mastered: {mastered}/{self.total_cards}")
        self.set_name_label.setText(self.flashcard_set.get('set_name', 'Multiple Choice'))
        
        # Generate options
        correct_answer = current_card['answer']
        
        # Get all available cards for wrong options (from both deck and mastered)
        all_available_cards = self.card_deck + self.mastered_cards
        other_answers = [card['answer'] for card in all_available_cards if card['answer'] != correct_answer]
        
        # Check if we have enough unique answers
        if len(other_answers) < 3:
            # Not enough options - show error and complete
            self.question_label.setText("⚠️ Not enough unique answers to generate options!")
            self.result_label.setText("Please add more cards with different answers.")
            self.result_label.setStyleSheet(self.styles["result_label"] + "background-color: #F9E2AF;")
            self.result_label.show()
            
            # Hide options and change button
            for btn in self.option_buttons:
                btn.hide()
            self.next_btn.setText("Back to Sets")
            self.next_btn.clicked.disconnect()
            self.next_btn.clicked.connect(lambda: self.main_window.show_page(3))
            return
        
        # Shuffle and select wrong options
        random.shuffle(other_answers)
        wrong_options = other_answers[:3]
        
        # Combine and shuffle all options
        all_options = [correct_answer] + wrong_options
        random.shuffle(all_options)
        
        # Store correct answer
        self.correct_answer = correct_answer
        
        # Update buttons
        for i, option_text in enumerate(all_options):
            self.option_buttons[i].setText(option_text)
            self.option_buttons[i].setEnabled(True)
            self.option_buttons[i].setChecked(False)
            self.option_buttons[i].show()
        
        self.result_label.hide()
        self.next_btn.hide()  # Hide until answer is selected
        
    def on_option_clicked(self):
        """Handle option click - uncheck others and check answer"""
        clicked_button = self.sender()
        
        # Uncheck all other buttons
        for btn in self.option_buttons:
            if btn != clicked_button:
                btn.setChecked(False)
        
        # Ensure clicked button is checked
        clicked_button.setChecked(True)
        
        # Check the answer
        self.check_answer()
    
    def check_answer(self):
        """Check if selected answer is correct - tracks mistakes per appearance"""
        selected_button = self.button_group.checkedButton()
        if not selected_button:
            return
            
        selected_answer = selected_button.text()
        
        if selected_answer == self.correct_answer:
            # Correct answer!
            if hasattr(self, 'had_mistake_this_appearance') and self.had_mistake_this_appearance:
                # Had mistakes on this appearance - card will appear again
                self.result_label.setText("✓ Correct! But you made mistakes, so it will appear again.")
                self.result_label.setStyleSheet(self.styles["result_label"] + "background-color: #F9E2AF;")
            else:
                # First try correct - card is mastered!
                self.result_label.setText("✓ Correct! First try - this question is mastered!")
                self.result_label.setStyleSheet(self.styles["result_label"] + "background-color: #A6E3A1;")
            self.correct_count += 1
        else:
            # Wrong answer - mark that we had a mistake
            self.had_mistake_this_appearance = True
            self.result_label.setText(f"✗ Wrong! Try another answer.")
            self.result_label.setStyleSheet(self.styles["result_label"] + "background-color: #F38BA8;")
            self.wrong_count += 1
            
            # Re-enable options so they can try again on SAME question
            for btn in self.option_buttons:
                btn.setEnabled(True)
                btn.setChecked(False)
            
            self.result_label.show()
            return  # Don't change to Next button - let them try again
        
        self.result_label.show()
        
        # Disable options
        for btn in self.option_buttons:
            btn.setEnabled(False)
        
        # Show Next button
        self.next_btn.show()
        
    def next_question(self):
        """Move to next question using card deck system"""
        if not self.card_deck:
            self.show_completion()
            return
        
        current_card = self.card_deck[0]
        
        # Only remove if answered correctly on FIRST TRY (no mistakes this appearance)
        if not self.had_mistake_this_appearance:
            # First try correct - remove from deck and add to mastered
            self.card_deck.pop(0)
            self.mastered_cards.append(current_card)
        else:
            # Had mistakes - move to back of deck for another try
            self.card_deck.pop(0)
            self.card_deck.append(current_card)
        
        # Uncheck all radio buttons to clear selection color
        for btn in self.option_buttons:
            btn.setChecked(False)
        
        # Load next question (which will reset had_mistake_this_appearance)
        self.load_question()
        
    def show_completion(self):
        """Show completion message with detailed stats"""
        total_attempts = self.correct_count + self.wrong_count
        accuracy = (self.correct_count / total_attempts * 100) if total_attempts > 0 else 0
        
        completion_text = f"🎉 All Cards Mastered!\n\n"
        completion_text += f"Total Cards: {self.total_cards}\n"
        completion_text += f"Correct Answers: {self.correct_count}\n"
        completion_text += f"Wrong Answers: {self.wrong_count}\n"
        completion_text += f"Accuracy: {accuracy:.1f}%"
        
        self.question_label.setText(completion_text)
        
        # Hide options
        for btn in self.option_buttons:
            btn.hide()
        
        self.result_label.hide()
        
        # Change Next button to show two options
        self.next_btn.setText("🔄 Try Again")
        self.next_btn.clicked.disconnect()
        self.next_btn.clicked.connect(self.restart_quiz)
        self.next_btn.show()
    
    def restart_quiz(self):
        """Restart the quiz with the same flashcard set"""
        # Re-initialize with the same flashcard set
        self.update_flashcard_set(self.flashcard_set)
