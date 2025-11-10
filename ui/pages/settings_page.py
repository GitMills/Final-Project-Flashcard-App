# FINAL PROJECT FLASHCARD APP / ui / pages / setttings_page.py


from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCheckBox, QSlider, QComboBox,
    QGroupBox, QPushButton, QColorDialog, QMessageBox, QSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from streamlit import success


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setStyleSheet("color: black;")  

        title = QLabel("<h1>Application Settings</h1>")

        #Notification settings group
        notify_group = QGroupBox("Notifications")
        notify_layout = QVBoxLayout()

        self.notify_check = QCheckBox("Enable notifications")
        self.sound_check = QCheckBox("Play sound")

        #Volume tracker (slider + label)
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setEnabled(False)

        self.volume_label = QLabel("Volume: 50%")

        #Enable/disable volume when "Play sound" is checked
        self.sound_check.stateChanged.connect(
            lambda state: self.volume_slider.setEnabled(state == Qt.CheckState.Checked)
        )

        #Update label when slider moves
        self.volume_slider.valueChanged.connect(
            lambda value: self.volume_label.setText(f"Volume: {value}%")
        )

        notify_layout.addWidget(self.notify_check)
        notify_layout.addWidget(self.sound_check)
        notify_layout.addWidget(self.volume_slider)
        notify_layout.addWidget(self.volume_label)
        notify_group.setLayout(notify_layout)

        #Theme settings group
        theme_group = QGroupBox("Appearance")
        theme_layout = QVBoxLayout()

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "Auto"])

        theme_layout.addWidget(QLabel("Theme:"))
        theme_layout.addWidget(self.theme_combo)
        theme_group.setLayout(theme_layout)

        #Font settings group
        font_group = QGroupBox("Font Settings")
        font_layout = QVBoxLayout()

        self.font_size = QSpinBox()
        self.font_size.setRange(8, 40)
        self.font_size.setValue(14)

        font_layout.addWidget(QLabel("Font Size:"))
        font_layout.addWidget(self.font_size)
        font_group.setLayout(font_layout)

        #Color settings group
        color_group = QGroupBox("Background Color")
        color_layout = QVBoxLayout()

        self.color_button = QPushButton("Choose Color")
        self.color_button.clicked.connect(self.choose_color)

        color_layout.addWidget(self.color_button)
        color_group.setLayout(color_layout)

        #Save settings button
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)

        #Add all groups to layout
        layout.addWidget(title)
        layout.addWidget(notify_group)
        layout.addWidget(theme_group)
        layout.addWidget(font_group)
        layout.addWidget(color_group)
        layout.addWidget(self.save_button)
        layout.addStretch()

        self.setLayout(layout)

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

        self.show_success_message(
            "Success!",
            f"Flashcard set 'Settings' saved successfully!\n\nTotal cards saved: 4\n"
            f"Theme: {theme}\nFont Size: {font_size}\nBackground: {color}\nVolume: {volume}%"
        )

    #Custom styled message box
    def show_success_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.NoIcon)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)

        #Custom icon
        icon_path = "success.png" 
        msg.setIconPixmap(QPixmap(icon_path).scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio))
        msg.setWindowIcon(QIcon(icon_path))

        #Style: white background, black text, green rounded OK button
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
