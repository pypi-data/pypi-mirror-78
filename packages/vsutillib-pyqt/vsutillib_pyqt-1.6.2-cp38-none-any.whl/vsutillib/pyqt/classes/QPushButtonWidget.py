"""
subclass of QPushButton to save text, shortcut and tooltip
this information is used for internationalization
"""

from PySide2.QtWidgets import QPushButton


class QPushButtonWidget(QPushButton):
    """
    QPushButton subclass of QAction save original shortcut and tooltip for locale application

    Args:
        shortcut (str, optional): original shortcut string representation. Defaults to None.
        tooltip (str, optional): original tooltip. Defaults to None.
    """

    def __init__(self, *args, function=None, toolTip=None, **kwargs):
        super().__init__(*args, **kwargs)

        for p in args:
            if isinstance(p, str):
                # Save first string found assume is the button label
                self.originalText = p
                break

        self.toolTip = toolTip

        if function is not None:
            self.clicked.connect(function)

        if toolTip is not None:
            self.setToolTip(toolTip)

    def setToolTip(self, toolTip, *args, **kwargs):

        if self.toolTip is None:
            self.toolTip = toolTip

        super().setToolTip(toolTip, *args, **kwargs)
