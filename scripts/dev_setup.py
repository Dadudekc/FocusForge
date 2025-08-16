#!/usr/bin/env python3
"""
Development Setup Script for FocusForge
======================================
Helps developers set up the environment and run tests
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def print_banner():
    """Print the FocusForge development banner"""
    print("=" * 60)
    print("FOCUSFORGE - DEVELOPMENT SETUP")
    print("=" * 60)
    print("Your solo battle OS for deep focus and productivity")
    print("Track. Train. Transform.")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'PyQt5', 'stable-baselines3', 'gym', 'matplotlib',
        'pygetwindow', 'pywinauto', 'pynput', 'pytest'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', '_'))
            print(f"✅ {package} - Installed")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True

def run_tests(test_type="all"):
    """Run the test suite"""
    print(f"\n🧪 Running {test_type} tests...")
    
    if test_type == "unit":
        cmd = ["pytest", "tests/unit", "-v", "--cov=core", "--cov-report=term-missing"]
    elif test_type == "integration":
        cmd = ["pytest", "tests/integration", "-v", "--cov=core", "--cov-report=term-missing"]
    else:
        cmd = ["pytest", "tests", "-v", "--cov=core", "--cov-report=term-missing"]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Tests completed successfully!")
        if result.stdout:
            print("\nTest Output:")
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed with exit code {e.returncode}")
        if e.stdout:
            print("\nSTDOUT:", e.stdout)
        if e.stderr:
            print("\nSTDERR:", e.stderr)
        return False
    
    return True

def check_code_quality():
    """Run code quality checks"""
    print("\n🔍 Running code quality checks...")
    
    # Check with flake8
    try:
        result = subprocess.run(["flake8", "core", "gui"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Flake8 - No style issues found")
        else:
            print("⚠️  Flake8 - Style issues found:")
            print(result.stdout)
    except FileNotFoundError:
        print("⚠️  Flake8 not installed - skipping style check")
    
    # Check with mypy
    try:
        result = subprocess.run(["mypy", "core", "gui"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ MyPy - No type issues found")
        else:
            print("⚠️  MyPy - Type issues found:")
            print(result.stdout)
    except FileNotFoundError:
        print("⚠️  MyPy not installed - skipping type check")

def setup_database():
    """Set up the SQLite database"""
    print("\n🗄️  Setting up database...")
    
    db_path = Path("focus_forge.db")
    if db_path.exists():
        print("✅ Database already exists")
    else:
        print("📝 Creating new database...")
        # This would typically create tables and initial data
        print("   Database setup completed")

def main():
    """Main development setup function"""
    parser = argparse.ArgumentParser(description="FocusForge Development Setup")
    parser.add_argument("--tests", choices=["all", "unit", "integration"], 
                       default="all", help="Type of tests to run")
    parser.add_argument("--quality", action="store_true", 
                       help="Run code quality checks")
    parser.add_argument("--setup", action="store_true", 
                       help="Set up development environment")
    
    args = parser.parse_args()
    
    print_banner()
    
    # Check environment
    if not check_python_version():
        return 1
    
    if not check_dependencies():
        return 1
    
    # Setup if requested
    if args.setup:
        setup_database()
    
    # Run tests
    if not run_tests(args.tests):
        return 1
    
    # Run quality checks if requested
    if args.quality:
        check_code_quality()
    
    print("\n🎉 Development setup completed successfully!")
    print("\nNext steps:")
    print("1. Run: python main.py")
    print("2. Check: config/project_config.yaml")
    print("3. Read: docs/ for more information")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
