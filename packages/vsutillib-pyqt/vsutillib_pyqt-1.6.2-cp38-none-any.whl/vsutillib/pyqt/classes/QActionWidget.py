"""
subclass of QAction to save text, shortcut and tooltip
this information is used for internationalization
"""

from PySide2.QtWidgets import QAction


class QActionWidget(QAction):
    """
    QActionWidget subclass of QAction save original shortcut and tooltip for locale application

    Args:
        shortcut (str, optional): original shortcut string representation. Defaults to None.
        tooltip (str, optional): original tooltip. Defaults to None.
    """

    #def __init__(self, *args, shortcut=None, tooltip=None, textPrefix=None, textSuffix=None, **kwargs):
    def __init__(self, *args, **kwargs):

        textPrefix = kwargs.pop("textPrefix", None)
        textSuffix = kwargs.pop("textSuffix", None)
        shortcut = kwargs.pop("shortcut", None)
        tooltip = kwargs.pop("tooltip", None)

        super().__init__(*args, **kwargs)

        for p in args:
            if isinstance(p, str):
                self.originaltext = p

        self.shortcut = shortcut
        self.tooltip = tooltip
        self.textPrefix = ""
        self.textSuffix = ""

        if shortcut is not None:
            self.setShortcut(shortcut)

        if tooltip is not None:
            self.setToolTip(tooltip)

        if textPrefix is not None:
            self.textPrefix = textPrefix

        if textSuffix is not None:
            self.textSuffix = textSuffix

    def setShortcut(self, shortcut, *args, **kwargs):

        if self.shortcut is None:
            self.shortcut = shortcut

        super().setShortcut(shortcut, *args, **kwargs)

    def setToolTip(self, tooltip, *args, **kwargs):

        if self.tooltip is None:
            self.tooltip = tooltip

        super().setToolTip(tooltip, *args, **kwargs)
