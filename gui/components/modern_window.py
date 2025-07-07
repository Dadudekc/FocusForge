# gui/components/modern_window.py

"""Simplified redesigned GUI for FocusForge."""

from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QLineEdit,
    QComboBox,
    QStackedWidget,
    QProgressBar,
    QListWidgetItem,
)
from PyQt5.QtCore import Qt, QTimer

from ..dialogs.settings_dialog import SettingsDialog
from core.utils.database import Database
from core.engine.decision_engine import DecisionEngine


class MainWindow(QMainWindow):
    """Redesigned main window with sidebar navigation."""

    def __init__(self, distraction_detector, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("FocusForge")
        self.resize(900, 600)

        self.distraction_detector = distraction_detector
        self.db = Database()
        self.decision_engine = DecisionEngine(self.db, distraction_detector)
        self.distraction_detector.start_monitoring()

        self.is_work = True
        self.time_left = self.decision_engine.work_duration * 60
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.init_ui()

    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------
    def init_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        outer = QVBoxLayout(central)
        outer.setContentsMargins(10, 10, 10, 10)

        title = QLabel("FocusForge")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        outer.addWidget(title)

        layout = QHBoxLayout()
        outer.addLayout(layout, 1)

        # Sidebar navigation
        sidebar = QVBoxLayout()
        sidebar.setAlignment(Qt.AlignTop)
        self.dashboard_btn = QPushButton("Dashboard")
        self.tasks_btn = QPushButton("Tasks")
        self.analytics_btn = QPushButton("Analytics")
        self.settings_btn = QPushButton("Settings")
        for btn in [self.dashboard_btn, self.tasks_btn, self.analytics_btn, self.settings_btn]:
            sidebar.addWidget(btn)
        layout.addLayout(sidebar)

        # Stacked pages
        self.pages = QStackedWidget()
        layout.addWidget(self.pages, 1)

        self.init_dashboard_page()
        self.init_tasks_page()
        self.init_analytics_page()
        self.init_placeholder_page()

        self.dashboard_btn.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.tasks_btn.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        self.analytics_btn.clicked.connect(lambda: self.pages.setCurrentIndex(2))
        self.settings_btn.clicked.connect(self.show_settings)

        self.apply_styles()

    def init_dashboard_page(self) -> None:
        page = QWidget()
        layout = QVBoxLayout(page)

        self.timer_label = QLabel(self.format_time())
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        layout.addWidget(self.timer_label)

        btn_row = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        self.pause_btn = QPushButton("Pause")
        self.reset_btn = QPushButton("Reset")
        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(self.pause_btn)
        btn_row.addWidget(self.reset_btn)
        layout.addLayout(btn_row)

        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        self.metrics_label = QLabel()
        layout.addWidget(self.metrics_label)

        self.start_btn.clicked.connect(self.start_timer)
        self.pause_btn.clicked.connect(self.pause_timer)
        self.reset_btn.clicked.connect(self.reset_timer)

        self.pages.addWidget(page)

    def init_tasks_page(self) -> None:
        page = QWidget()
        layout = QVBoxLayout(page)

        input_row = QHBoxLayout()
        self.task_input = QLineEdit()
        self.priority_box = QComboBox()
        self.priority_box.addItems(["1 (High)", "2 (Medium)", "3 (Low)"])
        self.add_task_btn = QPushButton("Add")
        input_row.addWidget(self.task_input)
        input_row.addWidget(self.priority_box)
        input_row.addWidget(self.add_task_btn)
        layout.addLayout(input_row)

        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        self.add_task_btn.clicked.connect(self.add_task)

        self.pages.addWidget(page)

    def init_analytics_page(self) -> None:
        page = QWidget()
        layout = QVBoxLayout(page)

        self.analytics_progress = QProgressBar()
        layout.addWidget(self.analytics_progress)

        self.analytics_label = QLabel()
        layout.addWidget(self.analytics_label)

        self.pages.addWidget(page)

    def init_placeholder_page(self) -> None:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Use the sidebar to open settings."))
        self.pages.addWidget(page)

    def show_settings(self) -> None:
        dialog = SettingsDialog(self.decision_engine, self)
        if dialog.exec_():
            self.time_left = self.decision_engine.work_duration * 60
            self.update_timer_label()

    # ------------------------------------------------------------------
    # Timer helpers
    # ------------------------------------------------------------------
    def format_time(self) -> str:
        minutes, seconds = divmod(self.time_left, 60)
        return f"{int(minutes):02d}:{int(seconds):02d}"

    def update_timer_label(self) -> None:
        self.timer_label.setText(self.format_time())

    def start_timer(self) -> None:
        if not self.timer.isActive():
            self.timer.start(1000)

    def pause_timer(self) -> None:
        if self.timer.isActive():
            self.timer.stop()

    def reset_timer(self) -> None:
        self.timer.stop()
        self.is_work = True
        self.time_left = self.decision_engine.work_duration * 60
        self.update_timer_label()

    def update_timer(self) -> None:
        self.time_left -= 1
        if self.time_left <= 0:
            if self.is_work:
                self.time_left = self.decision_engine.break_duration * 60
            else:
                self.time_left = self.decision_engine.work_duration * 60
            self.is_work = not self.is_work
        self.update_timer_label()

    def add_task(self) -> None:
        title = self.task_input.text().strip()
        if not title:
            return
        priority = self.priority_box.currentText()[0]
        item = QListWidgetItem(f"[{priority}] {title}")
        self.task_list.addItem(item)
        self.task_input.clear()

    # ------------------------------------------------------------------
    # Styling helpers
    # ------------------------------------------------------------------
    def apply_styles(self) -> None:
        """Apply a vibrant yet clean stylesheet to the window."""
        self.setStyleSheet(
            """
            QWidget { font-size: 14px; }
            QPushButton { background-color: #3498db; color: white; padding: 6px; border: none; border-radius: 4px; }
            QPushButton:hover { background-color: #2980b9; }
            QProgressBar { height: 16px; border-radius: 8px; background: #eee; }
            QProgressBar::chunk { background-color: #2ecc71; border-radius: 8px; }
            QListWidget { background: white; }
            """
        )
