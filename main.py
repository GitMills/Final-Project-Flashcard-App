import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.main_window import MainWindow
from utils.path_helper import get_asset_path

def main():
    app = QApplication(sys.argv)
    
    # Set app icon using path helper
    app.setWindowIcon(QIcon(get_asset_path("AppIcon.png")))

    # Create and show main window
    window = MainWindow()
    window.showMaximized()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    