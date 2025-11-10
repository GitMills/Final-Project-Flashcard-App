# FINAL PROJECT FLASHCARD APP / main.py

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt 

# Enable high DPI scaling with proper fallbacks
if hasattr(Qt, 'HighDpiScaleFactorRoundingPolicy'):
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

# Set environment variables for scaling
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCALE_FACTOR"] = "1"

from ui.pages.bootup_page import BootupPage
from ui.pages.welcome_page import WelcomePage
from ui.main_window import MainWindow
from utils.path_helper import get_asset_path

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(get_asset_path("AppIcon.png")))

    # Create main window but don’t show yet
    main_window = MainWindow()

    # Create welcome page (it will show main window later)
    class AppController:
        def __init__(self):
            self.main_window = main_window
            
        def show_main_window(self):
            self.welcome_page.close()
            self.main_window.showMaximized()

    controller = AppController()
    controller.welcome_page = WelcomePage(app=controller)

    # Bootup page → Welcome page
    def on_bootup_finished():
        bootup_page.close()
        controller.welcome_page.showMaximized()

    # Bootup
    bootup_page = BootupPage(on_finish_callback=on_bootup_finished)
    bootup_page.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
