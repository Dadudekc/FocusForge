# gui/main_window.py

import sys
import time
import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout,
    QWidget, QLabel, QLineEdit, QMessageBox, QListWidget, QComboBox,
    QTableWidget, QTableWidgetItem, QProgressBar, QTabWidget, QHBoxLayout, QFrame
)
from PyQt5.QtCore import QTimer, Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from database import Database
from decision_engine import DecisionEngine
from focus_report import FocusReport
from gui.settings_dialog import SettingsDialog

class MainWindow(QMainWindow):
    def __init__(self, distraction_detector, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("MainWindow __init__ called with distraction_detector:", distraction_detector)
        self.setWindowTitle("Focus Forge AI Agent")
        self.setFixedSize(1000, 700)  # Increased size for better layout
        self.distraction_detector = distraction_detector
        self.db = Database()
        self.decision_engine = DecisionEngine(self.db, self.distraction_detector)
        self.distraction_detector.start_monitoring()

        # Initialize time_left before calling init_ui
        self.is_work = True
        self.time_left = self.decision_engine.work_duration * 60  # in seconds
        self.distractions = 0

        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

    def init_ui(self):
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Layout
        main_layout = QVBoxLayout()

        # Tabs
        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        # Tab 1: Dashboard
        dashboard_tab = QWidget()
        dashboard_layout = QVBoxLayout()

        # Timer Display
        self.timer_label = QLabel(self.format_time())
        self.timer_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        self.timer_label.setAlignment(Qt.AlignCenter)
        dashboard_layout.addWidget(self.timer_label)

        # Timer Controls
        controls_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_timer)
        controls_layout.addWidget(self.start_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_timer)
        controls_layout.addWidget(self.pause_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_timer)
        controls_layout.addWidget(self.reset_button)

        dashboard_layout.addLayout(controls_layout)

        # Focus Progress Bar
        self.focus_progress = QProgressBar()
        self.focus_progress.setRange(0, 100)
        dashboard_layout.addWidget(self.focus_progress)
        print("Calling update_dashboard_focus_progress()")
        self.update_dashboard_focus_progress()

        # Performance Metrics
        self.metrics_label = QLabel()
        self.metrics_label.setStyleSheet("font-size: 14px;")
        dashboard_layout.addWidget(self.metrics_label)
        self.update_dashboard_metrics()

        # Add Dashboard Layout to Tab
        dashboard_tab.setLayout(dashboard_layout)
        tabs.addTab(dashboard_tab, "Dashboard")
        print("Dashboard tab initialized.")

        # Tab 2: Tasks
        tasks_tab = QWidget()
        tasks_layout = QVBoxLayout()

        # Task Input Section
        task_input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter your task here")
        task_input_layout.addWidget(self.task_input)

        self.priority_input = QComboBox()
        self.priority_input.addItems(["1 (High)", "2 (Medium)", "3 (Low)"])
        task_input_layout.addWidget(self.priority_input)

        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.add_task)
        task_input_layout.addWidget(self.add_task_button)

        tasks_layout.addLayout(task_input_layout)

        # Task List
        self.task_list = QListWidget()
        self.task_list.setFixedHeight(150)
        tasks_layout.addWidget(self.task_list)
        self.load_tasks()

        tasks_tab.setLayout(tasks_layout)
        tabs.addTab(tasks_tab, "Tasks")

        # Tab 3: Session History
        history_tab = QWidget()
        history_layout = QVBoxLayout()

        # Session History Table
        self.session_table = QTableWidget()
        self.session_table.setColumnCount(6)
        self.session_table.setHorizontalHeaderLabels(["Task", "Work Planned", "Work Actual", "Break Taken", "Distractions", "Completed"])
        self.session_table.horizontalHeader().setStretchLastSection(True)
        self.session_table.setEditTriggers(QTableWidget.NoEditTriggers)
        history_layout.addWidget(self.session_table)
        self.load_sessions()

        history_tab.setLayout(history_layout)
        tabs.addTab(history_tab, "Session History")

        # Tab 4: Analytics
        analytics_tab = QWidget()
        analytics_layout = QVBoxLayout()

        # Focus Progress Bar for Analytics
        self.focus_progress_analytics = QProgressBar()
        self.focus_progress_analytics.setRange(0, 100)
        analytics_layout.addWidget(self.focus_progress_analytics)
        print("Calling update_analytics_focus_progress()")
        self.update_analytics_focus_progress()

        # Performance Metrics for Analytics
        self.metrics_label_analytics = QLabel()
        self.metrics_label_analytics.setStyleSheet("font-size: 14px;")
        analytics_layout.addWidget(self.metrics_label_analytics)
        self.update_analytics_metrics()

        # Analytics Plots
        self.figure = plt.figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        analytics_layout.addWidget(self.canvas)
        self.plot_session_history()

        analytics_tab.setLayout(analytics_layout)
        tabs.addTab(analytics_tab, "Analytics")
        print("Analytics tab initialized.")

        # Tab 5: Reports
        reports_tab = QWidget()
        reports_layout = QVBoxLayout()

        self.generate_report_button = QPushButton("Generate Focus Report")
        self.generate_report_button.clicked.connect(self.generate_report)
        reports_layout.addWidget(self.generate_report_button)

        self.report_output = QLabel("")
        self.report_output.setWordWrap(True)
        reports_layout.addWidget(self.report_output)

        reports_tab.setLayout(reports_layout)
        tabs.addTab(reports_tab, "Reports")

        # Add Tabs to Main Layout
        main_layout.addWidget(tabs)

        # Set Main Layout
        central_widget.setLayout(main_layout)

        # Apply Stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F0F0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit, QComboBox, QListWidget, QTableWidget, QProgressBar {
                font-size: 14px;
            }
            QLabel {
                font-size: 16px;
            }
        """)

    # Dashboard Specific Update Methods
    def update_dashboard_focus_progress(self):
        """
        Updates the Dashboard's focus progress bar based on success rate.
        """
        success_rate = self.db.get_success_rate()
        self.focus_progress.setValue(int(success_rate))
        self.focus_progress.setFormat(f"Success Rate: {success_rate:.2f}%")

    def update_dashboard_metrics(self):
        """
        Updates performance metrics in the Dashboard tab.
        """
        success_rate = self.db.get_success_rate()
        avg_work = self.db.get_average_work_duration()
        avg_distractions = self.db.get_average_distractions()

        metrics_text = f"""
        <h3>Performance Metrics</h3>
        <p><b>Success Rate:</b> {success_rate:.2f}%</p>
        <p><b>Average Work Duration:</b> {avg_work:.2f} minutes</p>
        <p><b>Average Distractions per Session:</b> {avg_distractions:.2f}</p>
        """
        self.metrics_label.setText(metrics_text)

    # Analytics Specific Update Methods
    def update_analytics_focus_progress(self):
        """
        Updates the Analytics' focus progress bar based on success rate.
        """
        success_rate = self.db.get_success_rate()
        self.focus_progress_analytics.setValue(int(success_rate))
        self.focus_progress_analytics.setFormat(f"Success Rate: {success_rate:.2f}%")

    def update_analytics_metrics(self):
        """
        Updates performance metrics in the Analytics tab.
        """
        success_rate = self.db.get_success_rate()
        avg_work = self.db.get_average_work_duration()
        avg_distractions = self.db.get_average_distractions()

        metrics_text = f"""
        <h3>Performance Metrics</h3>
        <p><b>Success Rate:</b> {success_rate:.2f}%</p>
        <p><b>Average Work Duration:</b> {avg_work:.2f} minutes</p>
        <p><b>Average Distractions per Session:</b> {avg_distractions:.2f}</p>
        """
        self.metrics_label_analytics.setText(metrics_text)

    def add_task(self):
        description = self.task_input.text().strip()
        priority_text = self.priority_input.currentText()
        priority = int(priority_text.split()[0])  # Extract priority number from text

        if description:
            self.db.add_task(description, priority)
            self.load_tasks()
            self.task_input.clear()
            QMessageBox.information(self, "Task Added", f"Task '{description}' added successfully.")
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a task description.")

    def load_tasks(self):
        self.task_list.clear()
        tasks = self.db.get_pending_tasks()
        for task in tasks:
            self.task_list.addItem(f"{task[1]} (Priority: {task[2]})")

    def get_current_task(self):
        selected_items = self.task_list.selectedItems()
        if selected_items:
            selected_item = selected_items[0].text()
            task_description = selected_item.split(" (Priority:")[0]
            return task_description
        # If no task is selected, default to the highest priority task
        pending_tasks = self.db.get_pending_tasks()
        return pending_tasks[0][1] if pending_tasks else "No Task"

    def start_timer(self):
        if not self.timer.isActive():
            self.timer.start(1000)  # Update every second
            print("Timer started.")

    def pause_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            print("Timer paused.")

    def reset_timer(self):
        self.timer.stop()
        self.is_work = True
        self.time_left = self.decision_engine.work_duration * 60
        self.timer_label.setText(self.format_time())
        # Log the session as incomplete
        self.log_session(completed=False)
        QMessageBox.information(self, "Session Reset", "The current session has been reset and logged.")

    def format_time(self):
        """
        Ensures time is formatted correctly as MM:SS.
        Converts NumPy arrays to integers if necessary.
        """
        if isinstance(self.time_left, np.ndarray):
            self.time_left = int(self.time_left.item())

        mins, secs = divmod(self.time_left, 60)
        return f"{mins:02d}:{secs:02d}"

    def update_timer(self):
        """
        Updates the countdown timer and handles session transitions.
        """
        if isinstance(self.time_left, np.ndarray):
            self.time_left = int(self.time_left.item())

        if self.time_left > 0:
            self.time_left = max(0, self.time_left - 1)  # Ensure it never goes below zero
            self.timer_label.setText(self.format_time())  # No argument needed
        else:
            self.timer.stop()  # Stop the countdown when the timer reaches zero

            if self.is_work:
                # Switch to break mode
                self.is_work = False
                self.time_left = self.decision_engine.break_duration * 60
                self.timer_label.setText(self.format_time())

                # Notify the user
                QMessageBox.information(self, "Break Time", "Time for a break!")

                # Log completed work session
                self.log_session(completed=True)

                # Apply AI-based session adjustments
                new_work, new_break = self.decision_engine.apply_rules()
                self.decision_engine.work_duration = new_work
                self.decision_engine.break_duration = new_break
                self.time_left = new_work * 60  # Set next work duration
                self.load_tasks()
            else:
                # Switch to work mode
                self.is_work = True
                self.time_left = self.decision_engine.work_duration * 60
                self.timer_label.setText(self.format_time())

                # Notify the user
                QMessageBox.information(self, "Work Time", "Time to focus on your task!")

            # Update UI elements
            self.update_dashboard_focus_progress()
            self.update_dashboard_metrics()
            self.update_analytics_focus_progress()
            self.update_analytics_metrics()
            self.plot_session_history()

    def log_session(self, completed):
        """
        Logs the session details into the database.
        """
        task = self.get_current_task()
        distractions = self.distraction_detector.logger.get_summary()["total_distractions"]
        self.db.log_session(
            work_planned=self.decision_engine.work_duration,
            work_actual=(self.decision_engine.work_duration * 60 - self.time_left) / 60 if completed else (self.decision_engine.work_duration * 60 - self.time_left) / 60,
            break_taken=1 if not self.is_work else 0,
            break_duration=self.decision_engine.break_duration if not self.is_work else 0,
            task=task,
            completed=1 if completed else 0,
            distractions=distractions
        )
        self.distraction_detector.logger.logs.clear()  # Clear logs after logging the session
        self.load_sessions()
        self.plot_session_history()

        # Update UI elements
        self.update_dashboard_focus_progress()
        self.update_dashboard_metrics()
        self.update_analytics_focus_progress()
        self.update_analytics_metrics()

    def load_sessions(self):
        """
        Loads recent sessions into the session history table.
        """
        sessions = self.db.get_recent_sessions(limit=20)
        self.session_table.setRowCount(len(sessions))
        for row, session in enumerate(sessions):
            # session indices:
            # 0: id, 1: work_planned, 2: work_actual, 3: break_taken, 4: break_duration,
            # 5: task, 6: completed, 7: distraction_events, 8: timestamp
            self.session_table.setItem(row, 0, QTableWidgetItem(session[5]))
            self.session_table.setItem(row, 1, QTableWidgetItem(str(session[1])))
            self.session_table.setItem(row, 2, QTableWidgetItem(str(session[2])))
            self.session_table.setItem(row, 3, QTableWidgetItem("Yes" if session[3] else "No"))
            self.session_table.setItem(row, 4, QTableWidgetItem(str(session[7])))
            self.session_table.setItem(row, 5, QTableWidgetItem("Yes" if session[6] else "No"))

    def update_dashboard_focus_progress(self):
        """
        Updates the Dashboard's focus progress bar based on success rate.
        """
        success_rate = self.db.get_success_rate()
        self.focus_progress.setValue(int(success_rate))
        self.focus_progress.setFormat(f"Success Rate: {success_rate:.2f}%")

    def update_dashboard_metrics(self):
        """
        Updates performance metrics in the Dashboard tab.
        """
        success_rate = self.db.get_success_rate()
        avg_work = self.db.get_average_work_duration()
        avg_distractions = self.db.get_average_distractions()

        metrics_text = f"""
        <h3>Performance Metrics</h3>
        <p><b>Success Rate:</b> {success_rate:.2f}%</p>
        <p><b>Average Work Duration:</b> {avg_work:.2f} minutes</p>
        <p><b>Average Distractions per Session:</b> {avg_distractions:.2f}</p>
        """
        self.metrics_label.setText(metrics_text)

    def update_analytics_focus_progress(self):
        """
        Updates the Analytics' focus progress bar based on success rate.
        """
        success_rate = self.db.get_success_rate()
        self.focus_progress_analytics.setValue(int(success_rate))
        self.focus_progress_analytics.setFormat(f"Success Rate: {success_rate:.2f}%")

    def update_analytics_metrics(self):
        """
        Updates performance metrics in the Analytics tab.
        """
        success_rate = self.db.get_success_rate()
        avg_work = self.db.get_average_work_duration()
        avg_distractions = self.db.get_average_distractions()

        metrics_text = f"""
        <h3>Performance Metrics</h3>
        <p><b>Success Rate:</b> {success_rate:.2f}%</p>
        <p><b>Average Work Duration:</b> {avg_work:.2f} minutes</p>
        <p><b>Average Distractions per Session:</b> {avg_distractions:.2f}</p>
        """
        self.metrics_label_analytics.setText(metrics_text)

    def plot_session_history(self):
        """
        Plots the work duration over sessions.
        """
        sessions = self.db.get_recent_sessions(limit=20)
        if not sessions:
            return
        sessions = sessions[::-1]  # Oldest first
        work_planned = [s[1] for s in sessions]
        work_actual = [s[2] for s in sessions]
        distractions = [s[7] for s in sessions]

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(work_planned, label='Planned Work Duration', marker='o')
        ax.plot(work_actual, label='Actual Work Duration', marker='x')
        ax.set_title('Work Duration Over Sessions')
        ax.set_xlabel('Session')
        ax.set_ylabel('Minutes')
        ax.legend()
        self.canvas.draw()

    def generate_report(self):
        """
        Generates a focus report and displays recommendations.
        """
        report = FocusReport()
        report.generate_report()
        report.export_csv()
        summary = report.get_summary()
        recommendations = report.get_recommendations()

        report_text = f"""
        <h3>Focus Report Summary</h3>
        <p><b>Total Sessions:</b> {len(report.logs)}</p>
        <p><b>Total Distractions:</b> {summary['total_distractions']}</p>
        <p><b>Distractions by Type:</b> {summary['by_type']}</p>
        <h4>Recommendations:</h4>
        <ul>
        """
        for rec in recommendations:
            report_text += f"<li>{rec}</li>"
        report_text += "</ul>"

        self.report_output.setText(report_text)

    def closeEvent(self, event):
        """
        Handles the application close event to stop monitoring and generate reports.
        """
        self.distraction_detector.stop_monitoring()
        # Generate final report
        focus_report = FocusReport()
        focus_report.generate_report()
        focus_report.export_csv()

        reply = QMessageBox.question(self, 'Quit',
                                     "Are you sure you want to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
