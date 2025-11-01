def get_sidebar_styles():
    return {
        "sidebar_collapsed": """
            QFrame {
                background-color: transparent;
                border: none;
            }
        """,
        
        "sidebar_expanded": """
            QFrame {
                background-color: #2c3e50;
                border: none;
            }
        """,
        
        "toggle_button": """
            QPushButton {
                background-color: #2c3e50;
                color: #FC483D;
                border: none;
                border-bottom-right-radius: 20px;
                font-size: 25px;
            }
            QPushButton:hover {
                background-color: #2c3e50;
            }
        """,
        
        "nav_button_collapsed": """
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                text-align: left;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgba(52, 73, 94, 0.7);
            }
        """,
        
        "nav_button_expanded": """
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                text-align: left;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """
    }


def get_main_window_styles():
    return {
        "main_layout": """
            background-color: #FFF5E5;
        """
    }


def home_page_styles():
    return {
        "home_button": """
            QPushButton {
                background-color: #FC483D;
                color: #FFF5E5;
                font-size: 33px;
                font-weight: 900;
                border-radius: 30px;
                padding: 14px 40px;
                min-height: 60px;
                min-width: 300px;
                max-width: 300x;
            }
            QPushButton:hover {
                background-color: #434190;
            }
        """
    }

def get_create_flashcard_styles():
    return {
        "title": """
            QLabel {
                font-size: 30px;
                font-weight: 900;
                color: #A2A8D3;
                padding: 15px 0;
                background-color: transparent;
                border: none;
            }
        """,

        "name_input": """
            QLineEdit {
                background-color: #C0D6BF;
                border: none;
                padding: 12px 15px;
                font-size: 14px;
                selection-background-color: none;
            }
            QLineEdit:focus {
                border: 2px solid #89B4FA;
                background-color: blue;
            }
        """,

        "card_frame": """
            QFrame {
                background-color: #F2E6D5;
                border-radius: 15px;
                padding: 20px;
                margin: 10px 5px;
                box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
            }
        """,

        "card_number": """
            QLabel {
                font-size: 16px;
                font-weight: 600;
                color: #89B4FA;
                padding: 5px 0;
                background-color: transparent;
                border: none;
            }
        """,

        "question_input": """
            QLineEdit {
                background-color: #313244;
                border: 2px solid #45475A;
                border-radius: 12px;
                padding: 12px 15px;
                font-size: 14px;
                color: #CDD6F4;
                selection-background-color: #585B70;
            }
            QLineEdit:focus {
                border: 2px solid #89B4FA;
                background-color: #313244;
            }
            QLineEdit::placeholder {
                color: #6C7086;
                font-style: italic;
            }
        """,

        "answer_input": """
            QTextEdit {
                background-color: #313244;
                border: 2px solid #45475A;
                border-radius: 12px;
                padding: 12px 15px;
                font-size: 14px;
                color: #CDD6F4;
                selection-background-color: #585B70;
            }
            QTextEdit:focus {
                border: 2px solid #89B4FA;
                background-color: #313244;
            }
            QTextEdit::placeholder {
                color: #6C7086;
                font-style: italic;
            }
        """,

        "add_button": """
            QPushButton {
                background-color: #585B70;
                color: #CDD6F4;
                font-size: 14px;
                font-weight: 600;
                border-radius: 12px;
                padding: 12px 20px;
                min-height: 45px;
                min-width: 140px;
                margin: 5px;
                border: 2px solid #6C7086;
            }
            QPushButton:hover {
                background-color: #6C7086;
                border: 2px solid #89B4FA;
            }
            QPushButton:pressed {
                background-color: #45475A;
            }
        """,

        "save_button": """
            QPushButton {
                background-color: #A6E3A1;
                color: #1E1E2E;
                font-size: 14px;
                font-weight: 700;
                border-radius: 12px;
                padding: 12px 20px;
                min-height: 45px;
                min-width: 140px;
                margin: 5px;
                border: 2px solid #94E2D5;
            }
            QPushButton:hover {
                background-color: #94E2D5;
                border: 2px solid #74C7EC;
            }
            QPushButton:pressed {
                background-color: #89DCEB;
            }
        """,

        "cancel_button": """
            QPushButton {
                background-color: #F38BA8;
                color: #1E1E2E;
                font-size: 14px;
                font-weight: 700;
                border-radius: 12px;
                padding: 12px 20px;
                min-height: 45px;
                min-width: 140px;
                margin: 5px;
                border: 2px solid #F5C2E7;
            }
            QPushButton:hover {
                background-color: #F5C2E7;
                border: 2px solid #CBA6F7;
            }
            QPushButton:pressed {
                background-color: #CBA6F7;
            }
        """,

        "scroll_area": """
            QScrollArea {
                background-color: transparent;
                border: 2px solid #45475A;
                border-radius: 12px;
                padding: 5px;
            }
            QScrollArea QWidget {
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #313244;
                width: 12px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background-color: #585B70;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #6C7086;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """
    }