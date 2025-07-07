"""
GUI package for FocusForge.
"""

# Use the redesigned window by default
from .components.modern_window import MainWindow
from .components.splash_screen import SplashScreen
from .dialogs.settings_dialog import SettingsDialog

__all__ = ['MainWindow', 'SplashScreen', 'SettingsDialog']
