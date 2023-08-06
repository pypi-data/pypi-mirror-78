"""
This module contains functions to help evaluate and compare feyn graphs and other models.
"""

from ._metrics import accuracy_score, r2_score, rmse, confusion_matrix, segmented_loss

__all__ = [
    'accuracy_score',
    'r2_score',
    'rmse',
    'confusion_matrix',
    'segmented_loss',
]

