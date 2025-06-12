import json
import os
import time
from datetime import datetime

LOG_FILE = "logs/distraction_log.json"

class DistractionLogger:
    def __init__(self):
        """Initialize log storage and ensure log directory exists."""
        os.makedirs("logs", exist_ok=True)
        self.logs = self.load_logs()

    def load_logs(self):
        """Load existing logs from JSON file if available."""
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                return json.load(f)
        return []

    def log_event(self, event_type, details):
        """
        Logs a distraction event with a timestamp.
        
        Args:
            event_type (str): Type of event (e.g., "Inactivity", "App Switch", "Distraction").
            details (dict): Additional info about the event.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "event_type": event_type,
            "details": details
        }
        self.logs.append(log_entry)

        # Save to JSON file
        with open(LOG_FILE, "w") as f:
            json.dump(self.logs, f, indent=4)

    def get_logs(self):
        """Retrieve all logs."""
        return self.logs

    def get_summary(self):
        """Summarizes logged distractions by category."""
        summary = {
            "total_distractions": len(self.logs),
            "by_type": {}
        }
        for log in self.logs:
            event_type = log["event_type"]
            summary["by_type"][event_type] = summary["by_type"].get(event_type, 0) + 1
        return summary
