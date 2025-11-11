# FINAL PROJECT FLASHCARD APP / ui / pages / create_flashcard_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QScrollArea, QFrame, QMessageBox
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap
from ui.visual.styles.styles import get_create_flashcard_styles, get_inline_label_styles
from utils.path_helper import get_asset_path


class CreateFlashcard(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.flashcards = []  # Store flashcards
        self.current_card_number = 1  # Track card numbers
        self.styles = get_create_flashcard_styles()
        self.label_styles = get_inline_label_styles()
        self.has_unsaved_changes = False  # Track unsaved changes
        self.setup_ui()
    
    def setup_ui(self):
        # Main layout - no right margin for scrollbar
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(85, 0, 0, 0) # Left, top, Right (0 for scrollbar), Bottom
        self.setLayout(main_layout)
        
        # Scroll area for all content (title, set name, flashcards)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Content widget that goes inside the scroll area
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(15)
        self.scroll_layout.setContentsMargins(20, 20, 105, 200)  # Extra right (105) and bottom (200) space for buttons
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Page title
        self.title = QLabel("Create New Flashcard")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet(self.styles["title"])
        self.scroll_layout.addWidget(self.title)
        
        # Edit mode indicator banner (initially hidden)
        self.edit_mode_banner = QLabel("📝 Editing Mode - Changes will update the existing set")
        self.edit_mode_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_mode_banner.setStyleSheet(self.label_styles["edit_mode_banner"])
        self.edit_mode_banner.hide()
        self.scroll_layout.addWidget(self.edit_mode_banner)

        # Flashcard set name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Set Name")
        self.name_input.setStyleSheet(self.styles["name_input"])
        self.name_input.textChanged.connect(self.mark_unsaved_changes)
        self.scroll_layout.addWidget(self.name_input)
        
        # Difficulty level selection
        difficulty_layout = QHBoxLayout()
        difficulty_layout.setSpacing(10)
        difficulty_layout.setContentsMargins(5, 10, 5, 10)
        
        difficulty_label = QLabel("Difficulty Level:")
        difficulty_label.setStyleSheet(self.styles["difficulty_label"])
        difficulty_layout.addWidget(difficulty_label)
        
        # Difficulty buttons
        from PyQt6.QtWidgets import QButtonGroup
        self.difficulty_group = QButtonGroup()
        
        self.easy_btn = QPushButton("Easy")
        self.easy_btn.setCheckable(True)
        self.easy_btn.setChecked(True)  # Default to Easy
        self.easy_btn.setStyleSheet(self.styles["difficulty_button_easy"])
        
        self.medium_btn = QPushButton("Medium")
        self.medium_btn.setCheckable(True)
        self.medium_btn.setStyleSheet(self.styles["difficulty_button_medium"])
        
        self.hard_btn = QPushButton("Hard")
        self.hard_btn.setCheckable(True)
        self.hard_btn.setStyleSheet(self.styles["difficulty_button_hard"])
        
        self.difficulty_group.addButton(self.easy_btn, 1)
        self.difficulty_group.addButton(self.medium_btn, 2)
        self.difficulty_group.addButton(self.hard_btn, 3)
        
        difficulty_layout.addWidget(self.easy_btn)
        difficulty_layout.addWidget(self.medium_btn)
        difficulty_layout.addWidget(self.hard_btn)
        difficulty_layout.addStretch()
        
        self.scroll_layout.addLayout(difficulty_layout)
        
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
        self.floating_button_container.setStyleSheet(self.styles["floating_button_container"])
        
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
        # Account for scrollbar width (20px)
        self.floating_button_container.setGeometry(0, self.height() - 150, self.width() - 20, 150)
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
        question_input.textChanged.connect(self.mark_unsaved_changes)
        
        # Answer input field (text area for longer answers)
        answer_input = QTextEdit()
        answer_input.setPlaceholderText("Enter Answer")
        answer_input.setMaximumHeight(80)
        answer_input.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        answer_input.setStyleSheet(self.styles["answer_input"])
        answer_input.textChanged.connect(self.mark_unsaved_changes)
        
        # Custom hint input field (optional)
        hint_input = QLineEdit()
        hint_input.setPlaceholderText("💡 Custom Hint (Optional - leave empty for auto hint)")
        hint_input.setStyleSheet(self.styles["hint_input"])
        hint_input.textChanged.connect(self.mark_unsaved_changes)
        
        # Store references to inputs for later access
        card_frame.question_input = question_input
        card_frame.answer_input = answer_input
        card_frame.hint_input = hint_input
        card_frame.card_number = self.current_card_number
        
        # Add widgets to card layout
        card_layout.addLayout(card_header)
        card_layout.addWidget(question_input)  
        card_layout.addWidget(answer_input)
        card_layout.addWidget(hint_input)    
        
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
    
    def _scroll_to_top(self):
        # Scroll to top instantly to show title
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(0)

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
                        hint = widget.hint_input.text().strip() if hasattr(widget, 'hint_input') else ''
                        
                        if question and answer:
                            card_data = {
                                'question': question,
                                'answer': answer
                            }
                            # Add custom hint if provided
                            if hint:
                                card_data['custom_hint'] = hint
                            self.flashcards.append(card_data)
                            valid_cards += 1
            
            # Validate we have at least 4 flashcards
            if valid_cards < 4:
                self.show_warning_message("Not Enough Flashcards", 
                                        f"You need at least 4 flashcards. You currently have {valid_cards} valid card(s).")
                return
            
            # Get difficulty level
            difficulty = 'Easy'
            if self.medium_btn.isChecked():
                difficulty = 'Medium'
            elif self.hard_btn.isChecked():
                difficulty = 'Hard'
            
            # Use controller to save the flashcard set
            from core.controller import FlashcardController
            controller = FlashcardController()
            
            # CHECK IF WE'RE UPDATING AN EXISTING SET
            was_editing = hasattr(self, 'original_set_name') and self.original_set_name
            
            if was_editing:
                print(f"DEBUG: Updating set - deleting original: '{self.original_set_name}'")
                
                # Always delete the original set first when editing
                delete_error = controller.delete_flashcard_set(self.original_set_name)
                
                if delete_error:
                    self.show_warning_message("Update Error", f"Failed to update flashcard set:\n{delete_error}")
                    return
                
                # Then create the updated set with difficulty
                error_message = controller.create_flashcard_set(set_name, self.flashcards, difficulty)
                
                # Update original_set_name to the new name (in case it was renamed)
                if not error_message:
                    print(f"DEBUG: Successfully updated set to: '{set_name}'")
                    self.original_set_name = set_name  # Keep in edit mode with new name
            else:
                print(f"DEBUG: Creating new set: '{set_name}'")
                # Original create new set logic with difficulty
                error_message = controller.create_flashcard_set(set_name, self.flashcards, difficulty)
            
            if error_message:
                self.show_warning_message("Save Error", f"Failed to save flashcard set:\n{error_message}")
            else:
                # SUCCESS MESSAGE BOX
                self.show_save_success(set_name, len(self.flashcards))
                self.has_unsaved_changes = False  # Clear unsaved changes flag
                
                # Check if we were editing - if so, reload the edited set to stay in edit mode
                was_editing = hasattr(self, 'original_set_name') and self.original_set_name
                
                if was_editing:
                    # Reload the updated set to continue editing
                    from core.controller import FlashcardController
                    controller = FlashcardController()
                    updated_set = controller.get_study_set(set_name)
                    if updated_set:
                        self.load_flashcards_for_editing(updated_set)
                else:
                    # Only reset if creating new (not editing)
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
        
        # Reset title to create mode
        self.title.setText("Create New Flashcard")
        self.edit_mode_banner.hide()
        
        # Reset save button text
        self.save_btn.setText("Save Flashcard")
        
        # Reset button back to Reset (not Discard Changes)
        self.reset_btn.setText("Reset")
        try:
            self.reset_btn.clicked.disconnect()
        except:
            pass
        self.reset_btn.clicked.connect(self.show_reset_warning)
        
        # Reset difficulty to Easy
        self.easy_btn.setChecked(True)
        
        # Clear unsaved changes flag
        self.has_unsaved_changes = False
        
        # Create 4 new flashcards
        self.create_flashcard_inputs()
        
        # Scroll to top to show title
        self._scroll_to_top()

    def mark_unsaved_changes(self):
        """Mark that there are unsaved changes"""
        self.has_unsaved_changes = True
    
    def load_flashcards_for_editing(self, flashcard_set):
        """Load existing flashcard set for editing"""
        try:
            # Clear existing form
            self.reset_form()
            
            # Set edit mode
            self.title.setText("Edit/View Flashcard")
            self.edit_mode_banner.show()
            self.save_btn.setText("Update Flashcard")
            
            # Replace Reset button with Discard Changes button
            self.reset_btn.setText("Discard Changes")
            self.reset_btn.clicked.disconnect()
            self.reset_btn.clicked.connect(self.discard_changes)
            
            # Set the flashcard set name
            self.name_input.setText(flashcard_set['set_name'])
            
            # Set difficulty level
            difficulty = flashcard_set.get('difficulty', 'Easy')
            if difficulty == 'Easy':
                self.easy_btn.setChecked(True)
            elif difficulty == 'Medium':
                self.medium_btn.setChecked(True)
            else:  # Hard
                self.hard_btn.setChecked(True)
            
            # Remove the initial 4 empty cards
            for i in range(self.scroll_layout.count() - 1, -1, -1):
                item = self.scroll_layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    if isinstance(widget, QFrame) and hasattr(widget, 'question_input'):
                        self.scroll_layout.removeWidget(widget)
                        widget.deleteLater()
            
            # Reset card counter
            self.current_card_number = 1
            
            # Add cards from the existing set
            for card in flashcard_set['cards']:
                self.add_flashcard_input()
                
                # Get the most recently added card frame
                last_item = self.scroll_layout.itemAt(self.scroll_layout.count() - 1)
                if last_item and last_item.widget():
                    card_frame = last_item.widget()
                    if hasattr(card_frame, 'question_input') and hasattr(card_frame, 'answer_input'):
                        # Populate with existing data
                        card_frame.question_input.setText(card['question'])
                        card_frame.answer_input.setPlainText(card['answer'])
                        # Load custom hint if exists
                        if hasattr(card_frame, 'hint_input') and 'custom_hint' in card:
                            card_frame.hint_input.setText(card.get('custom_hint', ''))
            
            # Store the original set name for update purposes
            self.original_set_name = flashcard_set['set_name']
            
            # Clear unsaved changes flag (we just loaded)
            self.has_unsaved_changes = False
            
            # Scroll to top to show title and set name
            self._scroll_to_top()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load flashcards for editing: {str(e)}")
    
    def discard_changes(self):
        """Discard changes and reload original flashcard set"""
        if not hasattr(self, 'original_set_name') or not self.original_set_name:
            return
        
        # Show confirmation dialog
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Discard Changes")
        msg_box.setText("Are you sure you want to discard all changes?")
        msg_box.setInformativeText("This will reload the last saved version.")
        msg_box.setStyleSheet(self.styles["warning_message_box"])
        
        # Add custom icon
        icon_path = get_asset_path("warning_icon.png")
        if icon_path:
            custom_icon = QPixmap(icon_path)
            if not custom_icon.isNull():
                screen = self.main_window.screen()
                screen_size = screen.availableGeometry()
                icon_size = int(min(screen_size.width(), screen_size.height()) * 0.05)
                msg_box.setIconPixmap(custom_icon.scaled(icon_size, icon_size, Qt.AspectRatioMode.KeepAspectRatio))
        
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        
        if msg_box.exec() == QMessageBox.StandardButton.Yes:
            # Reload the original flashcard set
            from core.controller import FlashcardController
            controller = FlashcardController()
            flashcard_set = controller.get_study_set(self.original_set_name)
            
            if flashcard_set:
                self.load_flashcards_for_editing(flashcard_set)
    
    def go_back(self):
        """Go back with unsaved changes warning"""
        # Determine where to go back to
        if hasattr(self, 'original_set_name') and self.original_set_name:
            back_page = 3  # All Cards page when editing
        else:
            back_page = 0  # Home page when creating
        
        if self.has_unsaved_changes:
            # Show warning dialog
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Unsaved Changes")
            msg_box.setText("You have unsaved changes. Are you sure you want to leave?")
            msg_box.setInformativeText("All unsaved changes will be lost.")
            msg_box.setStyleSheet(self.styles["warning_message_box"])
            
            # Add custom icon
            from utils.path_helper import get_asset_path
            from PyQt6.QtGui import QPixmap
            icon_path = get_asset_path("warning_icon.png")
            if icon_path:
                custom_icon = QPixmap(icon_path)
                if not custom_icon.isNull():
                    screen = self.main_window.screen()
                    screen_size = screen.availableGeometry()
                    icon_size = int(min(screen_size.width(), screen_size.height()) * 0.05)
                    msg_box.setIconPixmap(custom_icon.scaled(icon_size, icon_size, Qt.AspectRatioMode.KeepAspectRatio))
            
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg_box.setDefaultButton(QMessageBox.StandardButton.No)
            
            if msg_box.exec() == QMessageBox.StandardButton.Yes:
                self.has_unsaved_changes = False
                self.main_window.show_page(back_page)
        else:
            self.main_window.show_page(back_page)