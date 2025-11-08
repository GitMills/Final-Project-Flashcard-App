# FINAL PROJECT FLASHCARD APP / ui / components / pomodoro_timer.py

from PyQt6.QtCore import QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QSpinBox, QMessageBox, QWidget, QFrame)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtProperty

class BreakOverlay(QWidget):
    def __init__(self, parent, session_info):
        super().__init__(parent)
        self.session_info = session_info
        self.setup_ui()
        
    def setup_ui(self):
        # Cover the entire parent window
        self.setGeometry(0, 0, self.parent().width(), self.parent().height())
        
        # Semi-transparent dark background
        self.setStyleSheet("""
            BreakOverlay {
                background-color: rgba(0, 0, 0, 0.85);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)
        
        # Main break message
        break_label = QLabel("🌿 BREAK TIME 🌿")
        break_label.setStyleSheet("""
            QLabel {
                color: #A6E3A1;
                font-size: 32px;
                font-weight: bold;
                padding: 20px;
            }
        """)
        break_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Encouraging message
        messages = [
            "You're doing great! Your brain needs this rest.",
            "Well done! Taking breaks improves memory retention.",
            "Excellent work! This break will boost your focus.",
            "Amazing progress! Your mind is consolidating what you learned.",
            "Outstanding! This pause will enhance your learning."
        ]
        import random
        message = random.choice(messages)
        
        message_label = QLabel(message)
        message_label.setStyleSheet("""
            QLabel {
                color: #F9E2AF;
                font-size: 18px;
                font-weight: normal;
                padding: 15px;
            }
        """)
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setWordWrap(True)
        
        # RESPONSIVE SIZING - 60% of screen width for message      ganito dapat sizing wag fixed para applicable for all screensizes
        if self.parent():
            screen = self.parent().screen()
            screen_size = screen.availableGeometry()
            message_label.setMaximumWidth(int(screen_size.width() * 0.6))
        else:
            message_label.setMaximumWidth(500)
        
        # Session progress
        progress_label = QLabel(f"Session {self.session_info} completed!")
        progress_label.setStyleSheet("""
            QLabel {
                color: #CBA6F7;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Timer display in overlay
        self.timer_label = QLabel("05:00")
        self.timer_label.setStyleSheet("""
            QLabel {
                color: #F38BA8;
                font-size: 48px;
                font-weight: bold;
                font-family: 'Monospace';
                padding: 20px;
                background-color: rgba(30, 30, 46, 0.7);
                border-radius: 15px;
            }
        """)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # RESPONSIVE SIZING - 20% of screen width for timer
        if self.parent():
            screen = self.parent().screen()
            screen_size = screen.availableGeometry()
            self.timer_label.setMinimumWidth(int(screen_size.width() * 0.2))
        else:
            self.timer_label.setMinimumWidth(200)
        
        # Instruction
        instruction_label = QLabel("Relax... The timer will automatically continue when break is over")
        instruction_label.setStyleSheet("""
            QLabel {
                color: #6C7086;
                font-size: 14px;
                padding: 10px;
            }
        """)
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(break_label)
        layout.addWidget(message_label)
        layout.addWidget(progress_label)
        layout.addWidget(self.timer_label)
        layout.addWidget(instruction_label)
        
        self.setLayout(layout)
        
        # Fade in animation
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(800)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()
    
    def update_timer(self, minutes, seconds):
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")
    
    def resizeEvent(self, event):
        # Always cover the entire parent window
        self.setGeometry(0, 0, self.parent().width(), self.parent().height())
        super().resizeEvent(event)

class PomodoroTimer:
    def __init__(self, main_window):
        self.main_window = main_window
        self.time_remaining = 0
        self.timer_running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        
        # Session settings (user customizable)
        self.study_time = 25  # minutes
        self.break_time = 5   # minutes
        self.total_sessions = 4
        self.current_session = 0
        
        # State tracking
        self.is_break_time = False
        self.forced_break_mode = False
        self.sessions_completed = 0
        self.break_overlay = None
    
    def start_timer(self):
        if not self.timer_running and not self.forced_break_mode:
            if self.time_remaining == 0:
                # First start - initialize timer
                self.time_remaining = self.study_time * 60
                self.current_session = 1
            self.timer_running = True
            self.timer.start(1000)
            self.update_display()
            return True
        return False
    
    def pause_timer(self):
        # CANNOT pause during forced breaks
        if self.timer_running and not self.forced_break_mode:
            self.timer_running = False
            self.timer.stop()
            self.update_display()
            return True
        return False
    
    def reset_timer(self):
        # CANNOT reset during forced breaks
        if not self.forced_break_mode:
            self.timer_running = False
            self.timer.stop()
            self.time_remaining = 0
            self.is_break_time = False
            self.forced_break_mode = False
            self.current_session = 0
            self.sessions_completed = 0
            self.remove_break_overlay()
            self.update_display()
            return True
        return False
    
    def update_timer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.update_display()
            
            # Update overlay timer if it exists
            if self.break_overlay:
                minutes = self.time_remaining // 60
                seconds = self.time_remaining % 60
                self.break_overlay.update_timer(minutes, seconds)
        else:
            self.timer_finished()
    
    def update_display(self):
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        
        if self.forced_break_mode:
            status = "FORCED BREAK"
            color = "#F9E2AF"  # Yellow for forced break
        else:
            status = "Break" if self.is_break_time else "Study"
            color = "#A6E3A1"  # Green for normal mode
        
        # Add session info to display
        session_info = f" ({self.current_session}/{self.total_sessions})"
        display_text = f"{status}{session_info}: {minutes:02d}:{seconds:02d}"
        self.main_window.update_timer_display(display_text)
        
        # Update button states based on forced break mode
        self.update_button_states()
    
    def update_button_states(self):
        if hasattr(self.main_window, 'pomodoro_btn'):
            if self.forced_break_mode:
                # FORCED BREAK: Disable all controls
                self.main_window.pomodoro_btn.setEnabled(False)
                self.main_window.pomodoro_btn.setText("⏸ Forced Break")
                self.main_window.pomodoro_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #585B70;
                        color: #CDD6F4;
                        border: none;
                        border-radius: 15px;
                        font-weight: bold;
                        padding: 5px;
                    }
                """)
                
                # Also disable settings button during forced break
                if hasattr(self.main_window, 'timer_settings_btn'):
                    self.main_window.timer_settings_btn.setEnabled(False)
                    
            else:
                # NORMAL MODE: Enable controls
                self.main_window.pomodoro_btn.setEnabled(True)
                if hasattr(self.main_window, 'timer_settings_btn'):
                    self.main_window.timer_settings_btn.setEnabled(True)
                    
                if self.timer_running:
                    self.main_window.pomodoro_btn.setText("⏸ Pause")
                    self.main_window.pomodoro_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #F38BA8;
                            color: #1E1E2E;
                            border: none;
                            border-radius: 15px;
                            font-weight: bold;
                            padding: 5px;
                        }
                    """)
                else:
                    self.main_window.pomodoro_btn.setText("▶ Start")
                    self.main_window.pomodoro_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #A6E3A1;
                            color: #1E1E2E;
                            border: none;
                            border-radius: 15px;
                            font-weight: bold;
                            padding: 5px;
                        }
                    """)
    
    def show_break_overlay(self):
        # Show the full-screen break overlay
        session_info = f"{self.current_session}/{self.total_sessions}"
        self.break_overlay = BreakOverlay(self.main_window, session_info)
        self.break_overlay.show()
        self.break_overlay.raise_()
    
    def remove_break_overlay(self):
        # Remove the break overlay
        if self.break_overlay:
            self.break_overlay.deleteLater()
            self.break_overlay = None
    
    def timer_finished(self):
        self.timer_running = False
        self.timer.stop()
        
        if not self.is_break_time:
            # STUDY TIME FINISHED - START FORCED BREAK
            self.sessions_completed += 1
            self.is_break_time = True
            self.forced_break_mode = True  # THIS IS THE FORCE BREAK!
            self.time_remaining = self.break_time * 60
            
            # Show break overlay (covers entire screen)
            self.show_break_overlay()
            
            # AUTO-START the forced break (user cannot stop this!)
            self.timer_running = True
            self.timer.start(1000)
            
        else:
            # BREAK TIME FINISHED - Check if we have more sessions
            self.is_break_time = False
            self.forced_break_mode = False  # End forced break
            
            # Remove the break overlay
            self.remove_break_overlay()
            
            if self.current_session < self.total_sessions:
                # More sessions remaining
                self.current_session += 1
                self.time_remaining = self.study_time * 60
                
                QMessageBox.information(self.main_window, "Break Complete!", 
                                      f"Ready for session {self.current_session}/{self.total_sessions}?")
            else:
                # All sessions completed!
                self.time_remaining = 0
                self.current_session = 0
                self.sessions_completed = 0
                
                QMessageBox.information(self.main_window, "All Sessions Complete!", 
                                      f"Congratulations! You completed all {self.total_sessions} sessions! 🎉")
        
        self.update_display()
    
    def set_times(self, study_time, break_time, sessions):
        # Can only change settings when not in forced break
        if not self.forced_break_mode:
            self.study_time = study_time
            self.break_time = break_time
            self.total_sessions = sessions
            if not self.timer_running:
                self.time_remaining = self.study_time * 60
                self.current_session = 0
                self.sessions_completed = 0
                self.update_display()
            return True
        return False
    
    def show_settings(self, parent_widget):
        # Show settings dialog - disabled during forced breaks
        if self.forced_break_mode:
            QMessageBox.warning(parent_widget, "Settings Locked", 
                              "Cannot change settings during forced break!\n"
                              "Please wait for the break to complete.")
            return False
        
        settings_dialog = PomodoroSettings(parent_widget)
        settings_dialog.study_spin.setValue(self.study_time)
        settings_dialog.break_spin.setValue(self.break_time)
        settings_dialog.sessions_spin.setValue(self.total_sessions)
        
        if settings_dialog.exec() == QDialog.DialogCode.Accepted:
            return self.set_times(
                settings_dialog.study_spin.value(), 
                settings_dialog.break_spin.value(),
                settings_dialog.sessions_spin.value()
            )
        return False


class PomodoroSettings(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Timer Settings")
        
        # RESPONSIVE SIZING - 20% of screen size
        if self.parent():
            screen = self.parent().screen()
            screen_size = screen.availableGeometry()
            dialog_width = int(screen_size.width() * 0.2)
            dialog_height = int(screen_size.height() * 0.2)
            self.setMinimumSize(dialog_width, dialog_height)
        else:
            self.setMinimumSize(350, 250)  # Fallback
        
        layout = QVBoxLayout()
        
        # Study time
        study_layout = QHBoxLayout()
        study_layout.addWidget(QLabel("Study Time (min):"))
        self.study_spin = QSpinBox()
        self.study_spin.setRange(1, 60)
        self.study_spin.setValue(25)
        study_layout.addWidget(self.study_spin)
        layout.addLayout(study_layout)
        
        # Break time
        break_layout = QHBoxLayout()
        break_layout.addWidget(QLabel("Break Time (min):"))
        self.break_spin = QSpinBox()
        self.break_spin.setRange(1, 30)
        self.break_spin.setValue(5)
        break_layout.addWidget(self.break_spin)
        layout.addLayout(break_layout)
        
        # Sessions
        sessions_layout = QHBoxLayout()
        sessions_layout.addWidget(QLabel("Sessions:"))
        self.sessions_spin = QSpinBox()
        self.sessions_spin.setRange(1, 10)
        self.sessions_spin.setValue(4)
        sessions_layout.addWidget(self.sessions_spin)
        layout.addLayout(sessions_layout)
        
        # Info label
        info_label = QLabel("Note: All breaks between sessions are forced for your well-being.")
        info_label.setStyleSheet("color: #6C7086; font-size: 10px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)