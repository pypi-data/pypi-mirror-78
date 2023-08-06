"""
This file contains custom errors used by BESOS
"""


class ModeError(ValueError):
    """An error for when an invalid mode is encountered."""

    def __init__(self, mode=None, message=None):
        if message is None:
            message = f'Invalid mode {mode}. Expected "idf" or "json"'
        super().__init__(message)
