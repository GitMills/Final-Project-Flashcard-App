# FINAL PROJECT FLASHCARD APP / ui / pages / create_flashcard_page.py

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
        main_layout.setContentsMargins(85, 0, 85, 0) # Left, top, Right, Bottom
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
        
        # Create 4 initial empty flashcards
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
        
        # Create the four main buttons
        self.add_btn = QPushButton("Add Flashcard")
        self.add_btn.setStyleSheet(self.styles["add_button"])
        self.save_btn = QPushButton("Save Flashcard")
        self.save_btn.setStyleSheet(self.styles["save_button"])
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setStyleSheet(self.styles["cancel_button"])  # Using cancel style for reset
        self.back_btn = QPushButton("Back")
        self.back_btn.setStyleSheet(self.styles["cancel_button"])
        
        # Add buttons to layout
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.reset_btn)
        button_layout.addWidget(self.back_btn)
        
        # Connect button clicks to functions
        self.add_btn.clicked.connect(self.add_flashcard_input)
        self.save_btn.clicked.connect(self.save_all_flashcards)
        self.reset_btn.clicked.connect(self.show_reset_warning)
        self.back_btn.clicked.connect(self.go_back)
    
    def resizeEvent(self, event):
        self.floating_button_container.setGeometry(0, self.height() - 150, self.width(), 150)
        super().resizeEvent(event)
    
    def create_flashcard_inputs(self):
        # Create 4 initial flashcard input sections
        for i in range(4):
            self.add_flashcard_input()

    def add_flashcard_input(self):
        # Create card container frame
        card_frame = QFrame()
        
        # Apply color cycling based on card position
        color_index = (self.current_card_number - 1) % 4 + 1
        card_frame.setStyleSheet(self.styles[f"card_frame_{color_index}"])
        
        card_layout = QVBoxLayout(card_frame)
        
        # Card header with number and remove button (only show remove for cards 5+)
        card_header = QHBoxLayout()
        
        # Card number label
        card_number = QLabel(f"Card {self.current_card_number}")
        card_number.setStyleSheet(self.styles["card_number"])
        
        card_header.addWidget(card_number)
        
        # Only add remove button for cards 5 and above
        if self.current_card_number >= 5:
            remove_btn = QPushButton("✗")
            remove_btn.setMinimumSize(30, 30)  # FIXED: setFixedSize -> setMinimumSize
            remove_btn.setStyleSheet(self.styles["remove_btn"])
            remove_btn.clicked.connect(lambda checked, frame=card_frame: self.remove_flashcard(frame))
            card_header.addStretch()
            card_header.addWidget(remove_btn)
        else:
            card_header.addStretch()  # Push card number to left for cards 1-4
        
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
        card_layout.addLayout(card_header)
        card_layout.addWidget(question_input)  
        card_layout.addWidget(answer_input)    
        
        # Add card to scroll area
        self.scroll_layout.addWidget(card_frame)
        
        # Increment card counter
        self.current_card_number += 1

        # Auto-scroll to show the new card
        self._scroll_to_bottom()

    def remove_flashcard(self, card_frame):
        # Count current cards
        current_card_count = self.count_flashcards()
        
        # Prevent removal if it would go below minimum 4 cards
        if current_card_count <= 4:
            QMessageBox.warning(self, "Minimum Cards", "You must have at least 4 flashcards.")
            return
        
        # Remove the card frame from layout
        self.scroll_layout.removeWidget(card_frame)
        card_frame.deleteLater()
        
        # Re-number all remaining cards and update colors
        self.renumber_cards()

    def count_flashcards(self):
        count = 0
        for i in range(self.scroll_layout.count()):
            item = self.scroll_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, QFrame) and hasattr(widget, 'question_input'):
                    count += 1
        return count

    def renumber_cards(self):
        # Re-number all cards and update their colors
        card_frames = []
        
        # Collect all card frames
        for i in range(self.scroll_layout.count()):
            item = self.scroll_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, QFrame) and hasattr(widget, 'question_input'):
                    card_frames.append(widget)
        
        # Re-number and update colors
        for index, card_frame in enumerate(card_frames, 1):
            # Find the card number label in the card header
            card_header = card_frame.layout().itemAt(0).layout()
            card_number_label = card_header.itemAt(0).widget()
            card_number_label.setText(f"Card {index}")
            
            # Update the stored card number
            card_frame.card_number = index
            
            # Update color based on new position
            color_index = (index - 1) % 4 + 1
            card_frame.setStyleSheet(self.styles[f"card_frame_{color_index}"])
            
            # Update remove button visibility (only show for cards 5+)
            self.update_remove_button_visibility(card_frame, index)
        
        # Reset current_card_number to continue from the correct number
        self.current_card_number = len(card_frames) + 1

    def update_remove_button_visibility(self, card_frame, card_number):
        #Show/hide remove button based on card number
        card_header = card_frame.layout().itemAt(0).layout()
        
        # First, remove any existing remove button by checking widget types
        for i in range(card_header.count() - 1, -1, -1):
            item = card_header.itemAt(i)
            if item and item.widget() and isinstance(item.widget(), QPushButton):
                remove_btn = item.widget()
                card_header.removeWidget(remove_btn)
                remove_btn.deleteLater()
        
        # Also remove any stretch that might be before the button
        for i in range(card_header.count() - 1, -1, -1):
            item = card_header.itemAt(i)
            if item and item.layout() is None and item.widget() is None:  # It's a stretch
                card_header.removeItem(item)
        
        # Add remove button only for cards 5+
        if card_number >= 5:
            remove_btn = QPushButton("✗")
            remove_btn.setMinimumSize(30, 30)  # FIXED: setFixedSize -> setMinimumSize
            remove_btn.setStyleSheet(self.styles['remove_btn'])
            remove_btn.clicked.connect(lambda checked, frame=card_frame: self.remove_flashcard(frame))
            card_header.addStretch()
            card_header.addWidget(remove_btn)
        else:
            # Ensure cards 1-4 have proper layout with stretch
            card_header.addStretch()

    def _scroll_to_bottom(self):
        # Scroll to bottom instantly without any delays
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def save_all_flashcards(self):
        try:
            # Debug info
            is_editing = hasattr(self, 'original_set_name') and self.original_set_name
            original_name = self.original_set_name if is_editing else "None"
            print(f"DEBUG: Saving - Editing: {is_editing}, Original: '{original_name}', New: '{self.name_input.text().strip()}'")
            
            # Collect flashcard data from the form
            self.flashcards = []
            set_name = self.name_input.text().strip()
            
            # Validate set name
            if not set_name:
                self.show_warning_message("Missing Set Name", "Please enter a name for your flashcard set.")
                return
            
            # Count valid flashcards
            valid_cards = 0
            for i in range(self.scroll_layout.count()):
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
                            valid_cards += 1
            
            # Validate we have at least 4 flashcards
            if valid_cards < 4:
                self.show_warning_message("Not Enough Flashcards", 
                                        f"You need at least 4 flashcards. You currently have {valid_cards} valid card(s).")
                return
            
            # Use controller to save the flashcard set
            from core.controller import FlashcardController
            controller = FlashcardController()
            
            # CHECK IF WE'RE UPDATING AN EXISTING SET
            if hasattr(self, 'original_set_name') and self.original_set_name:
                print(f"DEBUG: Updating set - deleting original: '{self.original_set_name}'")
                
                # Always delete the original set first when editing
                delete_error = controller.delete_flashcard_set(self.original_set_name)
                
                if delete_error:
                    self.show_warning_message("Update Error", f"Failed to update flashcard set:\n{delete_error}")
                    return
                
                # Then create the updated set
                error_message = controller.create_flashcard_set(set_name, self.flashcards)
                
                # Clear the original set name after successful update
                if not error_message:
                    print(f"DEBUG: Successfully updated set to: '{set_name}'")
                    self.original_set_name = None
            else:
                print(f"DEBUG: Creating new set: '{set_name}'")
                # Original create new set logic
                error_message = controller.create_flashcard_set(set_name, self.flashcards)
            
            if error_message:
                self.show_warning_message("Save Error", f"Failed to save flashcard set:\n{error_message}")
            else:
                # SUCCESS MESSAGE BOX
                self.show_save_success(set_name, len(self.flashcards))
                self.reset_form()
                
                # IMPORTANT: Refresh the AllCards page to show updated sets
                self.refresh_all_cards_page()

        except Exception as e:
            self.show_warning_message("Critical Error", f"The app encountered an error:\n{str(e)}")

    def refresh_all_cards_page(self):
        """Refresh the AllCards page to show updated flashcard sets"""
        # Find the AllCards page in the main window stack
        all_cards_page = None
        for i in range(self.main_window.pages_stack.count()):
            widget = self.main_window.pages_stack.widget(i)
            if hasattr(widget, '__class__') and widget.__class__.__name__ == 'AllCards':
                all_cards_page = widget
                break
        
        if all_cards_page and hasattr(all_cards_page, 'load_flashcards'):
            all_cards_page.load_flashcards()

    def show_warning_message(self, title, message):
        """Helper method to show warning messages"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStyleSheet(self.styles["warning_message_box"])
        msg_box.setIcon(QMessageBox.Icon.Warning)
        
        # Load custom icon
        icon_path = get_asset_path("warning_icon.png")  
        custom_icon = QPixmap(icon_path)
        
        if not custom_icon.isNull():
            screen = self.main_window.screen()
            screen_size = screen.availableGeometry()
            icon_size = int(min(screen_size.width(), screen_size.height()) * 0.05)
            msg_box.setIconPixmap(custom_icon.scaled(icon_size, icon_size, Qt.AspectRatioMode.KeepAspectRatio))
        
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

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
            # RESPONSIVE ICON SCALING
            screen = self.main_window.screen()
            screen_size = screen.availableGeometry()
            icon_size = int(min(screen_size.width(), screen_size.height()) * 0.04)  # 4% of screen
            msg_box.setIconPixmap(custom_icon.scaled(icon_size, icon_size, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            msg_box.setIcon(QMessageBox.Icon.Information)
        
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def show_reset_warning(self):
        # Show custom warning dialog for reset action
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirm Reset")
        msg_box.setText("Are you sure you want to reset?")
        msg_box.setInformativeText("All unsaved changes will be lost.")
        
        # Apply the warning style
        msg_box.setStyleSheet(self.styles["warning_message_box"])
        
        # Load custom icon using path helper
        icon_path = get_asset_path("warning_icon.png")
        custom_icon = QPixmap(icon_path)
        
        if not custom_icon.isNull():
            # RESPONSIVE ICON SCALING
            screen = self.main_window.screen()
            screen_size = screen.availableGeometry()
            icon_size = int(min(screen_size.width(), screen_size.height()) * 0.06)  # 6% of screen
            msg_box.setIconPixmap(custom_icon.scaled(icon_size, icon_size, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            msg_box.setIcon(QMessageBox.Icon.Warning)
        
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        
        if msg_box.exec() == QMessageBox.StandardButton.Yes:
            self.reset_form()

    def reset_form(self):
        # Reset the form to 4 empty flashcards
        # Remove all existing card frames
        for i in range(self.scroll_layout.count() - 1, -1, -1):
            item = self.scroll_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, QFrame) and hasattr(widget, 'question_input'):
                    self.scroll_layout.removeWidget(widget)
                    widget.deleteLater()
        
        # Clear set name
        self.name_input.clear()
        
        # Reset card counter
        self.current_card_number = 1
        
        # Clear original set name when resetting
        if hasattr(self, 'original_set_name'):
            self.original_set_name = None
        
        # Create 4 new flashcards
        self.create_flashcard_inputs()

    def go_back(self):
        # Simply go back to main page without warning
        self.main_window.show_page(0)