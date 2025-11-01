from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QFrame, QStackedWidget
)


# Import our page classes
from ui.pages.home_page import HomePage
from ui.pages.profile_page import ProfilePage
from ui.pages.settings_page import SettingsPage
from ui.pages.help_page import HelpPage
from ui.pages.all_cards_page import AllCards
from ui.pages.create_flashcard_page import CreateFlashcard
from ui.pages.existing_flashcard_page import ExistingFlashcard

# Import our visual classes
from ui.visual.animations import SidebarAnimations
from ui.visual.styles.styles import get_sidebar_styles, get_main_window_styles

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.sidebar_collapsed = True
        self.sidebar_styles = get_sidebar_styles()
        self.main_styles = get_main_window_styles()
        self.setup_ui()
        self.setup_animation()
        
    def setup_ui(self):
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setStyleSheet(self.main_styles["main_layout"])       

        # Create sidebar as a solid frame/box
        self.sidebar = QFrame()
        self.sidebar.setMinimumWidth(0)  # Start collapsed
        self.sidebar.setMaximumWidth(0)
        self.sidebar.setStyleSheet(self.sidebar_styles["sidebar_collapsed"])
        
        self.setup_sidebar_content()
        
        # Create main content widget
        self.main_content_widget = QWidget()
        main_content_layout = QVBoxLayout(self.main_content_widget)
        main_content_layout.setContentsMargins(0, 0, 0, 0)
        main_content_layout.setSpacing(0)
        
        # Create and add burger button to main content
        self.toggle_btn = QPushButton("☰")
        self.toggle_btn.setFixedSize(45, 45)
        self.toggle_btn.setStyleSheet(self.sidebar_styles["toggle_button"])
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        
        # Create stacked widget for main app pages
        self.pages_stack = QStackedWidget()
        self.create_pages()
        
        # Add burger button and pages to main content
        main_content_layout.addWidget(self.toggle_btn)
        main_content_layout.addWidget(self.pages_stack)
        
        # Add sidebar and main content to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.main_content_widget)
        
        self.setLayout(main_layout)
        self.setWindowTitle("Remora")
        self.resize(1000, 800)
    
    def setup_sidebar_content(self):
        # Create a layout for the sidebar box
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(10, 20, 10, 20)  # Padding inside the box
        sidebar_layout.setSpacing(10)
        
        # Navigation buttons - these will be INSIDE the sidebar box
        nav_texts = ["Home", "Profile", "Settings", "All Cards", "Help"]
        self.nav_buttons = []
        
        for i, text in enumerate(nav_texts):
            btn = QPushButton(text)  # Show text immediately
            btn.setFixedHeight(40)
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
        self.all_cards_page = AllCards()
        self.create_flashcard_page = CreateFlashcard(self)
        self.existing_flashcard_page = ExistingFlashcard(self)

        
        self.pages_stack.addWidget(self.home_page)         # index 0
        self.pages_stack.addWidget(self.profile_page)      # index 1
        self.pages_stack.addWidget(self.settings_page)     # index 2
        self.pages_stack.addWidget(self.all_cards_page)    # index 3
        self.pages_stack.addWidget(self.help_page)          # index 4
        self.pages_stack.addWidget(self.create_flashcard_page) # index 5
        self.pages_stack.addWidget(self.existing_flashcard_page) # index 6
    
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
    
    # NEW METHODS FOR HOME PAGE BUTTONS
    def show_existing_flashcards(self):
        """Show the Existing Flashcard page (index 6)"""
        self.show_page(6)  # Existing Flashcards is at index 6
        if not self.sidebar_collapsed:
            self.collapse_sidebar()
    
    def show_create_flashcard(self):
        """Show the create_flashcard_page page (index 5) """
        self.show_page(5)  # Create Flashcards is at index 5
        if not self.sidebar_collapsed:
            self.collapse_sidebar()