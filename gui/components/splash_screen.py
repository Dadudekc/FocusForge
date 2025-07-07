from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt, QTimer


class SplashScreen(QWidget):
    """Lightweight splash screen with an indeterminate progress bar."""

    def __init__(self, duration=2000, parent=None):
        super().__init__(parent, Qt.SplashScreen | Qt.FramelessWindowHint)
        self.setFixedSize(300, 200)
        self.duration = duration

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("FocusForge", self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addStretch()
        layout.addWidget(title)

        self.progress = QProgressBar(self)
        self.progress.setRange(0, 0)  # Infinite progress
        layout.addWidget(self.progress)
        layout.addStretch()

    def launch(self, callback):
        """Show the splash, wait for *duration* ms, then invoke callback."""
        self.show()
        QTimer.singleShot(self.duration, lambda: (self.close(), callback()))
