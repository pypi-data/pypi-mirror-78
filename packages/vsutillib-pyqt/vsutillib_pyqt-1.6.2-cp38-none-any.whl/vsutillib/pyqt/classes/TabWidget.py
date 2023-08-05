"""
Tabs Widget

Central widget holds:

    - ListViewWidget
    - TableViewWidget
    - TreeViewWidget

Todo: Hide and un hide at current position.  Possibly the widget itself do
      the hiding
"""
# TWG0001

import logging

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QTabWidget

# from ..utils import Text

MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class TabWidget(QTabWidget):
    """Main Widget"""

    # Class logging state
    __log = False

    setCurrentIndexSignal = Signal(int)
    setCurrentWidgetSignal = Signal(object)

    def __init__(self, parent=None, tabWidgets=None):
        super().__init__()

        self.parent = parent
        self.__tabWidgets = []

        self.__log = False

        self._initUI(tabWidgets)

        self.setCurrentIndexSignal.connect(super().setCurrentIndex)
        self.setCurrentWidgetSignal.connect(super().setCurrentWidget)

    def _initUI(self, tabWidgets):
        """Setup Widget Layout"""

        if tabWidgets is not None:
            self.__tabWidgets.extend(tabWidgets)

            for tw in tabWidgets:
                tabIndex = self.addTab(tw[0], tw[1])
                self.setTabToolTip(tabIndex, tw[2])

                try:
                    tw[0].tab = tabIndex
                except:  # pylint: disable=bare-except
                    pass

                try:
                    tw[0].title = tw[1]
                except:  # pylint: disable=bare-except
                    pass

                try:
                    tw[0].tabWidget = self
                except:  # pylint: disable=bare-except
                    pass

    @classmethod
    def classLog(cls, setLogging=None):
        """
        get/set logging at class level
        every class instance will log
        unless overwritten

        Args:
            setLogging (bool):
                - True class will log
                - False turn off logging
                - None returns current Value

        Returns:
            bool:
                returns the current value set
        """

        if setLogging is not None:
            if isinstance(setLogging, bool):
                cls.__log = setLogging

        return cls.__log

    @property
    def log(self):
        """
        class property can be used to override the class global
        logging setting

        Returns:
            bool:

            True if logging is enable False otherwise
        """
        if self.__log is not None:
            return self.__log

        return TabWidget.classLog()

    @log.setter
    def log(self, value):
        """set instance log variable"""
        if isinstance(value, bool) or value is None:
            self.__log = value

    def tabInserted(self, index):

        for tabIndex in range(self.count()):
            widget = self.widget(tabIndex)
            widget.tab = tabIndex

    def tabRemoved(self, index):

        for tabIndex in range(self.count()):
            widget = self.widget(tabIndex)
            widget.tab = tabIndex

    def addTabs(self, tabWidgets):
        self._initUI(tabWidgets)

    def setLanguage(self):
        """
        setLanguage set tabs labels according to locale
        """

        for i, (__, label, tooltip) in enumerate(self.__tabWidgets):
            self.setTabText(i, _(label))
            self.setTabToolTip(i, _(tooltip))
