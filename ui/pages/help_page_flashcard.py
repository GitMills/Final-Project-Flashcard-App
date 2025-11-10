from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class HelpPage(QWidget):
    """Simple standalone help page with information and back button."""
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("📖 Remora App Help")
        title.setFont(QFont("Arial Rounded MT Bold", 28))
        title.setStyleSheet("color: #434190;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        desc = QLabel("""
Welcome to the Remora Flashcard App!  
Here are some useful shortcuts and features:

🧠 **App Controls**
- **Ctrl + Q** → Quit the app  
- **Ctrl + S** → Save data  
- **Ctrl + F** → Open flashcard view  
- **Spacebar** → Flip flashcard  
- **Ctrl + Tab** → Switch tab  
- **F1** → Open this Help page  

🪄 **Tips**
- Use the sidebar ☰ to navigate pages.  
- You can switch between light 🌞 and dark 🌙 themes.  
- Add, edit, and review flashcards anytime!

Enjoy studying with Remora! 💪
""")
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignTop)
        desc.setStyleSheet("color: #555; font-size: 15px;")

        back_btn = QPushButton("⬅ Back to Main")
        back_btn.setFont(QFont("Arial Rounded MT Bold", 14))
        back_btn.setStyleSheet("background-color: #888; color: white; padding: 8px 20px; border-radius: 10px;")
        back_btn.clicked.connect(lambda: self.parent_window.help_page.fade_out(self.parent_window.main_page))

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addSpacing(20)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("background-color: #FFF6E9;")
