import json
import os
from datetime import datetime
import pandas as pd
import logging
import csv
from pathlib import Path
from ..utils.database import Database

LOG_FILE = "logs/distraction_log.json"
REPORT_FILE = "logs/focus_report.json"

class FocusReport:
    def __init__(self):
        """Initialize by loading distraction logs."""
        os.makedirs("logs", exist_ok=True)
        self.db = Database()
        self.report_data = {
            'sessions': [],
            'distractions': [],
            'tasks': []
        }
        self.logs = self.load_logs()

    def load_logs(self):
        """Loads existing distraction logs from JSON file if available."""
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                return json.load(f)
        return []

    def generate_report(self):
        """Generates a structured focus report based on distraction logs."""
        report = {
            "total_sessions": len(self.logs),
            "start_time": self.logs[0]["timestamp"] if self.logs else "N/A",
            "end_time": self.logs[-1]["timestamp"] if self.logs else "N/A",
            "distraction_summary": self.get_summary(),
            "time_distribution": self.get_time_analysis(),
            "recommendations": self.get_recommendations()
        }

        # Save report to file
        with open(REPORT_FILE, "w") as f:
            json.dump(report, f, indent=4)

        print("✅ Focus Report Generated!")
        return report

    def get_summary(self):
        """Summarizes distraction logs by category."""
        summary = {"total_distractions": 0, "work_sessions": 0, "by_type": {}}
        for log in self.logs:
            event_type = log["event_type"]
            if event_type == "Work App Usage":
                summary["work_sessions"] += 1
            else:
                summary["total_distractions"] += 1
                summary["by_type"][event_type] = summary["by_type"].get(event_type, 0) + 1
        return summary

    def get_time_analysis(self):
        """Analyzes time spent in work vs. distractions."""
        time_data = {"work_apps": {}, "distractions": {}}
        for log in self.logs:
            if log["event_type"] == "App Switch":
                details = log.get("details", {})
                app_name = details.get("new_window")
                duration = details.get("duration_in_previous_window", 0)

                if app_name is None:
                    logging.warning("Missing 'new_window' in log details.")
                    continue

                if any(work_app in app_name for work_app in ["ChatGPT", "Cursor", "VS Code"]):
                    time_data["work_apps"][app_name] = time_data["work_apps"].get(app_name, 0) + duration
                else:
                    time_data["distractions"][app_name] = time_data["distractions"].get(app_name, 0) + duration
        return time_data

    def get_recommendations(self):
        """AI-driven suggestions based on focus trends."""
        summary = self.get_summary()
        total_distractions = summary["total_distractions"]
        recommendations = []

        if total_distractions > 10:
            recommendations.append("🚀 Reduce distractions by using Focus Mode or a Pomodoro timer.")
        if summary["by_type"].get("Inactivity", 0) > 5:
            recommendations.append("⚡ Consider shorter work sessions with breaks to maintain engagement.")
        if summary["by_type"].get("App Switch", 0) > 8:
            recommendations.append("📌 Try limiting non-work-related app usage.")

        return recommendations

    def export_csv(self):
        """Exports log data to a CSV file for further analysis."""
        df = pd.DataFrame(self.logs)
        csv_file = "logs/focus_report.csv"
        df.to_csv(csv_file, index=False)
        print(f"✅ Report exported to {csv_file}")

# Example Usage:
if __name__ == "__main__":
    report = FocusReport()
    report.generate_report()
    report.export_csv()
