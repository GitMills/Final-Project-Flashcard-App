# FINAL PROJECT FLASHCARD APP / ui / pages / all_cards_page.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, 
                            QPushButton, QMessageBox, QFrame, QScrollArea, QGridLayout, QDialog, QApplication)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from ui.visual.styles.styles import get_all_cards_styles
from ui.pages.flashcard_study_multiple_choice_page import MultipleChoiceStudy
from utils.path_helper import get_asset_path

class AllCards(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.styles = get_all_cards_styles()
        self.setup_ui()  # Setup UI first
        self.load_flashcards()  # Then load data
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("All Flashcard Sets")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(self.styles["title"])
        layout.addWidget(title)
        
        # Refresh button
        refresh_layout = QHBoxLayout()
        refresh_layout.setContentsMargins(20, 0, 0, 0)
        
        self.refresh_btn = QPushButton()
        self.refresh_btn.setStyleSheet(self.styles["refresh_button"])
        self.refresh_btn.clicked.connect(self.load_flashcards)

        # Add icon INSIDE the button using QIcon
        refresh_icon_path = get_asset_path("refresh.png")
        if refresh_icon_path:
            self.refresh_btn.setIcon(QIcon(refresh_icon_path))

        # This makes the icons consistent to all screen sizes
        screen = self.main_window.screen()
        screen_size = screen.availableGeometry()
        icon_size = int(min(screen_size.width(), screen_size.height()) * 0.04)  # 4% of screen
        self.refresh_btn.setIconSize(QSize(icon_size, icon_size))

        refresh_layout.addWidget(self.refresh_btn)
        refresh_layout.addStretch()  # Makes the button not all the way up to the end of the screen
        layout.addLayout(refresh_layout)
        
        # Scroll area for flashcard sets
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(self.styles["scroll_area"])
        
        # Container for flashcard set cards - THIS CREATES self.sets_layout
        self.sets_container = QWidget()
        self.sets_layout = QGridLayout(self.sets_container)  # This is crucial!
        self.sets_layout.setSpacing(15)
        self.sets_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.scroll_area.setWidget(self.sets_container)
        layout.addWidget(self.scroll_area)
        
        self.setLayout(layout)
    
    def load_flashcards(self):
        try:
            # Clear existing sets - now self.sets_layout exists
            for i in reversed(range(self.sets_layout.count())):
                widget = self.sets_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            
            # Import and use controller to load saved sets
            from core.controller import FlashcardController
            controller = FlashcardController()
            all_sets = controller.get_all_sets()
            
            if not all_sets:
                # Create container
                no_sets_container = QWidget()
                no_sets_layout = QVBoxLayout(no_sets_container)
                no_sets_layout.setSpacing(10)
                no_sets_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Add top stretch to push content down to vertical center
                no_sets_layout.addStretch()
                
                # Refresh icon
                icon_btn = QPushButton()
                icon_btn.clicked.connect(self.load_flashcards)
                
                no_sets_icon_path = get_asset_path("warning_icon.png")
                if no_sets_icon_path:
                    icon_btn.setIcon(QIcon(no_sets_icon_path))
                    screen = self.main_window.screen()
                    screen_size = screen.availableGeometry()
                    icon_size = int(min(screen_size.width(), screen_size.height()) * 0.1)  # 10% of screen
                    icon_btn.setIconSize(QSize(icon_size, icon_size))            
                no_sets_layout.addWidget(icon_btn)
                
                # Text message
                no_sets_label = QLabel("No flashcard sets found.\nCreate some flashcards first!")
                no_sets_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                no_sets_label.setStyleSheet(self.styles["no_sets_label"])
                no_sets_layout.addWidget(no_sets_label)
                
                # Add bottom stretch to push content up to vertical center
                no_sets_layout.addStretch()
                
                self.sets_layout.addWidget(no_sets_container, 0, 0)
                return
            
            # Add each set as a styled card
            row, col = 0, 0
            for flashcard_set in all_sets:
                set_card = self.create_set_card(flashcard_set)
                self.sets_layout.addWidget(set_card, row, col)
                
                col += 1
                if col > 1:  # 2 cards per row
                    col = 0
                    row += 1
                    
        except Exception as e:
            error_label = QLabel(f"Error loading flashcards:\n{str(e)}")
            error_label.setStyleSheet(self.styles["error_label"])
            self.sets_layout.addWidget(error_label)
        
    def create_set_card(self, flashcard_set):
        # Create a styled card for a flashcard set
        card_frame = QFrame()
        card_frame.setStyleSheet(self.styles["card_frame"])
        card_frame.setMinimumWidth(200)
        
        card_layout = QVBoxLayout(card_frame)
        card_layout.setSpacing(10)
        card_layout.setContentsMargins(15, 15, 15, 15)
        
        # Set name
        name_label = QLabel(flashcard_set['set_name'])
        name_label.setStyleSheet(self.styles["card_name"])
        name_label.setWordWrap(True)
        card_layout.addWidget(name_label)
        
        # Set info
        info_text = f"Cards: {len(flashcard_set['cards'])}\nCreated: {flashcard_set['created_date']}"
        info_label = QLabel(info_text)
        info_label.setStyleSheet(self.styles["info_label"])
        card_layout.addWidget(info_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        # Study button
        study_btn = QPushButton("Study")
        study_btn.setStyleSheet(self.styles["study_button"])
        study_btn.clicked.connect(lambda: self.study_set(flashcard_set))
        button_layout.addWidget(study_btn)
        
        # Delete button
        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet(self.styles["delete_button"])
        delete_btn.clicked.connect(lambda: self.delete_set(flashcard_set['set_name']))
        button_layout.addWidget(delete_btn)
        
        card_layout.addLayout(button_layout)
        
        return card_frame
    
    def study_set(self, flashcard_set):
        print(f"Study set clicked: {flashcard_set['set_name']}")  

        # Show study options for this flashcard set
        try:
            from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
            
            study_dialog = QDialog(self)
            study_dialog.setWindowTitle("Choose Study Mode")
            
            layout = QVBoxLayout()
            
            # Title
            title = QLabel(f"Study: {flashcard_set['set_name']}")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title.setStyleSheet(self.styles["title"])
            layout.addWidget(title)
            
            # Cards count info
            cards_info = QLabel(f"Cards in set: {len(flashcard_set['cards'])}")
            cards_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cards_info.setStyleSheet(self.styles["cards_info"])
            layout.addWidget(cards_info)
            
            # Buttons layout
            buttons_layout = QVBoxLayout()
            buttons_layout.setSpacing(10)
            
            # Flip Card button
            flip_btn = QPushButton("Flip Cards")
            flip_btn.setStyleSheet(self.styles["mc_button"])
            flip_btn.clicked.connect(lambda: self.start_flip_card_study(flashcard_set, study_dialog))
            buttons_layout.addWidget(flip_btn)
            
            # Multiple Choice button
            mc_btn = QPushButton("Multiple Choice")
            
            # Check if enough cards for multiple choice
            if len(flashcard_set['cards']) < 4:
                mc_btn.clicked.connect(lambda: self.show_mc_warning(study_dialog))
            else:
                mc_btn.setStyleSheet(self.styles["mc_button"])
                mc_btn.clicked.connect(lambda: self.start_multiple_choice_study(flashcard_set, study_dialog))
            
            buttons_layout.addWidget(mc_btn)
            
            # Cancel button
            cancel_btn = QPushButton("Cancel")
            cancel_btn.setStyleSheet(self.styles["delete_button"])
            cancel_btn.clicked.connect(study_dialog.reject)
            buttons_layout.addWidget(cancel_btn)
            
            layout.addLayout(buttons_layout)
            study_dialog.setLayout(layout)
            
            study_dialog.exec()
                    
        except Exception as e:
            import traceback
            traceback.print_exc()

    def show_mc_warning(self, dialog):
        # Show warning when not enough cards for multiple choice
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.warning(
            self, 
            "Not Enough Cards", 
            "Multiple Choice mode requires at least 4 cards in the set.\n\n"
            "Please add more cards to use this study mode."
        )
        # Don't close the dialog - let user choose another option

    def start_flip_card_study(self, flashcard_set, dialog):
        # Start flip card study
        dialog.accept()
        self.main_window.show_flashcard_study_with_set(flashcard_set)

    def start_multiple_choice_study(self, flashcard_set, dialog):
        # Start multiple choice study
        dialog.accept()
        self.main_window.show_multiple_choice_study(flashcard_set)
    
    def delete_set(self, set_name):
        # Create message box
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirm Delete")
        msg_box.setText(f"Are you sure you want to delete '{set_name}'?")
        
        # Add custom icon
        delete_icon_path = get_asset_path("warning_icon.png")
        if delete_icon_path:
            custom_icon = QPixmap(delete_icon_path)
            if not custom_icon.isNull():
                # RESPONSIVE ICON SCALING - 5% of screen size
                screen = self.main_window.screen()
                screen_size = screen.availableGeometry()
                icon_size = int(min(screen_size.width(), screen_size.height()) * 0.05)  # 5% of screen
                msg_box.setIconPixmap(custom_icon.scaled(icon_size, icon_size, Qt.AspectRatioMode.KeepAspectRatio))
        
        # Set buttons and style
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        msg_box.setStyleSheet(self.styles["warning_message_box"])
        
        # Show dialog
        reply = msg_box.exec()
        
        if reply == QMessageBox.StandardButton.Yes:
            from core.controller import FlashcardController
            controller = FlashcardController()
            
            error_message = controller.delete_flashcard_set(set_name)
            
            if error_message:
                QMessageBox.critical(self, "Delete Error", f"Failed to delete set:\n{error_message}")
            else:
                QMessageBox.information(self, "Success", f"Flashcard set '{set_name}' deleted successfully!")
                self.load_flashcards()