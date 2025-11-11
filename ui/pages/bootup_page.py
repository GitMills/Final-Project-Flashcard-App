#ui/pages/bootup_page.py (jose)
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QFrame
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from ui.visual.styles.styles import FONT_LARGE_BOLD, progress_bar_styles
from utils.path_helper import get_asset_path


class BootupPage(QWidget):
    def __init__(self, on_finish_callback=None):
        super().__init__()
        self.on_finish_callback = on_finish_callback
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.init_ui()
        self.simulate_loading()

    def init_ui(self):
        # Set background color
        self.setStyleSheet("background-color: #FFF5E5;")
    
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 50, 50, 50)  # Add some padding around the edges
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_layout)
    
        # Create a container frame for the box effect
        from ui.visual.styles.styles import get_bootup_container_style
        container = QFrame()
        container.setFixedSize(500, 400)  # Fixed size for consistent centering
        container.setStyleSheet(get_bootup_container_style())
        
        # Container layout
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(25)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        # Logo
        logo = QLabel()
        pixmap = QPixmap(get_asset_path("AppIcon.png"))
        pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        # Title (optional - you had it empty)
        title = QLabel("Starting Up...")
        title.setFont(FONT_LARGE_BOLD)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #333333; margin-bottom: 10px;")
    
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.progress.setFixedWidth(350)  # Smaller width for the box
        self.progress.setFixedHeight(8)
        self.progress.setStyleSheet(progress_bar_styles)
        
        # Status label to show loading progress
        self.status_label = QLabel("Initializing...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #666666; font-size: 12px;")

        # Add widgets to container layout
        layout.addStretch(1)
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(self.progress)
        layout.addWidget(self.status_label)
        layout.addStretch(1)
        
        # Add container to main layout
        main_layout.addWidget(container)

    def simulate_loading(self):
        """Simulate a bootup loading sequence."""
        self.value = 0
        self.loading_stages = [
            (10, "Initializing..."),
            (30, "Loading components..."),
            (60, "Starting services..."),
            (85, "Finalizing..."),
            (100, "Ready!")
        ]
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(40)  # Controls loading speed

    def update_progress(self):
        self.value += 2
        self.progress.setValue(self.value)
        
        # Update status text based on progress
        for stage_value, stage_text in self.loading_stages:
            if self.value <= stage_value:
                self.status_label.setText(stage_text)
                break
        
        if self.value >= 100:
            self.timer.stop()
            if self.on_finish_callback:
                self.on_finish_callback()