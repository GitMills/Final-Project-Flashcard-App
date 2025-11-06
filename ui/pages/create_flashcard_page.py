from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QScrollArea, QFrame, QMessageBox
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap
from ui.visual.styles.styles import get_create_flashcard_styles
from utils.path_helper import get_asset_path


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
        self.scroll_area.setStyleSheet(self.styles["scroll_area"])
        
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
        try:
            # Collect flashcard data from the form
            self.flashcards = []
            set_name = self.name_input.text().strip()
            
            # Validate set name - CORRECT WAY
            if not set_name:
                missing_set_warning = QMessageBox(self)
                missing_set_warning.setWindowTitle("Missing Set Name")
                missing_set_warning.setText("Please enter a name for your flashcard set.")
                missing_set_warning.setStyleSheet(self.styles["warning_message_box"])
                missing_set_warning.setIcon(QMessageBox.Icon.Warning)
                missing_set_warning.setStandardButtons(QMessageBox.StandardButton.Ok)
                
                # Load custom icon
                icon_path = get_asset_path("warning_icon.png")  
                custom_icon = QPixmap(icon_path)
                
                if not custom_icon.isNull():
                    missing_set_warning.setIconPixmap(custom_icon.scaled(74, 74, Qt.AspectRatioMode.KeepAspectRatio))
                else:
                    missing_set_warning.setIcon(QMessageBox.Icon.Information)
                
                missing_set_warning.setStandardButtons(QMessageBox.StandardButton.Ok)
                missing_set_warning.exec()
                return
        
            # Loop through all card frames and collect data
            for i in range(self.scroll_layout.count() - 1):
                item = self.scroll_layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    
                    # ONLY process QFrame widgets (the card containers)
                    if isinstance(widget, QFrame) and hasattr(widget, 'question_input'):
                        question = widget.question_input.text().strip()
                        answer = widget.answer_input.toPlainText().strip()
                        
                        if question and answer:
                            card_data = {
                                'question': question,
                                'answer': answer
                            }
                            self.flashcards.append(card_data)
            
            # Validate we have at least one flashcard
            if not self.flashcards:
                no_flashcard_warning = QMessageBox(self)
                no_flashcard_warning.setWindowTitle("No Flashcards ")
                no_flashcard_warning.setText("Please fill in at least one flashcard.")
                no_flashcard_warning.setStyleSheet(self.styles["warning_message_box"])
                no_flashcard_warning.setIcon(QMessageBox.Icon.Warning)
                no_flashcard_warning.setStandardButtons(QMessageBox.StandardButton.Ok)
                    
                # Load custom icon  
                icon_path = get_asset_path("warning_icon.png")  
                custom_icon = QPixmap(icon_path)
                
                if not custom_icon.isNull():
                    no_flashcard_warning.setIconPixmap(custom_icon.scaled(74, 74, Qt.AspectRatioMode.KeepAspectRatio))
                else:
                    no_flashcard_warning.setIcon(QMessageBox.Icon.Information)
                    
                no_flashcard_warning.setStandardButtons(QMessageBox.StandardButton.Ok)
                no_flashcard_warning.exec()
                return
            
            # Use controller to save the flashcard set
            from core.controller import FlashcardController
            controller = FlashcardController()
            error_message = controller.create_flashcard_set(set_name, self.flashcards)
            
            if error_message:
                save_error_warning = QMessageBox(self)
                save_error_warning.setWindowTitle("Save Error")
                save_error_warning.setText(f"Failed to save flashcard set:\n{error_message}")
                save_error_warning.setStyleSheet(self.styles["warning_message_box"])
                save_error_warning.setIcon(QMessageBox.Icon.Warning)
                save_error_warning.setStandardButtons(QMessageBox.StandardButton.Ok)
                
                # Load custom icon
                icon_path = get_asset_path("warning_icon.png")  
                custom_icon = QPixmap(icon_path)
                
                if not custom_icon.isNull():
                    save_error_warning.setIconPixmap(custom_icon.scaled(74, 74, Qt.AspectRatioMode.KeepAspectRatio))
                else:
                    save_error_warning.setIcon(QMessageBox.Icon.Information)
                
                save_error_warning.setStandardButtons(QMessageBox.StandardButton.Ok)
                save_error_warning.exec()
            else:
                # SUCCESS MESSAGE BOX
                self.show_save_success(set_name, len(self.flashcards))
                self.clear_form()
                self.name_input.clear()

        except Exception as e:
            critical_error_warning = QMessageBox(self)
            critical_error_warning.setWindowTitle("Critical Error")
            critical_error_warning.setText(f"The app encountered an error:\n{str(e)}")
            critical_error_warning.setStyleSheet(self.styles["warning_message_box"])
            critical_error_warning.setIcon(QMessageBox.Icon.Warning)
            critical_error_warning.setStandardButtons(QMessageBox.StandardButton.Ok)
            
            # Load custom icon
            icon_path = get_asset_path("warning_icon.png")  
            custom_icon = QPixmap(icon_path)
            
            if not custom_icon.isNull():
                critical_error_warning.setIconPixmap(custom_icon.scaled(74, 74, Qt.AspectRatioMode.KeepAspectRatio))
            else:
                critical_error_warning.setIcon(QMessageBox.Icon.Information)
            
            critical_error_warning.setStandardButtons(QMessageBox.StandardButton.Ok)
            critical_error_warning.exec()

    def show_save_success(self, set_name, card_count):

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Success!")
        msg_box.setText(f"Flashcard set '{set_name}' saved successfully!")
        msg_box.setInformativeText(f"Total cards saved: {card_count}")
        
        # Apply the success style
        msg_box.setStyleSheet(self.styles["success_message_box"])
        
        # Load custom success icon
        icon_path = get_asset_path("success.png")  # Use your success icon
        custom_icon = QPixmap(icon_path)
        
        if not custom_icon.isNull():
            msg_box.setIconPixmap(custom_icon.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            msg_box.setIcon(QMessageBox.Icon.Information)
        
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def clear_form(self):
        # Clear all flashcard inputs but keep the form structure
        for i in range(self.scroll_layout.count() - 1):
            item = self.scroll_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                # Only clear QFrame widgets (the card containers)
                if isinstance(widget, QFrame):
                    # Check if the frame has the question_input attribute
                    if hasattr(widget, 'question_input'):
                        widget.question_input.clear()
                    if hasattr(widget, 'answer_input'):
                        widget.answer_input.clear()

    def go_back(self):
        #Show confirmation dialog with custom icon
    
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirm Cancel")
        msg_box.setText("Are you sure you want to cancel?")
        msg_box.setInformativeText("All unsaved changes will be lost.")
        
        # Apply the warning style
        msg_box.setStyleSheet(self.styles["warning_message_box"])
        
        # Load custom icon using path helper
        icon_path = get_asset_path("warning_icon.png")
        custom_icon = QPixmap(icon_path)
        
        if not custom_icon.isNull():
            msg_box.setIconPixmap(custom_icon.scaled(84, 84, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            msg_box.setIcon(QMessageBox.Icon.Warning)
        
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        
        if msg_box.exec() == QMessageBox.StandardButton.Yes:
            self.main_window.show_page(0)