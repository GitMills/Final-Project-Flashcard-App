#ui/pages/bootup_page.py (jose)
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from ui.visual.styles.styles import FONT_LARGE_BOLD, progress_bar_styles
from ui.visual.animations import FadeAnimation
from utils.path_helper import get_asset_path


class BootupPage(QWidget):
    def __init__(self, on_finish_callback=None):
        super().__init__()
        self.on_finish_callback = on_finish_callback
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint) #Added
        self.fade = FadeAnimation(self)
        self.init_ui()
        self.simulate_loading()

    def init_ui(self):
        self.setStyleSheet("background-color: #FFF5E5;")
    
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
    
        logo = QLabel()
        pixmap = QPixmap(get_asset_path("AppIcon.png"))
        pixmap = pixmap.scaled(600, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        title = QLabel("")
        title.setFont(FONT_LARGE_BOLD)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.progress.setFixedWidth(1000)
        self.progress.setStyleSheet(progress_bar_styles)
            

        layout.addStretch()
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addSpacing(25)
        layout.addWidget(self.progress)
        layout.addStretch()

    def simulate_loading(self):
        """Simulate a bootup loading sequence."""
        self.value = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(35)  # Controls loading speed

    def update_progress(self):
        self.value += 2
        self.progress.setValue(self.value)
        if self.value == 2:
            self.fade.fade_in()
        if self.value >= 100:
            self.timer.stop()
            self.fade.fade_out(self.on_finish_callback)
            


