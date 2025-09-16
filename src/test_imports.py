#!/usr/bin/env python3
"""
Test script to check if all imports work correctly.
"""

try:
    from config import EXCEL_FILE, columns
    print("✓ Config import successful")
except ImportError as e:
    print(f"✗ Config import failed: {e}")

try:
    from models.client import Client, Statistics
    print("✓ Models import successful")
except ImportError as e:
    print(f"✗ Models import failed: {e}")

try:
    from utils.excel_manager import ExcelManager
    print("✓ Utils import successful")
except ImportError as e:
    print(f"✗ Utils import failed: {e}")

try:
    from gui.main_window import MainWindow
    print("✓ Main window import successful")
except ImportError as e:
    print(f"✗ Main window import failed: {e}")

try:
    from gui.forms import ClientForm
    print("✓ Forms import successful")
except ImportError as e:
    print(f"✗ Forms import failed: {e}")

try:
    from gui.table import ClientTable
    print("✓ Table import successful")
except ImportError as e:
    print(f"✗ Table import failed: {e}")

try:
    from gui.filters import FilterPanel
    print("✓ Filters import successful")
except ImportError as e:
    print(f"✗ Filters import failed: {e}")

try:
    from gui.popups import StatisticsPopup, StyleSelector
    print("✓ Popups import successful")
except ImportError as e:
    print(f"✗ Popups import failed: {e}")

print("Import test completed.")
