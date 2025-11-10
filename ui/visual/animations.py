# FINAL PROJECT FLASHCARD APP / ui / visual / styles / animations.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGraphicsOpacityEffect
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QObject

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
    
class FadeAnimation(QObject): #jose
    """Reusable fade in/out animation for any QWidget."""
    def __init__(self, widget, duration=600):
        super().__init__()
        self.widget = widget
        self.animation = QPropertyAnimation(widget, b"windowOpacity")
        self.animation.setDuration(duration)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def fade_in(self):
        self.widget.setWindowOpacity(0)
        self.widget.show()
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def fade_out(self, on_finished=None):
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        if on_finished:
            self.animation.finished.connect(on_finished)
        self.animation.start()
        
class FadeWidget(QWidget):
    def __init__(self, widget, parent_window):
        super().__init__()
        self.widget = widget
        self.parent_window = parent_window

        # Layout setup
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget)
        self.setLayout(layout)

        # Opacity effect
        self.effect = QGraphicsOpacityEffect()
        self.widget.setGraphicsEffect(self.effect)
        self.anim = None

    def fade_in(self):
        self.anim = QPropertyAnimation(self.effect, b"opacity")
        self.anim.setDuration(600)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anim.start()

    def fade_out(self, next_widget=None, on_finish=None):
        """
        Fade out this widget.
        :param next_widget: FadeWidget to fade in next (optional)
        :param on_finish: callback to run after fade completes (optional)
        """
        self.anim = QPropertyAnimation(self.effect, b"opacity")
        self.anim.setDuration(600)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anim.finished.connect(lambda: self.switch_page(next_widget, on_finish))
        self.anim.start()

    def switch_page(self, next_widget=None, on_finish=None):
        """Safely handle switching or running callback after fade."""
        if next_widget is not None:
            try:
                next_widget.fade_in()
                if hasattr(self.parent_window, "stacked"):
                    self.parent_window.stacked.setCurrentWidget(next_widget)
            except Exception:
                pass

        if callable(on_finish):
            try:
                on_finish()
            except Exception:
                pass
            
