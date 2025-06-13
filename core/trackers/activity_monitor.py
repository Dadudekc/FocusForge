# activity_monitor.py

from pynput import keyboard, mouse
import time
from threading import Thread, Event

class ActivityMonitor:
    def __init__(self, inactivity_threshold=300):  # 5 minutes
        self.inactivity_threshold = inactivity_threshold
        self.last_activity = time.time()
        self.distraction_events = 0
        self.monitoring = False
        self.stop_event = Event()

    def start_monitoring(self):
        self.monitoring = True
        self.keyboard_listener = keyboard.Listener(on_press=self.on_activity)
        self.mouse_listener = mouse.Listener(on_move=self.on_activity, on_click=self.on_activity, on_scroll=self.on_activity)
        self.keyboard_listener.start()
        self.mouse_listener.start()
        self.thread = Thread(target=self.monitor, daemon=True)
        self.thread.start()

    def stop_monitoring(self):
        self.monitoring = False
        self.stop_event.set()
        self.keyboard_listener.stop()
        self.mouse_listener.stop()
        self.thread.join()

    def on_activity(self, *args):
        self.last_activity = time.time()

    def monitor(self):
        while not self.stop_event.is_set():
            current_time = time.time()
            if current_time - self.last_activity > self.inactivity_threshold:
                self.distraction_events += 1
                print("Inactivity detected as distraction!")
                self.last_activity = current_time  # Reset to prevent multiple counts
            time.sleep(1)

    def get_distractions(self):
        return self.distraction_events

    def reset_distractions(self):
        count = self.distraction_events
        self.distraction_events = 0
        return count
