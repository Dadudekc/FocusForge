from PyQt5.QtWidgets import QLabel, QGraphicsOpacityEffect
from PyQt5.QtCore import (Qt, QPropertyAnimation, QParallelAnimationGroup, 
                         QSequentialAnimationGroup, QEasingCurve, QTimer)
from PyQt5.QtGui import QColor, QPalette, QFont
import json
from pathlib import Path
from datetime import datetime

class AnimatedLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                background-color: rgba(0, 0, 0, 0.7);
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.setAlignment(Qt.AlignCenter)
        
        # Set up opacity effect
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)
        
    def show_animation(self, duration=1000):
        # Create fade in animation
        fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        fade_in.setDuration(duration // 2)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Create fade out animation
        fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        fade_out.setDuration(duration // 2)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Create sequential animation group
        self.animation_group = QSequentialAnimationGroup()
        self.animation_group.addAnimation(fade_in)
        self.animation_group.addAnimation(fade_out)
        
        # Start animation
        self.animation_group.start()

class XPAnimation:
    def __init__(self, parent_widget):
        self.parent = parent_widget
        self.setup_animations()
        
    def setup_animations(self):
        # Create level up label
        self.level_up_label = AnimatedLabel("Level Up!", self.parent)
        self.level_up_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.level_up_label.hide()
        
        # Create XP gain label
        self.xp_gain_label = AnimatedLabel("", self.parent)
        self.xp_gain_label.setFont(QFont("Arial", 12))
        self.xp_gain_label.hide()
        
    def show_level_up(self, skill_name, new_level):
        self.level_up_label.setText(f"🎉 {skill_name} Level {new_level}!")
        self.level_up_label.setGeometry(
            self.parent.width() // 2 - 100,
            self.parent.height() // 2 - 50,
            200,
            50
        )
        self.level_up_label.show()
        self.level_up_label.show_animation(2000)
        
    def show_xp_gain(self, amount, skill_name):
        self.xp_gain_label.setText(f"+{amount} {skill_name}")
        self.xp_gain_label.setGeometry(
            self.parent.width() - 150,
            10,
            140,
            30
        )
        self.xp_gain_label.show()
        self.xp_gain_label.show_animation(1000)
        
    def animate_progress_bar(self, progress_bar, new_value, duration=500):
        # Create progress animation
        animation = QPropertyAnimation(progress_bar, b"value")
        animation.setDuration(duration)
        animation.setStartValue(progress_bar.value())
        animation.setEndValue(new_value)
        animation.setEasingCurve(QEasingCurve.OutQuad)
        
        # Create color pulse animation
        def pulse_color():
            progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #3D3D3D;
                    border-radius: 3px;
                    text-align: center;
                    background-color: #2D2D2D;
                }
                QProgressBar::chunk {
                    background-color: #00FF00;
                    border-radius: 2px;
                }
            """)
            QTimer.singleShot(200, lambda: progress_bar.setStyleSheet("""
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
            """))
            
        # Start animations
        animation.start()
        pulse_color()

class DevlogWriter:
    def __init__(self, filename="devlog.md"):
        self.filename = filename
        
    def log_xp_event(self, skill_name, amount, task_name, leveled_up=False):
        """Log an XP event to the devlog"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if leveled_up:
            message = f"\n## {timestamp} - {skill_name} Level Up!\n\n"
            message += f"**{skill_name}** has reached a new level of mastery!\n\n"
            message += f"The Dreamer's power grows as they complete: **{task_name}**\n\n"
            message += "---\n"
        else:
            message = f"\n### {timestamp}\n\n"
            message += f"[+{amount} {skill_name}] from completing: **{task_name}**\n\n"
            message += "---\n"
            
        try:
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(message)
        except Exception as e:
            print(f"Error writing to devlog: {e}") 