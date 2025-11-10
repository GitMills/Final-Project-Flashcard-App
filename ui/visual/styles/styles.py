# FINAL PROJECT FLASHCARD APP / ui / visual / styles / styles.py
from PyQt6.QtGui import QFont

FONT_LARGE_BOLD = QFont("Poppins", 24, QFont.Weight.Bold) #jose

#stylesheet for loading bar, jose
progress_bar_styles = """
QProgressBar {
    border: 2px solid #E2E8F0;
    border-radius: 10px;
    background-color: #F7FAFC;
    height: 14px;
}
QProgressBar::chunk {
    background-color: #434190;
    border-radius: 10px;
}
"""

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
                min-height: 45px;
                min-width: 45px;
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
                min-height: 40px;
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
                min-height: 40px;
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
                font-size: 28px;
                font-weight: 900;
                border-radius: 30px;
                padding: 12px 30px;
                min-height: 50px;
                min-width: 250px;
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
                font-size: 24px;
                font-weight: 900;
                color: #A2A8D3;
                padding: 10px 0;
                background-color: transparent;
                text-align: center;
            }
        """,

        "name_input": """
            QLineEdit {
                background: #F27D72;
                font-size: 28px;
                font-weight: 600;
                padding: 12px;
                border-radius: 20px;
                margin: 8px 5px;
                color: white;
                min-height: 50px;
                selection-background-color: #E7E7E7;
            }
            QLineEdit:focus {
                background-color: #FFF9F9;
                color: #2C3E50;
            }
        """,

        "card_frame_1": """
            QFrame {
                background: #B3D9FF;
                border-radius: 15px;
                padding: 15px;
                margin: 8px 5px;
            }
        """,

        "card_frame_2": """
            QFrame {
                background: #B9FBC0;
                border-radius: 15px;
                padding: 15px;
                margin: 8px 5px;
            }
        """,

        "card_frame_3": """
            QFrame {
                background: #FFE6A7;
                border-radius: 15px;
                padding: 15px;
                margin: 8px 5px;
            }
        """,

        "card_frame_4": """
            QFrame {
                background: #FFB3B3;
                border-radius: 15px;
                padding: 15px;
                margin: 8px 5px;
            }
        """,

        "card_number": """
            QLabel {
                font-size: 14px;
                font-weight: 700;
                color: #45B7D1;
                padding: 1px 6px;
                background-color: transparent;
                border: none;
            }
        """,

        "question_input": """
            QLineEdit {
                background-color: #FFFFFF;
                border-radius: none;
                padding: 10px 12px;
                font-size: 14px;
                color: #2C3E50;
                font-weight: 500;
                selection-background-color: #E7E7E7;
            }
        """,

        "answer_input": """
            QTextEdit {
                background-color: #FFFFFF;
                border-radius: 12px;
                padding: 10px 12px;
                font-size: 14px;
                color: #2C3E50;
                font-weight: 500;
                selection-background-color: #E7E7E7;
                min-height: 60px;
            }
            QTextEdit:focus {
                background-color: #FFF9F9;
            }
        """,

        "add_button": """
            QPushButton {
                background-color: #ABC6DE;
                color: white;
                font-size: 14px;
                font-weight: 700;
                border-radius: 12px;
                padding: 10px 16px;
                min-height: 40px;
                min-width: 120px;
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
                padding: 10px 16px;
                min-height: 40px;
                min-width: 120px;
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
                padding: 10px 16px;
                min-height: 40px;
                min-width: 120px;
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
                background-color: #EDC29C;
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
        
        "remove_btn": """
            QPushButton {
                background-color: #FF6B6B;
                color: white;
                border-radius: 8px;
                font-size: 12px;
                margin: 0px;
                min-height: 30px;
                min-width: 30px;
            }
            QPushButton:hover {
                background-color: #FF5252;
            }
            QPushButton:pressed {
                background-color: #FF0000;
            }
        """           
    }


def get_all_cards_styles():
    return {
        "title": """
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #A2A8D3;
                padding: 8px;
            }
        """,
        
        "refresh_button": """
            QPushButton {
                background-color: #E3D3C3;
                border-radius: 15px;
                padding: 6px 12px;
                min-height: 40px;
                min-width: 40px;
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
                font-size: 32px;
                color: #7f8c8d;
                padding: 20px;
                text-align: center;
            }
        """,
        
        "error_label": """
            QLabel {
                font-size: 14px;
                color: #e74c3c;
                padding: 12px;
                text-align: center;
                background-color: #fadbd8;
                border-radius: 5px;
            }
        """,
        
        "card_frame_1": """
            QFrame {
                background: #B3D9FF;
                border-radius: 15px;
                padding: 15px;
                margin: 8px 5px;
                min-width: 280px;
            }
        """,
        
        "card_frame_2": """
            QFrame {
                background: #B9FBC0;
                border-radius: 15px;
                padding: 15px;
                margin: 8px 5px;
                min-width: 280px;
            }
        """,
        
        "card_frame_3": """
            QFrame {
                background: #FFE6A7;
                border-radius: 15px;
                padding: 15px;
                margin: 8px 5px;
                min-width: 280px;
            }
        """,
        
        "card_frame_4": """
            QFrame {
                background: #FFB3B3;
                border-radius: 15px;
                padding: 15px;
                margin: 8px 5px;
                min-width: 280px;
            }
        """,
        
        "card_name": """
            QLabel {
                font-size: 16px;
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
        
        "cards_info": """
            QLabel {
                font-size: 14px;
                color: #7f8c8d;
                padding: 8px;
            }
        """,
        
        "study_button": """
            QPushButton {
                background-color: #ABABDE;
                color: white;
                font-size: 14px;
                font-weight: 700;
                border-radius: 12px;
                padding: 8px 12px;
                min-height: 40px;
                min-width: 120px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #6AB9F0;
            }
        """,

        "delete_button": """
            QPushButton {
                background-color: #BA9C9C;
                color: white;
                font-size: 14px;
                font-weight: 700;
                border-radius: 12px;
                padding: 8px 12px;
                min-height: 40px;
                min-width: 120px;
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
                padding: 8px 12px;
                min-height: 40px;
                min-width: 120px;
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
                background-color: #EDC29C;
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
        ""","success_message_box": """
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
        ""","search_input": """
            QLineEdit {
                background-color: #E3D3C3;
                border: 2px solid #A2A8D3;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 18px;
                min-width: 300px;
                color:  black;
            }
            QLineEdit:focus {
                border-color: #585B70;
            }
        """,
        "no_results_label": """
            QLabel {
                color: #F38BA8;
                font-size: 18px;
                font-weight: 600;
                padding: 20px;
            }
        """
    }


def get_study_page_styles():    
    return {
        "title": """
            QLabel {
                font-size: 24px;
                font-weight: 900;
                color: #A2A8D3;
                padding: 12px 0;
                background-color: transparent;
                border: none;
            }
        """,
        
        "progress_bar": """
            QProgressBar {
                border-radius: 10px;
                text-align: center;
                background-color: #313244;
                height: 20px;
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
                color: #9C9191;
                font-size: 14px;
                font-weight: 600;
                background-color: transparent;
                margin: 0px;
                padding: 1px 6px;
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
                min-width: 100px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #6C7086;
            }
            QPushButton:pressed {
                background-color: #45475A;
            }
        """,
        
        "correct_button": """
            QPushButton {
                background-color: #A6E3A1;
                color: #1E1E2E;
                font-size: 14px;
                font-weight: 700;
                border-radius: 12px;
                padding: 12px 20px;
                min-height: 45px;
                min-width: 100px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #94E2D5;
            }
            QPushButton:pressed {
                background-color: #89DCEB;
            }
        """,
        
        "wrong_button": """
            QPushButton {
                background-color: #F38BA8;
                color: #1E1E2E;
                font-size: 14px;
                font-weight: 700;
                border-radius: 12px;
                padding: 12px 20px;
                min-height: 45px;
                min-width: 100px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #F5C2E7;
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
                min-width: 100px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #6C7086;
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
                min-width: 100px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #F5C2E7;
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
                border-radius: 4px;
                background-color: #313244;
            }
            QCheckBox::indicator:checked {
                background-color: #A6E3A1;
            }
        """,
        
        "card_front": """
            QFrame {
                background-color: #FDE4E0;
                border-radius: 20px;
                padding: 30px;
            }
        """,
        
        "card_back": """
            QFrame { 
                background-color: #FDE4E0;
                border-radius: 20px;
                padding: 30px;
            }
        """,
        
        "card_text": """
            QLabel {
                color: black;
                font-size: 24px;
                background-color: transparent;
            }
        """,

        "hint_button": """
            QPushButton {
                background-color: #C3DCF4;
                color: black;
                font-size: 14px;
                font-weight: 700;
                border-radius: 12px;
                padding: 12px 20px;
                min-height: 45px;
                min-width: 50px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #9CC5EC;
            }
            QPushButton:pressed {
                background-color: #76AFE5;
            }
        """,
        
        "hint_text": """
            QLabel {
                color: black;
                font-size: 18px;
                font-weight: 600;
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
                border: 6px solid #FAFDE7;
            }
        """
    }
    return {
        "title": """
            QLabel {
                font-size: 24px;
                font-weight: 900;
                color: #A2A8D3;
                padding: 12px 0;
                background-color: transparent;
                border: none;
            }
        """,
        
        "progress_bar": """
            QProgressBar {
                border-radius: 10px;
                text-align: center;
                background-color: #313244;
                height: 20px;
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
                color: #9C9191;
                font-size: 14px;
                font-weight: 600;
                background-color: transparent;
                margin: 0px;
                padding: 1px 6px;
            }
        """,
        
        "shuffle_button": """
            QPushButton {
                background-color: #585B70;
                color: #CDD6F4;
                font-size: 14px;
                font-weight: 600;
                border-radius: 12px;
                padding: 10px 16px;
                min-height: 40px;
                min-width: 120px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #6C7086;
            }
            QPushButton:pressed {
                background-color: #45475A;
            }
        """,
        
        "correct_button": """
            QPushButton {
                background-color: #A6E3A1;
                color: #1E1E2E;
                font-size: 14px;
                font-weight: 700;
                border-radius: 12px;
                padding: 12px 20px;
                min-height: 45px;
                min-width: 100px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #94E2D5;
            }
            QPushButton:pressed {
                background-color: #89DCEB;
            }
        """,
        
        "wrong_button": """
            QPushButton {
                background-color: #F38BA8;
                color: #1E1E2E;
                font-size: 14px;
                font-weight: 700;
                border-radius: 12px;
                padding: 12px 20px;
                min-height: 45px;
                min-width: 100px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #F5C2E7;
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
                padding: 10px 16px;
                min-height: 40px;
                min-width: 120px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #6C7086;
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
                padding: 10px 16px;
                min-height: 40px;
                min-width: 120px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #F5C2E7;
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
                border-radius: 4px;
                background-color: #313244;
            }
            QCheckBox::indicator:checked {
                background-color: #A6E3A1;
            }
        """,
        
        "card_front": """
            QFrame {
                background-color: #FDE4E0;
                border-radius: 20px;
                padding: 30px;
            }
        """,
        
        "card_back": """
            QFrame { 
                background-color: #FDE4E0;
                border-radius: 20px;
                padding: 30px;
            }
        """,
        
        "card_text": """
            QLabel {
                color: black;
                font-size: 24px;
                background-color: transparent;
            }
        """,

        "hint_button": """
            QPushButton {
                background-color: #C3DCF4;
                color: black;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 700;
                min-height: 40px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #9CC5EC;
            }
            QPushButton:pressed {
                background-color: #76AFE5;
            }
        """,
        "hint_text": """
            QLabel {
                color: black;
                font-size: 30px;
                font-weight: 700;
                border-radius: 12px;
                padding: 12px 20px;
                min-height: 20px;
                min-width: 100px;
                margin: 5px;
                background-color: #F8CF8D;
            }
        """
    }   
              
def get_multiple_choice_styles():
    return {
        "header_frame": """
            QFrame {
                background-color: #F3E8FC;
                border-radius: 15px;
                padding: 8px 12px;
                margin: 5px;
            }
        """,
        
        "question_frame": """
            QFrame {
                background-color: #FDE4E0;
                border-radius: 15px;
                margin: 8px 5px;
                padding: 15px;
                min-height: 80px;
            }
        """,
        
        "option_button": """
            QRadioButton {
                background-color: #F5F1E8;
                border-radius: 12px;
                padding: 10px 12px;
                font-size: 14px;
                font-weight: 500;
                color: #5D4037;
                min-height: 50px;
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
                font-size: 16px;
                font-weight: 700;
                color: #8B7355;
                padding: 5px;
            }
        """,
        
        "stats_label": """
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #5D4037;
                padding: 5px 0;
            }
        """,
        
        "question_label": """
            QLabel {
                font-size: 16px;
                font-weight: 600;
                color: #2D3748;
                padding: 8px;
                background-color: transparent;
            }
        """,
        
        "result_label": """
            QLabel {
                font-size: 14px;
                font-weight: 600;
                padding: 8px;
                border-radius: 8px;
                margin: 5px;
                color: #8B7355;
                min-height: 30px;
            }
        """,
        
        "back_button": """
            QPushButton {
                background-color: #F29797;
                color: #5D4037;
                font-size: 12px;
                font-weight: 600;
                border-radius: 8px;
                padding: 6px 12px;
                min-height: 30px;
                min-width: 70px;
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
                padding: 10px 16px;
                min-height: 40px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #6B5B45;
            }
            QPushButton:pressed {
                background-color: #5D4037;
            }
        """
    }


def get_existing_flashcard_styles():
    return {
        # === Main Page ===
        "page": "background-color: #FFF7EB;",

        # Back Button (main and topic views)
        "back_button": """
            QPushButton {
                background-color: #F27D72;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #d25a50; }
        """,

        # Title label ("TOPICS")
        "title": """
            QLabel {
                font-size: 24px;
                font-weight: bold;
                background-color: #F27D72;
                color: white;
                border-radius: 15px;
                padding: 15px;
            }
        """,

        # Topic buttons (English, Math, etc.)
        "topic_button": """
            QPushButton {{
                background-color: {color};
                border: none;
                border-radius: 25px;
                font-size: 20px;
                font-weight: bold;
                color: #333;
                text-align: left;
                padding-left: 30px;
            }}
            QPushButton:hover {{
                background-color: #dfefff;
            }}
        """,

        # Flashcard appearance
        "flashcard": """
            QFrame {
                background-color: #FDE3E3;
                border-radius: 20px;
            }
            QLabel {
                font-size: 16px;
                color: #333;
            }
        """,

        # Topic header title in study view
        "topic_title": "font-weight: bold; color: #9C9AC2; font-size: 20px;",
        "timer_label": "color: #5f5f5f; font-size: 14px;",

        # Control buttons (shuffle, correct, wrong, reset)
        "control_button": """
            QPushButton {{
                background-color: {color};
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                color: black;
            }}
            QPushButton:hover {{
                opacity: 0.8;
            }}
        """,

        # Progress bar
        "progress_bar": """
            QProgressBar {
                border: none;
                height: 18px;
                border-radius: 8px;
                background-color: #DDD;
            }
            QProgressBar::chunk {
                background-color: #55556A;
                border-radius: 8px;
            }
        """,
    }
    # Add this to your styles.py file


def get_pomodoro_styles():
    return {
        # Break Overlay Styles
        "break_overlay": """
            BreakOverlay {
                background-color: rgba(246, 242, 238, 0.8);
                border: none;
                
            }
        """,
        
        "break_label": """
            QLabel {
                background-color: rgba(246, 242, 238);
                padding: 20px;
                border-radius: 15px;
                
            }
        """,
        
        "break_message": """
            QLabel {
                background-color: rgba(246, 242, 238);
                color: #2C3E50;
                font-size: 18px;
                font-weight: normal;
                border-radius: 10px;
            }
        """,
        
        "break_progress": """
            QLabel {
                color: #8E44AD;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                background-color: rgba(246, 242, 238);

            }
        """,
        
        "break_timer": """
            QLabel {
                color: #C0392B;
                font-size: 48px;
                font-weight: bold;
                padding: 25px;
                background-color: rgba(246, 242, 238);
                border-radius: 15px;
            }
        """,
        
        "break_instruction": """
            QLabel {
                color: #2C3E50;
                font-size: 14px;
                border-radius: 8px;
                background-color: rgba(246, 242, 238);
            }
        """,
        # Timer Button States
        "timer_button_forced_break": """
            QPushButton {
                background-color: #95A5A6;
                color: #2C3E50;
                border: 2px solid #7F8C8D;
                border-radius: 15px;
                font-weight: bold;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:disabled {
                background-color: #BDC3C7;
                color: #7F8C8D;
            }
        """,
        
        "timer_button_running": """
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border: 2px solid #C0392B;
                border-radius: 15px;
                font-weight: bold;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """,
        
        "timer_button_stopped": """
            QPushButton {
                background-color: #27AE60;
                color: white;
                border: 2px solid #229954;
                border-radius: 15px;
                font-weight: bold;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """,
        
        # Settings Dialog Styles
        "settings_dialog": """
            QDialog {
                background-color: #ECF0F1;
                border-radius: 15px;
            }
            QWidget {
                background-color: #ECF0F1;
            }
        """,
        
        "settings_label": """
            QLabel {
                color: #2C3E50;
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                border-radius: 5px;
            }
        """,
        
        "spin_box": """
            QSpinBox {
                background-color: white;
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
                color: #2C3E50;
                font-weight: bold;
                min-width: 12px;
            }
            QSpinBox:focus {
                background-color: #FFF8E1;
            }
            QSpinBox::up-button {
                background-color: #C5DBF2;
                border-radius: 3px;
                width: 15px;
            }
            QSpinBox::down-button {
                background-color: #C5DBF2;
                border-radius: 3px;
                width: 15px;
            }
            QSpinBox::up-arrow {
                content: "▲";
                color: black;          
            }
            QSpinBox::down-arrow {
                 content: "▼";
                 color: black;
            }
        """,
        
        "settings_info": """
            QLabel {
                color: #E74C3C;
                font-size: 12px;
                font-weight: bold;
                background-color: #FFF8E1;
                padding: 12px;
                border-radius: 8px;
            }
        """,
        
        "save_button": """
            QPushButton {
                background-color: #27AE60;
                color: white;
                border-radius: 10px;
                font-weight: bold;
                padding: 10px 25px;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """,
        
        "cancel_button": """
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border-radius: 10px;
                font-weight: bold;
                padding: 10px 25px;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        ""","warning_message_box": """
            QMessageBox {
                background-color: #FEF5E7;
                border-radius: 15px;
            }
            QMessageBox QLabel {
                color: #2C3E50;
                font-size: 14px;
                font-weight: bold;
            }
            QMessageBox QPushButton {
                background-color: #C1E1A8;
                color: white;
                border-radius: 10px;
                font-weight: bold;
                padding: 8px 20px;
                font-size: 14px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #A9D585;
            }
        """
    }
