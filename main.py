# main.py

import sys
from PyQt5.QtWidgets import QApplication
from gui.components.main_window import MainWindow
from core.trackers.advanced_distraction import AdvancedDistractionDetector
from core.analytics.focus_report import FocusReport

print("Launching Focus Forge...")

def main():
    app = QApplication(sys.argv)
    distraction_detector = AdvancedDistractionDetector()
    window = MainWindow(distraction_detector)

    # Start Advanced Distraction Monitoring
    distraction_detector.start_monitoring()

    window.show()
    print("Focus Forge UI Loaded!")

    # Ensure the distraction detector stops when the app closes
    app.aboutToQuit.connect(distraction_detector.stop_monitoring)

    # Generate report after the app closes
    def generate_focus_report():
        print("Generating Focus Report...")
        focus_report = FocusReport()
        focus_report.generate_report()
        focus_report.export_csv()

    app.aboutToQuit.connect(generate_focus_report)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
