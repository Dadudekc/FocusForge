import time
import json
from datetime import datetime
from pathlib import Path
from ..utils.database import Database
from .activity_monitor import ActivityMonitor
from .distraction_logger import DistractionLogger
from pynput import keyboard, mouse
from transformers import pipeline
from threading import Thread, Event
import pygetwindow as gw

class AdvancedDistractionDetector:
    def __init__(self):
        self.db = Database()
        self.activity_monitor = ActivityMonitor()
        self.distraction_logger = DistractionLogger()
        self.is_monitoring = False
        self.last_activity_time = time.time()
        self.inactivity_threshold = 300
        self.check_interval = 5
        self.work_apps = ["ChatGPT", "Cursor", "VS Code", "PyCharm"]

        # AI-based distraction detection model
        self.classifier = pipeline("text-classification", model="facebook/bart-large-mnli")

        # Logging system
        self.logger = DistractionLogger()
        self.last_active_window = None
        self.last_switch_time = time.time()

        # Threading for background monitoring
        self.stop_event = Event()
        self.monitoring = False

        # Start keyboard & mouse tracking
        self.keyboard_listener = keyboard.Listener(on_press=self.on_activity)
        self.mouse_listener = mouse.Listener(on_move=self.on_activity, on_click=self.on_activity)
        self.keyboard_listener.start()
        self.mouse_listener.start()

        self.distraction_events = 0  # Example attribute to track distractions

    def on_activity(self, *args):
        """ Resets last activity timestamp when user interacts. """
        self.last_activity_time = time.time()

    def is_inactive(self):
        """ Returns True if user is inactive beyond threshold. """
        return (time.time() - self.last_activity_time) > self.inactivity_threshold

    def get_active_window(self):
        """ Returns the title of the currently active window. """
        active_window = gw.getActiveWindow()
        return active_window.title if active_window else "Unknown"

    def detect_off_task_window(self):
        """ Detects if the active window is non-work related and logs it. """
        active_window = self.get_active_window()

        if active_window and active_window != self.last_active_window:
            switch_duration = time.time() - self.last_switch_time
            self.logger.log_event("App Switch", {
                "previous_window": self.last_active_window,
                "new_window": active_window,
                "duration_in_previous_window": round(switch_duration, 2)
            })
            self.last_switch_time = time.time()
            self.last_active_window = active_window

        if active_window and any(app in active_window for app in self.work_apps):
            self.logger.log_event("Work App Usage", {"window": active_window})
        else:
            self.logger.log_event("Distraction", {"window": active_window})

    def detect_distraction_in_text(self, text):
        """ Uses AI to classify whether text is work-related or a distraction. """
        labels = ["Productive Work", "Distraction (Social Media, Entertainment)"]
        result = self.classifier(text, candidate_labels=labels)
        category = result["labels"][0]
        self.logger.log_event("Text Classification", {"text": text, "category": category})
        return category

    def start_monitoring(self):
        """ Starts background distraction monitoring. """
        self.monitoring = True
        self.thread = Thread(target=self.monitor, daemon=True)
        self.thread.start()

    def stop_monitoring(self):
        """ Stops background monitoring. """
        self.monitoring = False
        self.stop_event.set()
        self.thread.join()

    def monitor(self):
        """ Periodically checks for distractions and logs them. """
        while not self.stop_event.is_set():
            if self.is_inactive():
                self.logger.log_event("Inactivity", {"message": "User inactive for too long!"})

            self.detect_off_task_window()
            time.sleep(self.check_interval)

    def get_distraction_count(self):
        """ Return the number of distractions. """
        return self.distraction_events

    def reset_distractions(self):
        """ Reset the distraction count. """
        count = self.distraction_events
        self.distraction_events = 0
        return count
