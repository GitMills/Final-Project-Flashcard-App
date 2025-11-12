from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCheckBox, QSlider,
    QGroupBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput  
import os
import sys


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_music()  

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setStyleSheet("color: black;") 

        title = QLabel("<h1>Application Settings</h1>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Appearance settings group
        appearance_group = QGroupBox("Appearance")
        appearance_layout = QVBoxLayout()

        # Theme selector
        from PyQt6.QtWidgets import QComboBox, QHBoxLayout
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light Mode", "Dark Mode"])
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()

        appearance_layout.addLayout(theme_layout)
        appearance_group.setLayout(appearance_layout)

        # Music settings group
        music_group = QGroupBox("Background Music")
        music_layout = QVBoxLayout()

        # Clickable checkbox with label
        music_checkbox_layout = QHBoxLayout()
        self.sound_check = QCheckBox("Play background music")
        music_checkbox_layout.addWidget(self.sound_check)
        music_checkbox_layout.addStretch()

        # Volume tracker (slider + label)
        volume_layout = QHBoxLayout()
        volume_text = QLabel("Volume:")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setEnabled(False)
        self.volume_label = QLabel("50%")
        volume_layout.addWidget(volume_text)
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addWidget(self.volume_label)

        # Play Sound checkbox to toggle music
        self.sound_check.stateChanged.connect(self.toggle_music)
        self.volume_slider.valueChanged.connect(self.change_volume)

        music_layout.addLayout(music_checkbox_layout)
        music_layout.addLayout(volume_layout)
        music_group.setLayout(music_layout)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(appearance_group)
        layout.addWidget(music_group)
        layout.addStretch()
        self.setLayout(layout)

    def setup_music(self):
        try:
            from utils.path_helper import get_asset_path
            
            music_path = get_asset_path("bgmusic.mp3")
            
            if os.path.exists(music_path):
                self.music_output = QAudioOutput()
                self.music_player = QMediaPlayer()
                self.music_player.setAudioOutput(self.music_output)
                self.music_player.setSource(QUrl.fromLocalFile(music_path))
                self.music_output.setVolume(0.5)
                
                self.music_player.errorOccurred.connect(self.handle_music_error)
            else:
                self.music_player = None
                
        except ImportError:
            self.music_player = None
        except Exception:
            self.music_player = None

    def handle_music_error(self, error):
        pass

    def change_volume(self, value):
        self.volume_label.setText(f"{value}%")
        if hasattr(self, 'music_output') and self.music_output:
            self.music_output.setVolume(value / 100.0)
        
        # Auto-save volume preference
        self.auto_save_settings()

    def change_theme(self, theme_text):
        """Apply theme change immediately"""
        try:
            # Get QApplication instance to find AppStack
            from PyQt6.QtWidgets import QApplication
            app = QApplication.instance()
            
            # Find AppStack widget
            for widget in app.topLevelWidgets():
                if widget.__class__.__name__ == 'AppStack':
                    if hasattr(widget, 'welcome_page'):
                        welcome_page = widget.welcome_page
                        if hasattr(welcome_page, 'data') and hasattr(welcome_page, 'apply_theme'):
                            if theme_text == "Dark Mode":
                                welcome_page.data.theme = "dark"
                            else:
                                welcome_page.data.theme = "light"
                            welcome_page.apply_theme()
                            print(f"✓ Theme changed to: {welcome_page.data.theme}")
                            break
                
            # Auto-save theme preference
            self.auto_save_settings()
        except Exception as e:
            print(f"Error changing theme: {e}")
            import traceback
            traceback.print_exc()

    def toggle_music(self, state):
        enabled = (state == Qt.CheckState.Checked.value)
        self.volume_slider.setEnabled(enabled)

        if hasattr(self, 'music_player') and self.music_player:
            if enabled:
                self.music_output.setVolume(self.volume_slider.value() / 100.0)
                self.music_player.play()
            else:
                self.music_player.stop()
        
        # Auto-save music preference
        self.auto_save_settings()

    def auto_save_settings(self):
        """Automatically save settings when changed"""
        theme = self.theme_combo.currentText()
        volume = self.volume_slider.value()

        settings = {
            "theme": theme,
            "volume": volume,
            "music_enabled": self.sound_check.isChecked()
        }
        
        try:
            import json
            with open("app_settings.json", "w") as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def show_success_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.NoIcon)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)

        try:
            from utils.path_helper import get_icon_path
            icon_path = get_icon_path("success.png")
        except ImportError:
            icon_path = "success.png"

        if os.path.exists(icon_path):
            msg.setIconPixmap(QPixmap(icon_path).scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio))
            msg.setWindowIcon(QIcon(icon_path))

        from ui.visual.styles.styles import get_settings_message_box_style
        msg.setStyleSheet(get_settings_message_box_style())

        msg.exec()