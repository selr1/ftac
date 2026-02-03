from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QEvent
from tagqt.ui.theme import Theme


class ToastType:
    SUCCESS = "success"
    ERROR = "error"
    INFO = "info"


class ToastWidget(QWidget):
    def __init__(self, message, parent=None, duration=3000, toast_type=ToastType.INFO):
        super().__init__(parent)
        self.raise_()
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QLabel(message)
        
        color_map = {
            ToastType.SUCCESS: "#22c55e",
            ToastType.ERROR: Theme.RED,
            ToastType.INFO: Theme.ACCENT,
        }
        bg_color = color_map.get(toast_type, Theme.ACCENT)
        
        self.label.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {Theme.TOAST_TEXT};
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
            }}
        """)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.adjustSize()
        self.layout.addWidget(self.label)
        
        self.adjustSize()
        
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(200)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.OutCubic)
        
        self.fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out.setDuration(200)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.InQuad)
        self.fade_out.finished.connect(self.close)
        
        self.timer = None
        if duration > 0:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.start_fade_out)
            self.timer.start(duration)
            
        self.fade_in.start()

    def stop_timer(self):
        if self.timer and self.timer.isActive():
            self.timer.stop()

    def start_fade_out(self):
        self.stop_timer()
        if self.fade_in.state() == QPropertyAnimation.Running:
            self.fade_in.stop()
            current_opacity = self.opacity_effect.opacity()
            self.fade_out.setStartValue(current_opacity)
        self.fade_out.start()
        
    def mousePressEvent(self, event):
        self.start_fade_out()


class ToastManager(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.layout.setContentsMargins(0, 0, 0, 50)
        self.layout.setSpacing(10)
        
        self.current_toast = None
        
        if parent:
            self.resize(parent.size())
            parent.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.parent() and event.type() == QEvent.Resize:
            self.resize(event.size())
        return super().eventFilter(obj, event)

    def show_message(self, message, duration=3000, toast_type=ToastType.INFO):
        if self.current_toast:
            try:
                self.current_toast.stop_timer()
                self.current_toast.close()
                self.current_toast.deleteLater()
            except RuntimeError:
                pass
            self.current_toast = None
            
        self._spawn_toast(message, duration, toast_type)

    def show_success(self, message, duration=3000):
        self.show_message(message, duration, ToastType.SUCCESS)

    def show_error(self, message, duration=3000):
        self.show_message(message, duration, ToastType.ERROR)

    def _spawn_toast(self, message, duration, toast_type):
        toast = ToastWidget(message, self.parent(), duration, toast_type)
        self.current_toast = toast
        toast.show()
        
        target_y = self.parent().height() - 60 - toast.height()
        target_x = (self.parent().width() - toast.width()) // 2
        
        toast.move(target_x, target_y)
