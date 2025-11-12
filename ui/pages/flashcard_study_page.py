# FINAL PROJECT FLASHCARD APP / ui / pages / flashcard_study_page.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QFrame, QProgressBar, QCheckBox)
from PyQt6.QtCore import Qt
from ui.visual.styles.styles import get_study_page_styles, get_inline_label_styles, get_shuffle_button_active_style
import random

class FlashcardStudyPage(QWidget):
    def __init__(self, main_window, flashcard_set):
        super().__init__()
        self.main_window = main_window
        self.flashcard_set = flashcard_set or {'set_name': 'No Set', 'cards': []}
        self.current_card_index = 0
        self.is_flipped = False
        self.styles = get_study_page_styles()
        self.label_styles = get_inline_label_styles()
        
        # Hybrid hint system variables
        self.current_hint_level = 0
        self.max_hint_level = 1
        self.hint_strategy = 'word_by_word'
        self.answer_words = ['']
        
        # Simple progress tracking
        self.card_progress = {}
        
        # Shuffle toggle functionality
        self.is_shuffled = False
        self.original_card_order = []
        
        self.setup_ui()
        if self.flashcard_set and self.flashcard_set['cards']:
            # Store original order
            import copy
            self.original_card_order = copy.deepcopy(self.flashcard_set['cards'])
            self.load_card(0)
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # HEADER - Set name, difficulty badge, and back button
        header_layout = QHBoxLayout()
        
        # Set name and difficulty - left side in vertical layout
        name_difficulty_layout = QVBoxLayout()
        name_difficulty_layout.setSpacing(2)
        
        set_name_text = self.flashcard_set['set_name'] if self.flashcard_set else "No Set Selected"
        self.set_name_label = QLabel(set_name_text)
        self.set_name_label.setStyleSheet(self.styles["title"])
        name_difficulty_layout.addWidget(self.set_name_label)
        
        # Difficulty level text below set name
        difficulty = self.flashcard_set.get('difficulty', 'Easy')
        self.difficulty_badge = QLabel(f"Difficulty level: {difficulty}")
        self.difficulty_badge.setStyleSheet(self.label_styles["difficulty_badge_study"])
        name_difficulty_layout.addWidget(self.difficulty_badge)
        
        header_layout.addLayout(name_difficulty_layout)
        header_layout.addStretch()
        
        # Back button - right
        self.back_btn = QPushButton("← Back to All Cards")
        self.back_btn.setStyleSheet(self.styles["back_button"])
        self.back_btn.clicked.connect(self.go_back)
        header_layout.addWidget(self.back_btn)
        
        layout.addLayout(header_layout)
        
        # FLIP CARD AREA - with card counter
        card_area_layout = QHBoxLayout()
        card_area_layout.addStretch()
        
        self.flip_card_container = QFrame()
        
        # RESPONSIVE SIZING - 40% of screen width and height
        if self.main_window:
            screen = self.main_window.screen()
            screen_size = screen.availableGeometry()
            card_width = int(screen_size.width() * 0.4)
            card_height = int(screen_size.height() * 0.4)
            self.flip_card_container.setMinimumSize(card_width, card_height)
        else:
            self.flip_card_container.setMinimumSize(800, 600)  # Fallback
        
        # Create flip card with card counter
        self.setup_flip_card()
        card_area_layout.addWidget(self.flip_card_container)
        card_area_layout.addStretch()
        
        layout.addLayout(card_area_layout)
        
        # CONTROLS BELOW PROGRESS BAR - Horizontal: Shuffle, Hint, Correct, Wrong, Reset
        controls_layout = QHBoxLayout()
        controls_layout.addStretch()
        
        # Shuffle toggle button
        self.shuffle_btn = QPushButton("🔀 Shuffle")
        self.shuffle_btn.setStyleSheet(self.styles["shuffle_button"])
        self.shuffle_btn.clicked.connect(self.toggle_shuffle)
        controls_layout.addWidget(self.shuffle_btn)

        # Correct button
        self.correct_btn = QPushButton("Correct")
        self.correct_btn.setStyleSheet(self.styles["correct_button"])
        self.correct_btn.clicked.connect(lambda: self.mark_card(True))
        controls_layout.addWidget(self.correct_btn)
        
        # HINT BUTTON - Hybrid system
        self.hint_btn = QPushButton("Show Hint")
        self.hint_btn.setStyleSheet(self.styles["hint_button"])
        self.hint_btn.clicked.connect(self.show_hint)
        controls_layout.addWidget(self.hint_btn)
        
        # Wrong button
        self.wrong_btn = QPushButton("Wrong")
        self.wrong_btn.setStyleSheet(self.styles["wrong_button"])
        self.wrong_btn.clicked.connect(lambda: self.mark_card(False))
        controls_layout.addWidget(self.wrong_btn)
        
        # Reset progress
        self.reset_btn = QPushButton("Reset Progress")
        self.reset_btn.setStyleSheet(self.styles["reset_button"])
        self.reset_btn.clicked.connect(self.reset_progress)
        controls_layout.addWidget(self.reset_btn)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        self.setLayout(layout)
        
        # PROGRESS BAR - Below flip card
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setStyleSheet(self.styles["progress_bar"])
        layout.addWidget(self.progress_bar)
    
    def setup_flip_card(self):
        # Create front card with counter
        self.card_front = QFrame()
        self.card_front.setStyleSheet(self.styles["card_front"])
        
        front_layout = QVBoxLayout(self.card_front)
        front_layout.setSpacing(8)
        front_layout.setContentsMargins(20, 20, 20, 20)
        
        # QUESTION badge at top - smaller, no background
        question_badge = QLabel("Question")
        question_badge.setStyleSheet(self.label_styles["question_answer_badge"])
        question_badge.setAlignment(Qt.AlignmentFlag.AlignLeft)
        front_layout.addWidget(question_badge)
        
        # Card counter - centered
        self.front_counter = QLabel("Card 1 of 1")
        self.front_counter.setStyleSheet(self.styles["card_counter"])
        self.front_counter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        front_layout.addWidget(self.front_counter)
        
        # Individual card difficulty indicator - centered below counter
        self.front_card_difficulty = QLabel()
        self.front_card_difficulty.setStyleSheet(self.label_styles["card_difficulty_indicator"])
        self.front_card_difficulty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        front_layout.addWidget(self.front_card_difficulty)
        
        # Add stretch before content to push it to center
        front_layout.addStretch()
        
        # Front content
        self.front_label = QLabel()
        self.front_label.setStyleSheet(self.styles["card_text"])
        self.front_label.setWordWrap(True)
        self.front_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        front_layout.addWidget(self.front_label)
        
        # HINT LABEL - For hybrid system
        self.hint_label = QLabel()
        self.hint_label.setStyleSheet(self.styles["hint_text"])
        self.hint_label.setWordWrap(True)
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hint_label.hide()
        front_layout.addWidget(self.hint_label)
        
        # Add stretch after content to center everything
        front_layout.addStretch() 

        # Create back card with counter
        self.card_back = QFrame()
        self.card_back.setStyleSheet(self.styles["card_back"])
        
        back_layout = QVBoxLayout(self.card_back)
        back_layout.setSpacing(8)
        back_layout.setContentsMargins(20, 20, 20, 20)
        
        # ANSWER badge at top - smaller, no background
        answer_badge = QLabel("Answer")
        answer_badge.setStyleSheet(self.label_styles["question_answer_badge"])
        answer_badge.setAlignment(Qt.AlignmentFlag.AlignLeft)
        back_layout.addWidget(answer_badge)
        
        # Card counter - centered
        self.back_counter = QLabel("Card 1 of 1")
        self.back_counter.setStyleSheet(self.styles["card_counter"])
        self.back_counter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        back_layout.addWidget(self.back_counter)
        
        # Individual card difficulty indicator - centered below counter
        self.back_card_difficulty = QLabel()
        self.back_card_difficulty.setStyleSheet(self.label_styles["card_difficulty_indicator"])
        self.back_card_difficulty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        back_layout.addWidget(self.back_card_difficulty)
        
        # Add stretch before content to push it to center
        back_layout.addStretch()

        # Back content
        self.back_label = QLabel()
        self.back_label.setStyleSheet(self.styles["card_text"])
        self.back_label.setWordWrap(True)
        self.back_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        back_layout.addWidget(self.back_label)
        
        # Add stretch after content to center everything
        back_layout.addStretch()
        
        # Start with front visible
        self.card_back.hide()
        self.card_front.show()
        
        # Add both cards to container
        flip_layout = QVBoxLayout(self.flip_card_container)
        flip_layout.addWidget(self.card_front)
        flip_layout.addWidget(self.card_back)
        
        # FIXED: Proper click handling for flip
        self.card_front.mousePressEvent = self.handle_flip_click
        self.card_back.mousePressEvent = self.handle_flip_click
    
    def handle_flip_click(self, event):
        """Handle click events for both front and back cards"""
        self.flip_card()
        event.accept()
    
    def flip_card(self):
        if self.is_flipped:
            self.card_front.show()
            self.card_back.hide()
        else:
            self.card_front.hide()
            self.card_back.show()
        self.is_flipped = not self.is_flipped
    
    def analyze_answer_type(self, answer):
        """Determine if answer is single word or sentence and choose hint strategy"""
        try:
            if not answer or not isinstance(answer, str):
                return 'word_by_word', [''], 1
                
            clean_answer = answer.strip()
            if not clean_answer:
                return 'word_by_word', [''], 1
                
            words = clean_answer.split()
            
            # Single word: just one word with reasonable length
            if len(words) == 1 and len(clean_answer) <= 20:
                return 'letter_by_letter', [clean_answer], len(clean_answer)
            
            # Sentence: use word-by-word revelation
            else:
                return 'word_by_word', words, len(words)
                
        except Exception as e:
            print(f"Error analyzing answer type: {e}")
            return 'word_by_word', [answer], 1
    
    def load_card(self, index):
        try:
            if not self.flashcard_set or not self.flashcard_set['cards']:
                self.front_label.setText("No flashcards available")
                self.back_label.setText("Please select a flashcard set first")
                return
                
            if 0 <= index < len(self.flashcard_set['cards']):
                self.current_card_index = index
                card = self.flashcard_set['cards'][index]
                
                self.front_label.setText(f"{card['question']}")
                self.back_label.setText(f"{card['answer']}")
                
                # Analyze answer and set up HYBRID hint system
                answer = card['answer'].strip()
                self.hint_strategy, self.answer_words, self.max_hint_level = self.analyze_answer_type(answer)
                
                # Reset hint state
                self.current_hint_level = 0
                self.hint_label.hide()
                self.hint_btn.setText("Show Hint")
                self.hint_btn.setEnabled(True)
                
                # Reset flip state
                self.is_flipped = False
                self.card_front.show()
                self.card_back.hide()
                
                # Update UI
                self.update_card_counter()
                self.update_progress()
                
        except Exception as e:
            print(f"Error loading card: {e}")
            self.front_label.setText("Error loading card")
            self.back_label.setText("Please try another card")
    
    def show_hint(self):
        """HYBRID SYSTEM: Show hint using appropriate strategy based on answer type"""
        try:
            if not self.flashcard_set or not self.flashcard_set['cards']:
                return
            
            current_card = self.flashcard_set['cards'][self.current_card_index]
            
            # Check if custom hint exists
            if 'custom_hint' in current_card and current_card['custom_hint']:
                # Show custom hint
                self.hint_label.setText(f"<b>Hint:</b> {current_card['custom_hint']}")
                self.hint_label.show()
                self.hint_btn.setText("Full Answer")
                self.hint_btn.setEnabled(False)
                return
                
            self.current_hint_level += 1
            
            # Ensure we don't exceed bounds
            self.current_hint_level = min(self.current_hint_level, self.max_hint_level)
            
            if self.hint_strategy == 'letter_by_letter':
                self._show_letter_hint()
            else:  # word_by_word
                self._show_word_hint()
            
            # Update button
            if self.current_hint_level >= self.max_hint_level:
                self.hint_btn.setText("Full Answer")
                self.hint_btn.setEnabled(False)
            else:
                self.hint_btn.setText(f"Show Hint ({self.current_hint_level}/{self.max_hint_level})")
                
        except Exception as e:
            print(f"Error showing hint: {e}")
            self.hint_label.setText("Error showing hint")
            self.hint_label.show()
    
    def _show_letter_hint(self):
        """Letter-by-letter hint for single words"""
        try:
            if not self.answer_words or not self.answer_words[0]:
                self.hint_label.setText("<b>Hint:</b> No hint available")
                self.hint_label.show()
                return
                
            word = self.answer_words[0]
            if self.current_hint_level >= len(word):
                # Full word revealed
                hint_text = f"<b>Hint:</b> {word}"
            else:
                # Partial reveal with underscores
                revealed = word[:self.current_hint_level]
                remaining = " ".join(["_"] * (len(word) - self.current_hint_level))
                hint_text = f"<b>Hint:</b> {revealed} {remaining}"
            
            self.hint_label.setText(hint_text)
            self.hint_label.show()
            
        except Exception as e:
            print(f"Error in letter hint: {e}")
            self.hint_label.setText("<b>Hint:</b> Error")
            self.hint_label.show()
    
    def _show_word_hint(self):
        """Word-by-word hint for sentences"""
        try:
            if not self.answer_words:
                self.hint_label.setText("<b>Hint:</b> No hint available")
                self.hint_label.show()
                return
                
            # Ensure we don't go out of bounds
            safe_hint_level = min(self.current_hint_level, len(self.answer_words))
            revealed_words = self.answer_words[:safe_hint_level]
            remaining_count = len(self.answer_words) - safe_hint_level
            
            # Create the hint display
            if safe_hint_level >= len(self.answer_words):
                # Full sentence revealed
                full_sentence = " ".join(self.answer_words)
                hint_text = f"<b>Hint:</b> {full_sentence}"
            else:
                # Partial reveal with blanks for remaining words
                revealed_part = " ".join(revealed_words)
                blanks = " ".join(["_____"] * remaining_count)
                hint_text = f"<b>Hint:</b> {revealed_part} {blanks}"
            
            self.hint_label.setText(hint_text)
            self.hint_label.show()
            
        except Exception as e:
            print(f"Error in word hint: {e}")
            self.hint_label.setText("<b>Hint:</b> Error")
            self.hint_label.show()
    
    def update_card_counter(self):
        total = len(self.flashcard_set['cards'])
        current = self.current_card_index + 1
        counter_text = f"Card {current} of {total}"
        self.front_counter.setText(counter_text)
        self.back_counter.setText(counter_text)
        
        # Update individual card difficulty indicator
        current_card = self.flashcard_set['cards'][self.current_card_index]
        card_difficulty = current_card.get('difficulty', '')
        
        if card_difficulty:
            difficulty_text = f"Difficulty: {card_difficulty}"
            self.front_card_difficulty.setText(difficulty_text)
            self.back_card_difficulty.setText(difficulty_text)
        else:
            self.front_card_difficulty.setText("")
            self.back_card_difficulty.setText("")
    
    def update_progress(self):
        # Calculate progress based on mastered cards (3 correct answers)
        total_cards = len(self.flashcard_set['cards'])
        mastered_cards = 0
        
        for card in self.flashcard_set['cards']:
            card_id = card['question']  # Use question as unique ID
            if card_id in self.card_progress and self.card_progress[card_id] >= 2:
                mastered_cards += 1
        
        progress = (mastered_cards / total_cards) * 100 if total_cards > 0 else 0
        self.progress_bar.setValue(int(progress))
    
    def mark_card(self, correct):
        from core.controller import FlashcardController
        username = self.main_window.get_current_username() if self.main_window else None
        controller = FlashcardController(username)
        
        current_card = self.flashcard_set['cards'][self.current_card_index]
        card_id = current_card['question']
        
        # Update progress tracking
        if card_id not in self.card_progress:
            self.card_progress[card_id] = 0
            
        if correct:
            self.card_progress[card_id] += 1
        else:
            self.card_progress[card_id] = max(0, self.card_progress[card_id] - 1)
        
        # Update database
        learned = self.card_progress[card_id] >= 2
        controller.update_card_progress(
            self.flashcard_set['set_name'],
            self.current_card_index,
            learned,
            correct
        )
        
        # Update local data
        if 'progress' not in current_card:
            current_card['progress'] = {'learned': False, 'times_correct': 0, 'times_wrong': 0}
        
        if correct:
            current_card['progress']['times_correct'] += 1
            current_card['progress']['learned'] = learned
        else:
            current_card['progress']['times_wrong'] += 1
            current_card['progress']['learned'] = False
        
        # Auto-advance to next card
        self.update_progress()
        if self.current_card_index < len(self.flashcard_set['cards']) - 1:
            self.load_card(self.current_card_index + 1)
        else:
            # End of set - show completion if all mastered
            mastered_count = sum(1 for card in self.flashcard_set['cards'] 
                               if card['question'] in self.card_progress and self.card_progress[card['question']] >= 2)
            
            if mastered_count == len(self.flashcard_set['cards']):
                self.front_label.setText("🎉 Set Complete!")
                self.back_label.setText(f"You've mastered all {len(self.flashcard_set['cards'])} cards!")
                self.correct_btn.setEnabled(False)
                self.wrong_btn.setEnabled(False)
                self.hint_btn.setEnabled(False)
            else:
                # Loop back to beginning
                self.load_card(0)
    
    def toggle_shuffle(self):
        """Toggle between shuffled and original order"""
        import copy
        
        if self.is_shuffled:
            # Restore original order
            self.flashcard_set['cards'] = copy.deepcopy(self.original_card_order)
            self.is_shuffled = False
            self.shuffle_btn.setText("🔀 Shuffle")
            self.shuffle_btn.setStyleSheet(self.styles["shuffle_button"])
        else:
            # Make sure we have the original order saved
            if not self.original_card_order:
                self.original_card_order = copy.deepcopy(self.flashcard_set['cards'])
            
            # Create a shuffled copy
            shuffled_cards = copy.deepcopy(self.flashcard_set['cards'])
            random.shuffle(shuffled_cards)
            self.flashcard_set['cards'] = shuffled_cards
            
            self.is_shuffled = True
            self.shuffle_btn.setText("↩️ Reset Order")
            # Change button color to indicate shuffled state
            self.shuffle_btn.setStyleSheet(get_shuffle_button_active_style())
        
        # Load first card and preserve progress
        self.load_card(0)
        self.correct_btn.setEnabled(True)
        self.wrong_btn.setEnabled(True)
        self.hint_btn.setEnabled(True)
    
    def reset_progress(self):
        from core.controller import FlashcardController
        username = self.main_window.get_current_username() if self.main_window else None
        controller = FlashcardController(username)
        
        for i in range(len(self.flashcard_set['cards'])):
            controller.update_card_progress(
                self.flashcard_set['set_name'],
                i,
                False,
                False
            )
            if 'progress' in self.flashcard_set['cards'][i]:
                self.flashcard_set['cards'][i]['progress'] = {
                    'learned': False, 
                    'times_correct': 0, 
                    'times_wrong': 0
                }
        
        # Reset local progress tracking
        self.card_progress = {}
        
        self.update_progress()
        self.load_card(0)
        self.correct_btn.setEnabled(True)
        self.wrong_btn.setEnabled(True)
        self.hint_btn.setEnabled(True)

    
    def go_back(self):
        self.main_window.show_page(3)  # Back to All Cards page