# FINAL PROJECT FLASHCARD APP / ui / pages / flashcard_study_page.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QFrame, QProgressBar, QCheckBox)
from PyQt6.QtCore import Qt
from ui.visual.styles.styles import get_study_page_styles
import random

class FlashcardStudyPage(QWidget):
    def __init__(self, main_window, flashcard_set):
        super().__init__()
        self.main_window = main_window
        self.flashcard_set = flashcard_set or {'set_name': 'No Set', 'cards': []}
        self.current_card_index = 0
        self.is_flipped = False
        self.styles = get_study_page_styles()
        
        # Simple progress tracking
        self.card_progress = {}  # Track correct counts per card
        
        self.setup_ui()
        if self.flashcard_set and self.flashcard_set['cards']:
            self.load_card(0)
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # HEADER - Just set name and back button
        header_layout = QHBoxLayout()
        
        # Set name - left
        set_name_text = self.flashcard_set['set_name'] if self.flashcard_set else "No Set Selected"
        self.set_name_label = QLabel(set_name_text)
        self.set_name_label.setStyleSheet(self.styles["title"])
        header_layout.addWidget(self.set_name_label)
        
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
        
        # CONTROLS BELOW PROGRESS BAR - Horizontal: Shuffle, Correct, Wrong, Reset
        controls_layout = QHBoxLayout()
        controls_layout.addStretch()
        
        # Shuffle button
        self.shuffle_btn = QPushButton("Shuffle")
        self.shuffle_btn.setStyleSheet(self.styles["shuffle_button"])
        self.shuffle_btn.clicked.connect(self.shuffle_cards)
        controls_layout.addWidget(self.shuffle_btn)
        
        # Correct button
        self.correct_btn = QPushButton("Correct")
        self.correct_btn.setStyleSheet(self.styles["correct_button"])
        self.correct_btn.clicked.connect(lambda: self.mark_card(True))
        controls_layout.addWidget(self.correct_btn)
        
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
        
        # Card counter on front - simple text like before
        self.front_counter = QLabel("Card 1 of 1")
        self.front_counter.setStyleSheet(self.styles["card_counter"])
        self.front_counter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        front_layout.addWidget(self.front_counter)
        
        # Front content
        self.front_label = QLabel()
        self.front_label.setStyleSheet(self.styles["card_text"])
        self.front_label.setWordWrap(True)
        self.front_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        front_layout.addWidget(self.front_label)
        self.front_counter.setFixedHeight(15) 

        
        
        # Create back card with counter
        self.card_back = QFrame()
        self.card_back.setStyleSheet(self.styles["card_back"])
        
        back_layout = QVBoxLayout(self.card_back)
        
        # Card counter on back - simple text like before
        self.back_counter = QLabel("Card 1 of 1")
        self.back_counter.setStyleSheet(self.styles["card_counter"])
        self.back_counter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        back_layout.addWidget(self.back_counter)
        self.back_counter.setFixedHeight(15)

        
        # Back content
        self.back_label = QLabel()
        self.back_label.setStyleSheet(self.styles["card_text"])
        self.back_label.setWordWrap(True)
        self.back_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        back_layout.addWidget(self.back_label)
        
        # Start with front visible
        self.card_back.hide()
        self.card_front.show()
        
        # Add both cards to container
        flip_layout = QVBoxLayout(self.flip_card_container)
        flip_layout.addWidget(self.card_front)
        flip_layout.addWidget(self.card_back)
        
        # Click to flip
        self.card_front.mousePressEvent = lambda e: self.flip_card()
        self.card_back.mousePressEvent = lambda e: self.flip_card()
    
    def flip_card(self):
        if self.is_flipped:
            self.card_front.show()
            self.card_back.hide()
        else:
            self.card_front.hide()
            self.card_back.show()
        self.is_flipped = not self.is_flipped
    
    def load_card(self, index):
        if not self.flashcard_set or not self.flashcard_set['cards']:
            self.front_label.setText("No flashcards available")
            self.back_label.setText("Please select a flashcard set first")
            return
            
        if 0 <= index < len(self.flashcard_set['cards']):
            self.current_card_index = index
            card = self.flashcard_set['cards'][index]
            
            self.front_label.setText(f"Q: {card['question']}")
            self.back_label.setText(f"A: {card['answer']}")
            
            # Reset flip state
            self.is_flipped = False
            self.card_front.show()
            self.card_back.hide()
            
            # Update UI
            self.update_card_counter()
            self.update_progress()
    
    def update_card_counter(self):
        total = len(self.flashcard_set['cards'])
        current = self.current_card_index + 1
        counter_text = f"Card {current} of {total}"
        self.front_counter.setText(counter_text)
        self.back_counter.setText(counter_text)
    
    def update_progress(self):
        # Calculate progress based on mastered cards (3 correct answers)
        total_cards = len(self.flashcard_set['cards'])
        mastered_cards = 0
        
        for card in self.flashcard_set['cards']:
            card_id = card['question']  # Use question as unique ID
            if card_id in self.card_progress and self.card_progress[card_id] >= 3:
                mastered_cards += 1
        
        progress = (mastered_cards / total_cards) * 100 if total_cards > 0 else 0
        self.progress_bar.setValue(int(progress))
    
    def mark_card(self, correct):
        from core.controller import FlashcardController
        controller = FlashcardController()
        
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
        learned = self.card_progress[card_id] >= 3
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
                               if card['question'] in self.card_progress and self.card_progress[card['question']] >= 3)
            
            if mastered_count == len(self.flashcard_set['cards']):
                self.front_label.setText("🎉 Set Complete!")
                self.back_label.setText(f"You've mastered all {len(self.flashcard_set['cards'])} cards!")
                self.correct_btn.setEnabled(False)
                self.wrong_btn.setEnabled(False)
            else:
                # Loop back to beginning
                self.load_card(0)
    
    def shuffle_cards(self):
        random.shuffle(self.flashcard_set['cards'])
        self.load_card(0)
        self.correct_btn.setEnabled(True)
        self.wrong_btn.setEnabled(True)
    
    def reset_progress(self):
        from core.controller import FlashcardController
        controller = FlashcardController()
        
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

    
    def go_back(self):
        self.main_window.show_page(3)  # Back to All Cards page