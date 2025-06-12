import sys
import json
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QListWidget, 
                            QListWidgetItem, QInputDialog, QMessageBox,
                            QTextEdit, QProgressBar, QFrame)
from PyQt5.QtCore import Qt, QMimeData, QTimer
from PyQt5.QtGui import QDrag, QColor, QFont
from meta_skills import MetaSkillManager, MetaSkill
from skill_animations import XPAnimation, DevlogWriter

class TaskCard(QListWidgetItem):
    def __init__(self, title, description="", xp_value=5, skill_target="Grit"):
        super().__init__(title)
        self.description = description
        self.xp_value = xp_value
        self.skill_target = skill_target
        self.setFlags(self.flags() | Qt.ItemIsDragEnabled)
        
    def to_dict(self):
        return {
            "title": self.text(),
            "description": self.description,
            "xp_value": self.xp_value,
            "skill_target": self.skill_target
        }
    
    @classmethod
    def from_dict(cls, data):
        card = cls(
            data["title"], 
            data["description"], 
            data["xp_value"],
            data.get("skill_target", "Grit")
        )
        return card

class SkillProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3D3D3D;
                border-radius: 3px;
                text-align: center;
                background-color: #2D2D2D;
            }
            QProgressBar::chunk {
                background-color: #4D4D4D;
                border-radius: 2px;
            }
        """)
        self.setTextVisible(True)
        self.setFormat("%v/%m XP")

class SkillWidget(QFrame):
    def __init__(self, skill: MetaSkill, parent=None):
        super().__init__(parent)
        self.skill = skill
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Skill header
        header = QLabel(f"{self.skill.icon} {self.skill.name} (Level {self.skill.level})")
        header.setStyleSheet("color: #FFFFFF; font-weight: bold;")
        layout.addWidget(header)
        
        # Progress bar
        self.progress = SkillProgressBar()
        self.update_progress()
        layout.addWidget(self.progress)
        
        # Description
        desc = QLabel(self.skill.description)
        desc.setStyleSheet("color: #CCCCCC; font-size: 10px;")
        layout.addWidget(desc)
        
        self.setStyleSheet("""
            QFrame {
                background-color: #2D2D2D;
                border: 1px solid #3D3D3D;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        
    def update_progress(self, animate=True):
        if animate and hasattr(self.parent(), 'animations'):
            self.parent().animations.animate_progress_bar(
                self.progress, 
                self.skill.xp
            )
        else:
            self.progress.setMaximum(self.skill.xp_to_next_level)
            self.progress.setValue(self.skill.xp)

class SkillOverlay(QWidget):
    def __init__(self, skill_manager: MetaSkillManager, parent=None):
        super().__init__(parent)
        self.skill_manager = skill_manager
        self.devlog = DevlogWriter()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("🧠 Meta Skills")
        title.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        layout.addWidget(title)
        
        # Skills
        self.skill_widgets = {}
        for skill in self.skill_manager.get_all_skills():
            widget = SkillWidget(skill)
            self.skill_widgets[skill.name] = widget
            layout.addWidget(widget)
            
        # XP Log
        self.xp_log = QTextEdit()
        self.xp_log.setReadOnly(True)
        self.xp_log.setStyleSheet("""
            QTextEdit {
                background-color: #1D1D1D;
                color: #CCCCCC;
                border: 1px solid #3D3D3D;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        self.xp_log.setMaximumHeight(100)
        layout.addWidget(self.xp_log)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #2D2D2D;
                border: 1px solid #3D3D3D;
                border-radius: 5px;
            }
        """)
        
    def log_xp(self, message: str, skill_name: str, amount: int, task_name: str, leveled_up: bool):
        # Add to UI log
        self.xp_log.append(message)
        self.xp_log.verticalScrollBar().setValue(
            self.xp_log.verticalScrollBar().maximum()
        )
        
        # Log to devlog
        self.devlog.log_xp_event(skill_name, amount, task_name, leveled_up)
        
    def update_skills(self):
        for widget in self.skill_widgets.values():
            widget.update_progress()

class KantuColumn(QListWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QListWidget.DragDrop)
        self.setStyleSheet("""
            QListWidget {
                background-color: #2D2D2D;
                border: 1px solid #3D3D3D;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                background-color: #3D3D3D;
                border: 1px solid #4D4D4D;
                border-radius: 3px;
                padding: 5px;
                margin: 2px;
                color: #FFFFFF;
            }
            QListWidget::item:selected {
                background-color: #4D4D4D;
            }
        """)
        
        # Add column title
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-taskcard"):
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-taskcard"):
            event.accept()
            data = event.mimeData().data("application/x-taskcard")
            task_data = json.loads(data.data().decode())
            card = TaskCard.from_dict(task_data)
            self.addItem(card)
            
            # If dropped in Done column, award XP
            if self.title_label.text() == "Done":
                self.parent().award_xp(card)
        else:
            event.ignore()

class KantuBoard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kantu Board - Focus Forge")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1D1D1D;
            }
        """)
        
        # Initialize skill manager
        self.skill_manager = MetaSkillManager()
        
        # Initialize animations
        self.animations = XPAnimation(self)
        
        # Initialize UI
        self.init_ui()
        
        # Load tasks
        self.load_tasks()
        
    def init_ui(self):
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create board layout
        board_layout = QVBoxLayout()
        
        # Create columns
        self.backlog = KantuColumn("Backlog")
        self.now = KantuColumn("Now")
        self.done = KantuColumn("Done")
        
        # Add columns to layout
        columns_layout = QHBoxLayout()
        columns_layout.addWidget(self.backlog)
        columns_layout.addWidget(self.now)
        columns_layout.addWidget(self.done)
        board_layout.addLayout(columns_layout)
        
        # Add task button
        add_button = QPushButton("Add Task")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #4D4D4D;
                color: #FFFFFF;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #5D5D5D;
            }
        """)
        add_button.clicked.connect(self.add_task)
        board_layout.addWidget(add_button)
        
        # Add board to main layout
        main_layout.addLayout(board_layout)
        
        # Add skill overlay
        self.skill_overlay = SkillOverlay(self.skill_manager)
        main_layout.addWidget(self.skill_overlay)
        
        # Set window size
        self.setMinimumSize(1000, 600)
        
    def add_task(self):
        title, ok = QInputDialog.getText(self, "Add Task", "Task Title:")
        if ok and title:
            description, ok = QInputDialog.getText(self, "Add Task", "Task Description:")
            if ok:
                # Get skill target
                skills = list(self.skill_manager.skills.keys())
                skill, ok = QInputDialog.getItem(
                    self, "Add Task", "Target Skill:", skills, 0, False
                )
                if ok and skill:
                    # Get XP value
                    xp, ok = QInputDialog.getInt(
                        self, "Add Task", "XP Value:", 5, 1, 100, 1
                    )
                    if ok:
                        card = TaskCard(title, description, xp, skill)
                        self.backlog.addItem(card)
                        self.save_tasks()
                
    def award_xp(self, card: TaskCard):
        old_level = self.skill_manager.get_skill(card.skill_target).level
        message = self.skill_manager.add_xp(card.skill_target, card.xp_value)
        
        if message:
            # Show XP gain animation
            self.animations.show_xp_gain(card.xp_value, card.skill_target)
            
            # Check for level up
            new_level = self.skill_manager.get_skill(card.skill_target).level
            if new_level > old_level:
                self.animations.show_level_up(card.skill_target, new_level)
                self.skill_overlay.log_xp(
                    f"🎉 {card.skill_target} leveled up to {new_level}!",
                    card.skill_target,
                    card.xp_value,
                    card.text(),
                    True
                )
            else:
                self.skill_overlay.log_xp(
                    message,
                    card.skill_target,
                    card.xp_value,
                    card.text(),
                    False
                )
            
            self.skill_overlay.update_skills()
                
    def save_tasks(self):
        tasks = {
            "backlog": [item.to_dict() for item in self.get_items(self.backlog)],
            "now": [item.to_dict() for item in self.get_items(self.now)],
            "done": [item.to_dict() for item in self.get_items(self.done)]
        }
        
        with open("tasks.json", "w") as f:
            json.dump(tasks, f, indent=2)
            
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                tasks = json.load(f)
                
            for task in tasks.get("backlog", []):
                self.backlog.addItem(TaskCard.from_dict(task))
            for task in tasks.get("now", []):
                self.now.addItem(TaskCard.from_dict(task))
            for task in tasks.get("done", []):
                self.done.addItem(TaskCard.from_dict(task))
        except FileNotFoundError:
            # Create sample tasks for first run
            sample_tasks = [
                TaskCard("Initialize Focus Forge", "Set up core architecture", 10, "Grit"),
                TaskCard("Design UI Framework", "Create base UI components", 5, "Precision"),
                TaskCard("Implement Database", "Set up SQLite schema", 8, "Discipline")
            ]
            for task in sample_tasks:
                self.backlog.addItem(task)
            self.save_tasks()
            
    def get_items(self, list_widget):
        return [list_widget.item(i) for i in range(list_widget.count())]
        
    def closeEvent(self, event):
        self.save_tasks()
        event.accept()

def main():
    app = QApplication(sys.argv)
    board = KantuBoard()
    board.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 