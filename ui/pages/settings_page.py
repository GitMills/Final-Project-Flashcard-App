from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCheckBox, QSlider, QComboBox,
    QGroupBox, QPushButton, QColorDialog, QMessageBox, QSpinBox
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

        # Notification settings group
        notify_group = QGroupBox("Notifications")
        notify_layout = QVBoxLayout()

        self.notify_check = QCheckBox("Enable notifications")
        self.sound_check = QCheckBox("Play sound")

        # Volume tracker (slider + label)
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setEnabled(False)

        self.volume_label = QLabel("Volume: 50%")

        # Play Sound checkbox to toggle music
        self.sound_check.stateChanged.connect(self.toggle_music)
        self.volume_slider.valueChanged.connect(self.change_volume)

        notify_layout.addWidget(self.notify_check)
        notify_layout.addWidget(self.sound_check)
        notify_layout.addWidget(self.volume_slider)
        notify_layout.addWidget(self.volume_label)
        notify_group.setLayout(notify_layout)

        # Theme settings group
        theme_group = QGroupBox("Appearance")
        theme_layout = QVBoxLayout()

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "Auto"])

        theme_layout.addWidget(QLabel("Theme:"))
        theme_layout.addWidget(self.theme_combo)
        theme_group.setLayout(theme_layout)

        # Font settings group
        font_group = QGroupBox("Font Settings")
        font_layout = QVBoxLayout()

        self.font_size = QSpinBox()
        self.font_size.setRange(8, 40)
        self.font_size.setValue(14)

        font_layout.addWidget(QLabel("Font Size:"))
        font_layout.addWidget(self.font_size)
        font_group.setLayout(font_layout)

        # Color settings group
        color_group = QGroupBox("Background Color")
        color_layout = QVBoxLayout()

        self.color_button = QPushButton("Choose Color")
        self.color_button.clicked.connect(self.choose_color)

        color_layout.addWidget(self.color_button)
        color_group.setLayout(color_layout)

        # Save settings button
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)

        layout.addWidget(title)
        layout.addWidget(notify_group)
        layout.addWidget(theme_group)
        layout.addWidget(font_group)
        layout.addWidget(color_group)
        layout.addWidget(self.save_button)
        layout.addStretch()
        self.setLayout(layout)

    # Setup music player with path helper
    def setup_music(self):
        try:
            # Import your path helper
            from utils.path_helper import get_asset_path
            
            # Get the correct path using your helper
            music_path = get_asset_path("bgmusic.mp3")
            
            print(f"Looking for music at: {music_path}")  # Debug
            
            if os.path.exists(music_path):
                print("Music file found!")
                self.music_output = QAudioOutput()
                self.music_player = QMediaPlayer()
                self.music_player.setAudioOutput(self.music_output)
                self.music_player.setSource(QUrl.fromLocalFile(music_path))
                self.music_output.setVolume(0.5)
                
                # Connect error handling
                self.music_player.errorOccurred.connect(self.handle_music_error)
                print("Music player setup successful")
            else:
                print("Music file NOT found!")
                print(f"Expected path: {music_path}")
                # Check what's actually in the assets directory
                assets_dir = os.path.dirname(music_path)
                if os.path.exists(assets_dir):
                else:
                self.music_player = None
                
        except ImportError as e:
            self.music_player = None
        except Exception as e:
            self.music_player = None

    def handle_music_error(self, error):
        if hasattr(self, 'music_player') and self.music_player:

    # Change volume when slider moves
    def change_volume(self, value):
        self.volume_label.setText(f"Volume: {value}%")
        if hasattr(self, 'music_output') and self.music_output:
            self.music_output.setVolume(value / 100.0)

    # Toggle volume slider + background music
    def toggle_music(self, state):
        enabled = (state == Qt.CheckState.Checked.value)
        self.volume_slider.setEnabled(enabled)

        if hasattr(self, 'music_player') and self.music_player:
            if enabled:
                # Set volume first, then play
                self.music_output.setVolume(self.volume_slider.value() / 100.0)
                self.music_player.play()
            else:
                self.music_player.stop()
        else:

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color.name()
            self.show_success_message(
                "Color Selected",
                f"Chosen color: {self.selected_color}"
            )

    def save_settings(self):
        theme = self.theme_combo.currentText()
        font_size = self.font_size.value()
        color = getattr(self, "selected_color", "#FFFFFF")
        volume = self.volume_slider.value()

        if hasattr(self, 'music_output') and self.music_output:
            self.music_output.setVolume(volume / 100.0)

        self.show_success_message(
            "Success!",
            f"Flashcard set 'Settings' saved successfully!\n\nTotal cards saved: 4\n"
            f"Theme: {theme}\nFont Size: {font_size}\nBackground: {color}\nVolume: {volume}%"
        )

    # Custom message box with success icon
    def show_success_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.NoIcon)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)

        # Use path helper for icon too
        try:
            from utils.path_helper import get_icon_path
            icon_path = get_icon_path("success.png")
        except ImportError:
            icon_path = "success.png"  # Fallback

        if os.path.exists(icon_path):
            msg.setIconPixmap(QPixmap(icon_path).scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio))
            msg.setWindowIcon(QIcon(icon_path))

        msg.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
                color: #000000;
                font-size: 13px;
            }
            QLabel {
                color: #000000;
            }
            QPushButton {
                background-color: #cde5d4;
                color: black;
                border-radius: 8px;
                padding: 6px 25px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b4dbb8;
            }
        """)

        msg.exec()


