"""
GUI package for the Materna CRM application.
"""

from .main_window import MainWindow
from .forms import ClientForm
from .table import ClientTable
from .filters import FilterPanel
from .popups import StatisticsPopup, StyleSelector

__all__ = [
    'MainWindow',
    'ClientForm',
    'ClientTable',
    'FilterPanel',
    'StatisticsPopup',
    'StyleSelector'
]
