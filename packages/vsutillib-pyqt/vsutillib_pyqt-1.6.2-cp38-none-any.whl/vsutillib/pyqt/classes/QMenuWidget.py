"""
subclass of QMenu to save title
used in internationalization
"""

from PySide2.QtWidgets import QMenu

class QMenuWidget(QMenu):
    """Override QMenu __init__ to save title"""

    def __init__(self, title=None, titlePrefix=None, titleSuffix=None):
        super().__init__(title)

        self.originaltitle = title
        self.titlePrefix = "" if titlePrefix is None else titlePrefix
        self.titleSuffix = "" if titleSuffix is None else titleSuffix
