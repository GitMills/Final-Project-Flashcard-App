
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
                text-align: center;
            }
        """,

        "name_input": """
            QLineEdit {
                background: #FDE4E0;
                font-size: 35px;
                font-weight: 600;
                padding: 15px;
                border-radius: 20px;
                margin: 10px 5px;
                color: #2C3E50;
                height: 60px;
                box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);

            }
            QLineEdit:focus {
                background-color: #FFF9F9;
            }
            QLineEdit::placeholder {
                color: #95A5A6;
            }
        """,

        "card_frame": """
            QFrame {
                background: #FDE4E0;
                border-radius: 15px;
                padding: 20px;
                margin: 10px 5px;
            }
        """,

        "card_number": """
            QLabel {
                font-size: 16px;
                font-weight: 700;
                color: #45B7D1;
                padding: 5px 0;
                background-color: transparent;
                border: none;
            }
        """,

        "question_input": """
            QLineEdit {
                background-color: #FFFFFF;
                border-radius: 12px;
                padding: 12px 15px;
                font-size: 14px;
                color: #2C3E50;
                font-weight: 500;
            }
            QLineEdit:focus {
                background-color: #FFF9F9;
            }
            QLineEdit::placeholder {
                color: #95A5A6;
            }
        ""","answer_input": """
    QTextEdit {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 12px 15px;
        font-size: 14px;
        color: #2C3E50;
        font-weight: 500;
        border: 1px solid #E0E0E0;
    }
    QTextEdit:focus {
        background-color: #FFF9F9;
        border: 1px solid #3498DB;
    }
""",

        "add_button": """
            QPushButton {
                background-color: #ABC6DE;
                color: white;
                font-size: 14px;
                font-weight: 700;
                border-radius: 12px;
                padding: 12px 20px;
                min-height: 45px;
                min-width: 140px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #8AB0D0;
            }
            QPushButton:pressed {
                background-color: #6999C3;
            }
        """,

        "save_button": """
            QPushButton {
                background-color: #ABDEC3;
                color: white;
                font-size: 14px;
                font-weight: 700;
                border-radius: 12px;
                padding: 12px 20px;
                min-height: 45px;
                min-width: 140px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #8AD0AB;
            }
            QPushButton:pressed {
                background-color: #69C393;
            }
        """,

        "cancel_button": """
            QPushButton {
                background-color: #F7A291;
                color: white;
                font-size: 14px;
                font-weight: 700;
                border-radius: 12px;
                padding: 12px 20px;
                min-height: 45px;
                min-width: 140px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #F47E66;
            }
            QPushButton:pressed {
                background-color: #F15A3B;
            }
        """,

        "scroll_area": """
            QScrollArea {
                background-color: transparent;
                border-radius: 12px;
                padding: 5px;
            }
            QScrollArea QWidget {
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: transparent;
                width: 2px;
                border-radius: 7px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background-color: transparent;
                border-radius: 7px;
                min-height: 20px;
            }
        """,
        
        "warning_message_box": """
            QMessageBox {
                background-color: #FBF2E9;
                border-radius: 20px;
            }
            QMessageBox QLabel {
                color: #2C3E50;
                font-size: 14px;
                background-color: transparent;
                font-weight: 500;
            }
            QMessageBox QPushButton {
                background-color:#EDC29C;
                color: white;
                font-size: 14px;
                font-weight: 600;
                border-radius: 12px;
                padding: 8px 16px;
                min-height: 35px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #DF924E;
            }
            QMessageBox QPushButton:pressed {
                background-color: #D87A29;
            }
        """,
        
        "success_message_box": """
            QMessageBox {
                background-color: #F7FDFC;
                border-radius: 15px;
            }
            QMessageBox QLabel {
                color: #2C3E50;
                font-size: 14px;
                background-color: transparent;
                font-weight: 500;
            }
            QMessageBox QPushButton {
                background-color: #96CEB4;
                color: #2C3E50;
                font-size: 14px;
                font-weight: 600;
                border-radius: 12px;
                padding: 8px 16px;
                min-height: 35px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #7BBFA1;
            }
        """,           
    }


def get_all_cards_styles():
    return {
        "title": """
            QLabel {
                font-size: 30px;
                font-weight: bold;
                color: #A2A8D3;
                padding: 10px;
            }
        """,
       "refresh_button": """
            QPushButton {
                background-color: #E3D3C3;
                border-radius: 15px;
                padding: 8px 15px;
                height: 45px;
                widght: 35px
            }
            QPushButton:hover {
                background-color: #6B5B45;
            }
            QPushButton:pressed {
                background-color: #5D4037;
            }
        """,
        "scroll_area": """
            QScrollArea {
                  QScrollArea {
                background-color: transparent;
                border-radius: 12px;
                padding: 5px;
            }
            QScrollArea QWidget {
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: transparent;
                width: 2px;
                border-radius: 7px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background-color: transparent;
                border-radius: 7px;
                min-height: 20px;
            }
        """,
        "no_sets_label": """
            QLabel {
                font-size: 50px;
                color: #7f8c8d;
                padding: 30px;
                text-align: center;
            }
        """,
        "error_label": """
            QLabel {
                font-size: 14px;
                color: #e74c3c;
                padding: 15px;
                text-align: center;
                background-color: #fadbd8;
                border-radius: 5px;
            }
        """,
        "card_frame": """
            QFrame {
                background: #FFE8E5;
                border-radius: 15px;
                padding: 20px;
                margin: 10px 5px;
            }
        """,
        "card_name": """
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 3px;
            }
        """,
        "info_label": """
            QLabel {
                font-size: 14px;
                color: #535050;
                padding: 5px;
            }
        """,
        "cancel_button": """
            QPushButton {
                background-color:#F9BEBE;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F59898;
            }
        """,
        "cards_info": """
            QLabel {
                font-size: 14px;
                color: #7f8c8d;
                padding: 10px;
            }
        """,
        "study_button": """
            QPushButton {
              background-color: #98CEF5;
                color: white;
                font-size: 14px;
                font-weight: 700;
                border-radius: 12px;
                padding: 2px 4px;
                min-height: 45px;
                min-width: 140px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #6AB9F0;
            }
        """,

        "delete_button": """
            QPushButton {
                background-color: #F7A291;
                color: white;
                font-size: 14px;
                font-weight: 700;
                border-radius: 12px;
                padding: 2px 4px;
                min-height: 45px;
                min-width: 140px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #F47E66;
            }
            QPushButton:pressed {
                background-color: #F15A3B;
            }
        """,

        "mc_button": """
            QPushButton {
                background-color: #D3C3E3;
                color: white;
                font-size: 14px;
                font-weight: 700;
                border-radius: 12px;
                padding: 2px 4px;
                min-height: 45px;
                min-width: 140px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #D9C4AF;
            }
            QPushButton:pressed {
                background-color: #CBAD90;
            }
        """,
        "warning_message_box": """
            QMessageBox {
                background-color: #FBF2E9;
                border-radius: 20px;
            }
            QMessageBox QLabel {
                color: #2C3E50;
                font-size: 14px;
                background-color: transparent;
                font-weight: 500;
            }
            QMessageBox QPushButton {
                background-color:#EDC29C;
                color: white;
                font-size: 14px;
                font-weight: 600;
                border-radius: 12px;
                padding: 8px 16px;
                min-height: 35px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #DF924E;
            }
            QMessageBox QPushButton:pressed {
                background-color: #D87A29;
            }
        """

    }


def get_study_page_styles():    
    
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
        
        "progress_bar": """
            QProgressBar {
                border: 2px solid #45475A;
                border-radius: 10px;
                text-align: center;
                background-color: #313244;
            }
            QProgressBar::chunk {
                background-color: #A6E3A1;
                border-radius: 8px;
            }
        """,
        
        "stats_label": """
            QLabel {
                color: #CDD6F4;
                font-size: 14px;
                font-weight: 600;
                background-color: transparent;
            }
        """,
        
        "card_counter": """
            QLabel {
                color: #89B4FA;
                font-size: 16px;
                font-weight: 600;
                background-color: transparent;
            }
        """,
        
        "shuffle_button": """
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
        
        "correct_button": """
            QPushButton {
                background-color: #A6E3A1;
                color: #1E1E2E;
                font-size: 16px;
                font-weight: 700;
                border-radius: 12px;
                padding: 15px 25px;
                min-height: 50px;
                min-width: 120px;
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
        
        "wrong_button": """
            QPushButton {
                background-color: #F38BA8;
                color: #1E1E2E;
                font-size: 16px;
                font-weight: 700;
                border-radius: 12px;
                padding: 15px 25px;
                min-height: 50px;
                min-width: 120px;
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
        
        "reset_button": """
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
        
        "back_button": """
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
        
        "filter_checkbox": """
            QCheckBox {
                color: #CDD6F4;
                font-size: 14px;
                background-color: transparent;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #6C7086;
                border-radius: 4px;
                background-color: #313244;
            }
            QCheckBox::indicator:checked {
                background-color: #A6E3A1;
                border: 2px solid #94E2D5;
            }
        """,
        
        "card_front": """
            QFrame {
                background-color: red;
                border-radius: 20px;
                padding: 40px;
            }
        """,
        
        "card_back": """
            QFrame { 
                background-color: blue;
                border-radius: 20px;
                padding: 40px;
            }
        """,
        
        "card_text": """
            QLabel {
                color: #CDD6F4;
                font-size: 20px;
                background-color: transparent;
            }
        """
    }   


def get_multiple_choice_styles():
    return {
        "header_frame": """
            QFrame {
                background-color: #F3E8FC;
                border-radius: 15px;
                padding: 4px 10px;
                margin: 5px;
            }
        """,
        "question_frame": """
            QFrame {
                background-color: #FDE4E0;
                border-radius: 15px;
                margin: 10px 5px;
                font-size: 40px;
                min-height: 400px;
                min-width: 300px;
            }
        """,
        "option_button": """
            QRadioButton {
                background-color: #F5F1E8;
                border-radius: 12px;
                padding: 15px;
                font-size: 20px;
                font-weight: 500;
                color: #5D4037;
                min-height: 100px;
            }
            QRadioButton:hover {
                background-color: #E8DFCA;
            }
            QRadioButton:checked {
                background-color: #8B7355;
                color: #FFFFFF;
            }
            QRadioButton:disabled {
                background-color: #EDF2F7;
                color: #A0AEC0;
            }
        """,
        "set_name_label": """
            QLabel {
                font-size: 18px;
                font-weight: 700;
                color: #8B7355;
                padding: 5px ;
            }
        """,
        "stats_label": """
            QLabel {
                font-size: 16px;
                font-weight: 600;
                color: #5D4037;
                padding: 5px 0;
            }
        """,
        "question_label": """
            QLabel {
                font-size: 20px;
                font-weight: 600;
                color: #2D3748;
                padding: 10px;
                background-color: transparent;
            }
        """,
        "result_label": """
            QLabel {
                font-size: 16px;
                font-weight: 600;
                padding: 10px;
                border-radius: 8px;
                margin: 5px;
                color:  #8B7355;
            }
        """,
        "back_button": """
            QPushButton {
                background-color: #F29797;
                color: #5D4037;
                font-size: 14px;
                font-weight: 600;
                border-radius: 8px;
                padding: 8px 16px;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: #ED6E6E;
            }
            QPushButton:pressed {
                background-color: #E84545;
            }
        """,
        "next_button": """
            QPushButton {
                background-color: #8B7355;
                color: #FFFFFF;
                font-size: 14px;
                font-weight: 600;
                border-radius: 8px;
                padding: 12px 20px;
                min-height: 45px;
            }
            QPushButton:hover {
                background-color: #6B5B45;
            }
            QPushButton:pressed {
                background-color: #5D4037;
            }
        """
    }