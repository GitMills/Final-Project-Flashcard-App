# FINAL PROJECT FLASHCARD APP / ui / main_window.py

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QFrame, QStackedWidget, QLabel
)

from PyQt6.QtCore import QTimer

# Import our page classes
from ui.pages.home_page import HomePage
from ui.pages.profile_page import ProfilePage
from ui.pages.settings_page import SettingsPage
from ui.pages.help_page import HelpPage
from ui.pages.all_cards_page import AllCards
from ui.pages.create_flashcard_page import CreateFlashcard
from ui.pages.existing_flashcard_page import ExistingFlashcard
from ui.pages.flashcard_study_page import FlashcardStudyPage
from ui.components.pomodoro_timer import PomodoroTimer
from ui.pages.flashcard_study_multiple_choice_page import MultipleChoiceStudy

# Import our visual classes
from ui.visual.animations import SidebarAnimations
from ui.visual.styles.styles import get_sidebar_styles, get_main_window_styles

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.sidebar_collapsed = True
        self.sidebar_styles = get_sidebar_styles()
        self.main_styles = get_main_window_styles()
        
        # Initialize timer first
        self.pomodoro_timer = PomodoroTimer(self)
        
        self.setup_ui()
        self.setup_animation()

    def setup_ui(self):
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setStyleSheet(self.main_styles["main_layout"])

        # Create sidebar
        self.sidebar = QFrame()
        self.sidebar.setMinimumWidth(0)
        self.sidebar.setMaximumWidth(0)
        self.sidebar.setStyleSheet(self.sidebar_styles["sidebar_collapsed"])
        self.setup_sidebar_content()

        # Create main content widget
        self.main_content_widget = QWidget()
        main_content_layout = QVBoxLayout(self.main_content_widget)
        main_content_layout.setContentsMargins(0, 0, 0, 0)
        main_content_layout.setSpacing(0)

        # Header with timer display
        header_layout = QHBoxLayout()
        
        # Burger button
        self.toggle_btn = QPushButton("☰")
        self.toggle_btn.setMinimumSize(45, 45)
        self.toggle_btn.setStyleSheet(self.sidebar_styles["toggle_button"])
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        header_layout.addWidget(self.toggle_btn)

        # Timer display (top-right) - START HIDDEN
        header_layout.addStretch()
        self.timer_display = QLabel("Study: 25:00")
        self.timer_display.setStyleSheet("color: #A6E3A1; font-size: 14px; font-weight: bold; padding: 10px;")
        self.timer_display.setVisible(False)  # START HIDDEN
        header_layout.addWidget(self.timer_display)

        # Pomodoro control button - START HIDDEN
        self.pomodoro_btn = QPushButton("▶ Start Timer")
        self.pomodoro_btn.setMinimumSize(100, 35)
        self.pomodoro_btn.setStyleSheet("""
            QPushButton {
                background-color: #A6E3A1;
                color: #1E1E2E;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #94D2A2;
            }
        """)
        self.pomodoro_btn.clicked.connect(self.toggle_pomodoro_timer)
        self.pomodoro_btn.setVisible(False)  # START HIDDEN
        header_layout.addWidget(self.pomodoro_btn)

        # Timer settings button - START HIDDEN
        self.timer_settings_btn = QPushButton("⚙")
        self.timer_settings_btn.setMinimumSize(35, 35)
        self.timer_settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #585B70;
                color: #CDD6F4;
                border: none;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6C7086;
            }
        """)
        self.timer_settings_btn.clicked.connect(self.show_timer_settings)
        self.timer_settings_btn.setVisible(False)  # START HIDDEN
        header_layout.addWidget(self.timer_settings_btn)

        # Create stacked widget
        self.pages_stack = QStackedWidget()
        self.create_pages()

        # Add to main layout
        main_content_layout.addLayout(header_layout)
        main_content_layout.addWidget(self.pages_stack)

        # Add sidebar and main content to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.main_content_widget)

        self.setLayout(main_layout)
        self.setWindowTitle("Remora")

    def update_timer_display(self, text):
        # Update the timer display text
        self.timer_display.setText(text)
        
        current_page = self.pages_stack.currentIndex()
        non_learning_pages = [0, 1, 2, 4]  # Home, Profile, Settings, Help
        
        if current_page in non_learning_pages:
            # Special behavior for pages 0,1,2,4
            if self.pomodoro_timer.timer_running:
                # Timer running: show only timer display, hide buttons
                self.timer_display.setVisible(True)
                self.pomodoro_btn.setVisible(False)
                self.timer_settings_btn.setVisible(False)
            else:
                # Timer NOT running: hide everything
                self.timer_display.setVisible(False)
                self.pomodoro_btn.setVisible(False)
                self.timer_settings_btn.setVisible(False)
        else:
            # Other pages: always show everything
            self.timer_display.setVisible(True)
            self.pomodoro_btn.setVisible(True)
            self.timer_settings_btn.setVisible(True)
    
    def setup_sidebar_content(self):
        # Create a layout for the sidebar box
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(10, 20, 10, 20)  # Padding inside the box 
        sidebar_layout.setSpacing(10)
        
        # Navigation buttons - these will be INSIDE the sidebar box
        nav_texts = ["Home", "Profile", "Settings", "Saved Cards", "Help"]
        self.nav_buttons = []
        
        for i, text in enumerate(nav_texts):
            btn = QPushButton(text)  # Show text immediately
            btn.setMinimumHeight(40)
            btn.setStyleSheet(self.sidebar_styles["nav_button_expanded"])
            btn.clicked.connect(lambda checked, idx=i: self.navigate_to_page(idx))
            self.nav_buttons.append(btn)
            sidebar_layout.addWidget(btn)
        
        sidebar_layout.addStretch()
        self.sidebar.setLayout(sidebar_layout)
    
    def create_pages(self):
        # Create instances of our separate page classes and pass main window reference
        self.home_page = HomePage(self)  # Pass self (MainWindow) as reference
        self.profile_page = ProfilePage()
        self.settings_page = SettingsPage()
        self.help_page = HelpPage()
        self.all_cards_page = AllCards(self)
        self.create_flashcard_page = CreateFlashcard(self)
        self.existing_flashcard_page = ExistingFlashcard(self)
        self.flashcard_study_page = FlashcardStudyPage(self, None)
        self.multiple_choice_study_page = MultipleChoiceStudy(self, None) 

        self.pages_stack.addWidget(self.home_page)         # index 0
        self.pages_stack.addWidget(self.profile_page)      # index 1
        self.pages_stack.addWidget(self.settings_page)     # index 2
        self.pages_stack.addWidget(self.all_cards_page)    # index 3
        self.pages_stack.addWidget(self.help_page)          # index 4
        self.pages_stack.addWidget(self.create_flashcard_page) # index 5
        self.pages_stack.addWidget(self.existing_flashcard_page) # index 6
        self.pages_stack.addWidget(self.flashcard_study_page) # index 7
        self.pages_stack.addWidget(self.multiple_choice_study_page) # index 8

    def setup_animation(self):
        # Initialize animations
        self.sidebar_animations = SidebarAnimations(self.sidebar)
    
    def toggle_sidebar(self):
        if self.sidebar_collapsed:
            self.expand_sidebar()
        else:
            self.collapse_sidebar()
    
    def expand_sidebar(self):
        # Apply expanded styles and expand the sidebar box
        self.sidebar.setStyleSheet(self.sidebar_styles["sidebar_expanded"])
        self.sidebar_animations.expand_sidebar(0, 200)
        self.sidebar_collapsed = False
    
    def collapse_sidebar(self):
        # Apply collapsed styles and collapse the sidebar box
        self.sidebar.setStyleSheet(self.sidebar_styles["sidebar_collapsed"])
        self.sidebar_animations.collapse_sidebar(200, 0)
        self.sidebar_collapsed = True
    
    def navigate_to_page(self, page_index):
        self.show_page(page_index)
        if not self.sidebar_collapsed:
            self.collapse_sidebar()
    
    def show_page(self, page_index):
        self.pages_stack.setCurrentIndex(page_index)
        # Update timer visibility when page changes
        self.update_timer_display(self.timer_display.text())
    
    # NEW PAGES THROUGH BUTTONS
    def show_existing_flashcards(self):
        # Show the Existing Flashcard page (index 6)
        self.show_page(6)  # Existing Flashcards is at index 6
        if not self.sidebar_collapsed:
            self.collapse_sidebar()
    
    def show_create_flashcard(self):
        # Show the create_flashcard_page page (index 5) 
        self.show_page(5)  # Create Flashcards is at index 5
        if not self.sidebar_collapsed:
            self.collapse_sidebar()

    def show_flashcard_study_with_set(self, flashcard_set):
        # Update study page with specific flashcard set and show it
        try:
            # Simply update the existing study page and show it
            self.flashcard_study_page.flashcard_set = flashcard_set
            self.flashcard_study_page.current_card_index = 0
            self.flashcard_study_page.is_flipped = False
            
            # UPDATE THE SET NAME LABEL
            self.flashcard_study_page.set_name_label.setText(flashcard_set['set_name'])
            
            self.flashcard_study_page.load_card(0)
            
            self.show_page(7)
            
            if not self.sidebar_collapsed:
                self.collapse_sidebar()
                
        except Exception as e:
            print(f"Error: {e}")

    def toggle_pomodoro_timer(self):
        # Toggle between start and pause for the Pomodoro timer
        if self.pomodoro_timer.timer_running:
            # Timer is running, so pause it
            if self.pomodoro_timer.pause_timer():
                self.pomodoro_btn.setText("▶ Resume")
        else:
            # Timer is paused/stopped, so start it
            if self.pomodoro_timer.start_timer():
                self.pomodoro_btn.setText("⏸ Pause")
        
        # Update visibility after toggle
        self.update_timer_display(self.timer_display.text())

    def show_timer_settings(self):
        # Show the Pomodoro timer settings dialog
        self.pomodoro_timer.show_settings(self)

    def show_multiple_choice_study(self, flashcard_set):
        # Show multiple choice study interface
        try:            
            # Update the existing multiple choice page with the flashcard set
            self.multiple_choice_study_page.update_flashcard_set(flashcard_set)
            
            # Show the multiple choice page
            self.pages_stack.setCurrentIndex(8)  
            
            if not self.sidebar_collapsed:
                self.collapse_sidebar()
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Failed to start multiple choice: {str(e)}")