from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QSize
from tagqt.ui.theme import Theme

class ToastWidget(QWidget):
    def __init__(self, message, parent=None, duration=3000, is_error=False):
        super().__init__(parent)
        # Ensure it stays on top
        self.raise_()
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QLabel(message)
        bg_color = Theme.RED if is_error else Theme.ACCENT
        # Add shadow/border for better visibility
        self.label.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: #ffffff;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
                border: 1px solid {Theme.SURFACE1};
            }}
        """)
        self.label.setAlignment(Qt.AlignCenter)
        # Adjust size to fit content
        self.label.adjustSize()
        self.layout.addWidget(self.label)
        
        self.adjustSize()
        
        # Opacity Effect
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        # Fade In
        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(250)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.OutCubic)
        
        # Fade Out (Separate object to avoid conflict)
        self.fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out.setDuration(250)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.InQuad) # Smooth exit
        self.fade_out.finished.connect(self.close)
        
        if duration > 0:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.start_fade_out)
            self.timer.start(duration)
            
        self.fade_in.start()

    def stop_timer(self):
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()

    def start_fade_out(self):
        self.stop_timer() # Ensure timer doesn't trigger again
        # If currently fading in, stop it
        if self.fade_in.state() == QPropertyAnimation.Running:
            self.fade_in.stop()
            # Start fade out from current opacity
            current_opacity = self.opacity_effect.opacity()
            self.fade_out.setStartValue(current_opacity)
            
        self.fade_out.start()
        
    def mousePressEvent(self, event):
        # Click to dismiss immediately
        self.start_fade_out()

class ToastManager(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # We'll use a layout to stack toasts at the bottom center
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.layout.setContentsMargins(0, 0, 0, 50) # 50px from bottom
        self.layout.setSpacing(10)
        
        self.current_toast = None
        
        # Resize to match parent initially
        if parent:
            self.resize(parent.size())
            parent.installEventFilter(self)

    def eventFilter(self, obj, event):
        from PySide6.QtCore import QEvent
        if obj == self.parent() and event.type() == QEvent.Resize:
            self.resize(event.size())
        return super().eventFilter(obj, event)

    def show_message(self, message, duration=3000, is_error=False):
        # Kill previous toast if it exists
        if self.current_toast:
            try:
                self.current_toast.stop_timer() # Stop any pending fade out
                self.current_toast.close()
                self.current_toast.deleteLater()
            except RuntimeError:
                pass
            self.current_toast = None
            
        self._spawn_toast(message, duration, is_error)

    def _spawn_toast(self, message, duration, is_error):
        toast = ToastWidget(message, self.parent(), duration, is_error)
        self.current_toast = toast
        toast.show()
        
        # Position it
        # Center at the bottom
        target_y = self.parent().height() - 60 - toast.height()
        target_x = (self.parent().width() - toast.width()) // 2
        
        toast.move(target_x, target_y)

