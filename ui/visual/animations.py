# FINAL PROJECT FLASHCARD APP / ui / visual / styles / animations.py

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve

class SidebarAnimations:
    def __init__(self, sidebar_widget):
        self.sidebar = sidebar_widget
        self.setup_animations()
    
    def setup_animations(self):
        # Animation for sidebar width
        self.width_animation = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.width_animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.width_animation.setDuration(300)
        
        self.max_width_animation = QPropertyAnimation(self.sidebar, b"maximumWidth")
        self.max_width_animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.max_width_animation.setDuration(300)
    
    def expand_sidebar(self, start_width=50, end_width=200):
        # Animate sidebar expansion
        self.width_animation.setStartValue(start_width)
        self.width_animation.setEndValue(end_width)
        self.max_width_animation.setStartValue(start_width)
        self.max_width_animation.setEndValue(end_width)
        
        self.width_animation.start()
        self.max_width_animation.start()
    
    def collapse_sidebar(self, start_width=200, end_width=50):
        # Animate sidebar collapse
        self.width_animation.setStartValue(start_width)
        self.width_animation.setEndValue(end_width)
        self.max_width_animation.setStartValue(start_width)
        self.max_width_animation.setEndValue(end_width)
        
        self.width_animation.start()
        self.max_width_animation.start()
    
    def get_animation_state(self):
        # Check if any animation is runnig
        return self.width_animation.state() == QPropertyAnimation.State.Running