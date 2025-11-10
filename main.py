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
from ui.main_window import MainWindow
from utils.path_helper import get_asset_path

def main():
    app = QApplication(sys.argv)
    
    # Set app icon using path helper
    app.setWindowIcon(QIcon(get_asset_path("AppIcon.png")))

    # Create and show main window
    window = MainWindow()
    # Changed from showMaximized() to show() to let layout determine size
    window.showMaximized()
    
    def on_bootup_finished():
        bootup_page.close()
        window.showMaximized()

    # Create bootup page and pass callback
    bootup_page = BootupPage(on_finish_callback=on_bootup_finished)
    bootup_page.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
