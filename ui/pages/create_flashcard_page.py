from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QScrollArea, QFrame
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from ui.visual.styles.styles import get_create_flashcard_styles


class CreateFlashcard(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.flashcards = []  # Store flashcards
        self.current_card_number = 1  # Track card numbers
        self.styles = get_create_flashcard_styles()
        self.setup_ui()
    
    def setup_ui(self):
        # Main layout - no margins for full window usage
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        
        # Scroll area for all content (title, set name, flashcards)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Content widget that goes inside the scroll area
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(15)
        self.scroll_layout.setContentsMargins(20, 20, 20, 150)  # Extra bottom space for floating buttons
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Page title
        self.title = QLabel("Create New Flashcard")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet(self.styles["title"])
        self.scroll_layout.addWidget(self.title)

        # Flashcard set name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Set Name")
        self.name_input.setStyleSheet(self.styles["name_input"])
        self.scroll_layout.addWidget(self.name_input)
        
        # Create 3 initial empty flashcards
        self.create_flashcard_inputs()
        
        # Add stretch to push content up
        self.scroll_layout.addStretch()
        
        # Set the scroll content
        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)
        
        # FLOATING BUTTONS - these stay fixed at bottom, don't scroll
        self.floating_button_container = QWidget(self)
        self.floating_button_container.setFixedHeight(150)  # Height of button bar
        
        button_layout = QHBoxLayout(self.floating_button_container)
        button_layout.setSpacing(10)
        button_layout.setContentsMargins(20, 10, 20, 10)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create the three main buttons
        self.add_btn = QPushButton("Add Flashcard")
        self.add_btn.setStyleSheet(self.styles["add_button"])
        self.save_btn = QPushButton("Save Flashcard")
        self.save_btn.setStyleSheet(self.styles["save_button"])
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(self.styles["cancel_button"])
        
        # Add buttons to layout
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        # Connect button clicks to functions
        self.add_btn.clicked.connect(self.add_flashcard_input)
        self.save_btn.clicked.connect(self.save_all_flashcards)
        self.cancel_btn.clicked.connect(self.go_back)
    
    def resizeEvent(self, event):
        self.floating_button_container.setGeometry(0, self.height() - 150, self.width(), 150)
        super().resizeEvent(event)
    
    def create_flashcard_inputs(self):
        #Create 3 initial flashcard input sections
        for i in range(3):
            self.add_flashcard_input()

    def add_flashcard_input(self):
        #Add a new flashcard input section to the scroll area
        # Create card container frame
        card_frame = QFrame()
        card_frame.setStyleSheet(self.styles["card_frame"])
        
        card_layout = QVBoxLayout(card_frame)
        
        # Card number label
        card_number = QLabel(f"Card {self.current_card_number}")
        card_number.setStyleSheet(self.styles["card_number"])
        
        # Question input field
        question_input = QLineEdit()
        question_input.setPlaceholderText("Enter Question")
        question_input.setStyleSheet(self.styles["question_input"])
        
        # Answer input field (text area for longer answers)
        answer_input = QTextEdit()
        answer_input.setPlaceholderText("Enter Answer")
        answer_input.setMaximumHeight(80)
        answer_input.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        answer_input.setStyleSheet(self.styles["answer_input"])
        
        # Store references to inputs for later access
        card_frame.question_input = question_input
        card_frame.answer_input = answer_input
        card_frame.card_number = self.current_card_number
        
        # Add widgets to card layout
        card_layout.addWidget(card_number)
        card_layout.addWidget(question_input)  
        card_layout.addWidget(answer_input)    
        
        # Add card to scroll area
        self.scroll_layout.addWidget(card_frame)
        
        # Increment card counter
        self.current_card_number += 1

        # Auto-scroll to show the new card
        self._scroll_to_bottom()

    def _scroll_to_bottom(self):
        #Scroll to bottom instantly without any delays
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def save_all_flashcards(self):
        #Collect and save all flashcards from the form
        self.flashcards = []
        
        # Loop through all card frames in scroll area
        for i in range(self.scroll_layout.count() - 1):  # -1 to exclude the stretch
            item = self.scroll_layout.itemAt(i)
            if item and item.widget() and isinstance(item.widget(), QFrame):
                frame = item.widget()
                question = frame.question_input.text().strip()
                answer = frame.answer_input.toPlainText().strip()
                
                # Only save cards that have both question and answer
                if question and answer:
                    card_data = {
                        'number': frame.card_number,
                        'question': question,
                        'answer': answer
                    }
                    self.flashcards.append(card_data)
        
        # Process the saved flashcards
        if self.flashcards:
            print(f"Saved {len(self.flashcards)} flashcards:")
            for card in self.flashcards:
                print(f"Card #{card['number']}: Q: {card['question']}, A: {card['answer']}")
            self.clear_form()
        else:
            print("Please fill at least one flashcard")
    
    def clear_form(self):
        """Clear all flashcard inputs but keep the form structure"""
        for i in range(self.scroll_layout.count() - 1):
            item = self.scroll_layout.itemAt(i)
            if item and item.widget() and isinstance(item.widget(), QFrame):
                frame = item.widget()
                frame.question_input.clear()
                frame.answer_input.clear()
    
    def go_back(self):
        """Return to the home page"""
        self.main_window.show_page(0)