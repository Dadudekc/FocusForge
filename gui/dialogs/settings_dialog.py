from PyQt5.QtWidgets import QDialog, QPushButton, QFormLayout, QSpinBox, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt

class SettingsDialog(QDialog):
    """Modal dialog that allows users to tweak Pomodoro and UI settings."""

    def __init__(self, decision_engine, parent=None):
        super().__init__(parent)
        self.decision_engine = decision_engine
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 300)

        # Main layout
        layout = QFormLayout(self)

        # Work Duration Setting
        self.work_duration_spin = QSpinBox()
        self.work_duration_spin.setRange(15, 60)
        self.work_duration_spin.setValue(self.decision_engine.work_duration)
        layout.addRow("Default Work Duration (min):", self.work_duration_spin)

        # Break Duration Setting
        self.break_duration_spin = QSpinBox()
        self.break_duration_spin.setRange(5, 30)
        self.break_duration_spin.setValue(self.decision_engine.break_duration)
        layout.addRow("Default Break Duration (min):", self.break_duration_spin)

        # Reinforcement Learning Toggle
        self.rl_toggle = QCheckBox("Enable Reinforcement Learning Optimization")
        self.rl_toggle.setChecked(self.decision_engine.model is not None)
        layout.addRow(self.rl_toggle)

        # Dark Mode Toggle
        self.dark_mode_toggle = QCheckBox("Enable Dark Mode")
        self.dark_mode_toggle.stateChanged.connect(self.toggle_dark_mode)
        layout.addRow(self.dark_mode_toggle)

        # Save Button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        layout.addRow(save_button)

        self.setLayout(layout)

    # --------------------------- UI Helpers --------------------------- #

    def toggle_dark_mode(self, state: int):
        """Toggle application-wide dark mode by setting parent stylesheet."""
        if self.parent() is None:
            return  # should not happen, defensive coding

        if state == Qt.Checked:
            self.parent().setStyleSheet(
                "QMainWindow { background-color: #2E2E2E; color: white; } "
                "QPushButton { background-color: #444444; color: white; } "
                "QLabel { color: white; }"
            )
        else:
            self.parent().setStyleSheet("")

    def save_settings(self):
        """Persist selected settings back into the decision engine and close dialog."""
        # Basic Pomodoro timings
        self.decision_engine.work_duration = self.work_duration_spin.value()
        self.decision_engine.break_duration = self.break_duration_spin.value()

        # Reinforcement Learning Toggle Logic
        if self.rl_toggle.isChecked() and not self.decision_engine.model:
            # In a real application we might prompt to train or load a model here
            QMessageBox.information(self, "RL Enabled", "Reinforcement Learning optimization is enabled.")
        elif not self.rl_toggle.isChecked() and self.decision_engine.model:
            QMessageBox.information(self, "RL Disabled", "Reinforcement Learning optimization is disabled.")
            self.decision_engine.model = None

        self.accept() 