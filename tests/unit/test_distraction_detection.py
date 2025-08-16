#!/usr/bin/env python3
"""
Test suite for distraction detection system
"""

import pytest
import unittest.mock as mock
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core.trackers.advanced_distraction import AdvancedDistractionDetector
from core.trackers.activity_monitor import ActivityMonitor
from core.trackers.distraction_logger import DistractionLogger

class TestAdvancedDistractionDetector:
    """Test AdvancedDistractionDetector class functionality"""
    
    def test_initialization(self):
        """Test detector can be initialized without errors"""
        detector = AdvancedDistractionDetector()
        assert detector is not None
        assert hasattr(detector, 'start_monitoring')
        assert hasattr(detector, 'stop_monitoring')
    
    def test_start_monitoring(self):
        """Test monitoring can be started"""
        detector = AdvancedDistractionDetector()
        
        # Mock the monitoring thread
        with patch.object(detector, '_start_monitoring_thread'):
            detector.start_monitoring()
            assert detector.is_monitoring == True
    
    def test_stop_monitoring(self):
        """Test monitoring can be stopped"""
        detector = AdvancedDistractionDetector()
        detector.is_monitoring = True
        
        detector.stop_monitoring()
        assert detector.is_monitoring == False
    
    def test_distraction_detection(self):
        """Test distraction detection logic"""
        detector = AdvancedDistractionDetector()
        
        # Mock window focus events
        mock_event = Mock()
        mock_event.window_title = "Facebook"
        mock_event.process_name = "chrome.exe"
        
        # Test that social media is detected as distraction
        is_distraction = detector._is_distraction(mock_event)
        assert is_distraction == True
    
    def test_non_distraction_detection(self):
        """Test that productive apps are not flagged as distractions"""
        detector = AdvancedDistractionDetector()
        
        # Mock productive app event
        mock_event = Mock()
        mock_event.window_title = "Visual Studio Code"
        mock_event.process_name = "code.exe"
        
        # Test that productive apps are not distractions
        is_distraction = detector._is_distraction(mock_event)
        assert is_distraction == False

class TestActivityMonitor:
    """Test ActivityMonitor class functionality"""
    
    def test_initialization(self):
        """Test activity monitor can be initialized"""
        monitor = ActivityMonitor()
        assert monitor is not None
        assert hasattr(monitor, 'track_activity')
    
    def test_activity_tracking(self):
        """Test activity tracking functionality"""
        monitor = ActivityMonitor()
        
        # Mock activity data
        activity_data = {
            'timestamp': '2025-08-15 19:30:00',
            'window_title': 'Test App',
            'process_name': 'test.exe',
            'duration': 300
        }
        
        # Test tracking
        result = monitor.track_activity(activity_data)
        assert result is not None
    
    def test_idle_detection(self):
        """Test idle time detection"""
        monitor = ActivityMonitor()
        
        # Mock idle time
        with patch('pywinauto.Desktop') as mock_desktop:
            mock_desktop.return_value = Mock()
            
            idle_time = monitor.get_idle_time()
            assert isinstance(idle_time, (int, float))
            assert idle_time >= 0

class TestDistractionLogger:
    """Test DistractionLogger class functionality"""
    
    def test_initialization(self):
        """Test logger can be initialized"""
        logger = DistractionLogger()
        assert logger is not None
        assert hasattr(logger, 'log_distraction')
    
    def test_distraction_logging(self):
        """Test distraction logging functionality"""
        logger = DistractionLogger()
        
        # Mock distraction event
        distraction_event = {
            'timestamp': '2025-08-15 19:30:00',
            'window_title': 'Facebook',
            'process_name': 'chrome.exe',
            'duration': 180,
            'category': 'social_media'
        }
        
        # Test logging
        result = logger.log_distraction(distraction_event)
        assert result is not None
    
    def test_log_retrieval(self):
        """Test log retrieval functionality"""
        logger = DistractionLogger()
        
        # Mock database query
        with patch('sqlite3.connect') as mock_connect:
            mock_cursor = Mock()
            mock_cursor.fetchall.return_value = [
                ('2025-08-15 19:30:00', 'Facebook', 'chrome.exe', 180, 'social_media')
            ]
            mock_connect.return_value.cursor.return_value = mock_cursor
            
            logs = logger.get_distraction_logs()
            assert isinstance(logs, list)
            assert len(logs) > 0

class TestIntegration:
    """Integration tests for the distraction detection system"""
    
    def test_full_workflow(self):
        """Test complete distraction detection workflow"""
        detector = AdvancedDistractionDetector()
        monitor = ActivityMonitor()
        logger = DistractionLogger()
        
        # Mock the entire workflow
        with patch.object(detector, '_start_monitoring_thread'), \
             patch.object(monitor, 'track_activity'), \
             patch.object(logger, 'log_distraction'):
            
            # Start monitoring
            detector.start_monitoring()
            assert detector.is_monitoring == True
            
            # Simulate distraction detection
            mock_distraction = Mock()
            mock_distraction.window_title = "YouTube"
            mock_distraction.process_name = "chrome.exe"
            
            # Check if detected as distraction
            is_distraction = detector._is_distraction(mock_distraction)
            assert is_distraction == True
            
            # Stop monitoring
            detector.stop_monitoring()
            assert detector.is_monitoring == False
    
    def test_database_integration(self):
        """Test database integration for logging"""
        logger = DistractionLogger()
        
        # Mock database operations
        with patch('sqlite3.connect') as mock_connect:
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            
            # Test logging to database
            distraction_event = {
                'timestamp': '2025-08-15 19:30:00',
                'window_title': 'Instagram',
                'process_name': 'chrome.exe',
                'duration': 120,
                'category': 'social_media'
            }
            
            result = logger.log_distraction(distraction_event)
            assert result is not None
            
            # Verify database operations were called
            mock_cursor.execute.assert_called()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
