"""
DualProgressBar if for graphical representation of the inner (unit) and outer (total)
loop work

Dual progress bar intended use is horizontal position vertical layout possible

align:
    Qt.Horizontal - Horizontal layout the default
    Qt.Vertical - Vertical layout

TaskBarButtonProgress show progress bar on taskbar icon

"""

import platform

from PySide2.QtCore import Qt, Signal, Slot
from PySide2.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QProgressBar,
    QSizePolicy,
)

if platform.system() == "Windows":
    from PySide2.QtWinExtras import QWinTaskbarButton, QtWin
    myAppID = "VergaraSoft.MKVBatchMultiplex.mkv.2.0.0"  # arbitrary string
    QtWin.setCurrentProcessExplicitAppUserModelID(myAppID)

class DualProgressBar(QWidget):
    """
    Dual QProgressBar for unit and total progress

    param align - Set alignment Qt.Horizontal or Qt.Vertical
    type align - Qt.AlignmentFlags
    """

    valuesChangedSignal = Signal(int, int)

    def __init__(self, parent, align=Qt.Horizontal):
        super().__init__(parent)

        self.parent = parent
        self.taskbarButton = TaskbarButtonProgress(parent)
        self._lbl = QLabel()
        self._intControls()
        self._initLayout(align)

        # Default usage is to use widget in toolbar fix size
        # at extreme right
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def _intControls(self):

        self.pbBarUnit = QProgressBar()
        self.pbBarUnit.setRange(0, 100)
        self.pbBarUnit.setValue(0)
        self.pbBarUnit.resize(self.pbBarUnit.sizeHint())

        self.pbBarTotal = QProgressBar()
        self.pbBarTotal.setRange(0, 100)
        self.pbBarTotal.setValue(0)
        self.pbBarTotal.resize(self.pbBarTotal.sizeHint())

        # Horizontal with horizontal elements
        self.hboxLayout = QHBoxLayout()
        # Horizontal with vertical elements
        self.vboxLayout = QHBoxLayout()

    def _hLayout(self):
        """Set horizontal layout"""

        self._lbl.setText("Progress:")

        self.pbBarUnit.setOrientation(Qt.Horizontal)
        self.pbBarTotal.setOrientation(Qt.Horizontal)

        # Assign widgets to horizontal layout
        self.hboxLayout.addWidget(self._lbl)
        self.hboxLayout.addWidget(self.pbBarUnit)
        self.hboxLayout.addWidget(self.pbBarTotal)

    def _vLayout(self):
        """Set a vertical layout"""
        self.pbBarUnit.setOrientation(Qt.Vertical)
        self.pbBarTotal.setOrientation(Qt.Vertical)

        widg1 = _VerticalBarSetup(self.pbBarUnit, "U")
        widg2 = _VerticalBarSetup(self.pbBarTotal, "T")

        self.vboxLayout.addWidget(widg1)
        self.vboxLayout.addWidget(widg2)

    def _initLayout(self, align):
        """Set layout to use"""
        if align == Qt.Vertical:
            self._vLayout()
            self.setLayout(self.vboxLayout)
        else:
            self._hLayout()
            self.setLayout(self.hboxLayout)

    @property
    def label(self):
        return self._lbl

    @label.setter
    def label(self, value):
        if isinstance(value, str):
            self._lbl.setText(value)

    @Slot(int)
    def setAlignment(self, align):
        """
        Set Alignment

        : param align: Set alignment Qt.Horizontal or Qt.Vertical
        : type align: Qt.AlignmentFlags
        """

        if align == Qt.Horizontal:
            QWidget().setLayout(self.layout())
            self._intControls()
            self._hLayout()
            self.setLayout(self.hboxLayout)

        if align == Qt.Vertical:
            QWidget().setLayout(self.layout())
            self._intControls()
            self._vLayout()
            self.setLayout(self.vboxLayout)

    @Slot(int, int)
    def setMaximum(self, maxUnit=100, maxTotal=100):
        """
        Set maximum values

        : param maxUnit: maximum value for inner loop
        : type maxUnit: int
        : param maxTotal: maximum value for outer loop
        : type maxTotal: int
        """
        self.pbBarUnit.setMaximum(maxUnit)
        self.pbBarTotal.setMaximum(maxTotal)
        if self.taskbarButton:
            self.taskbarButton.progress.setMaximum(maxTotal)

    @Slot(int, int)
    def setMinimum(self, minUnit=0, minTotal=0):
        """
        Set minimum values

        : param minUnit: minimum value for inner loop
        : type minUnit: int
        : param minTotal: minimum value for outer loop
        : type minTotal: int
        """

        self.pbBarUnit.setMinimum(minUnit)
        self.pbBarTotal.setMinimum(minTotal)
        if self.taskbarButton:
            self.taskbarButton.progress.setMinimum(minTotal)

    @Slot(int, int, int, int)
    def setRange(self, minUnit=0, maxUnit=100, minTotal=0, maxTotal=100):
        """
        Set minimum and maximum as a range


        : param minUnit: minimum value for inner loop
        : type minUnit: int
        : param maxUnit: maximum value for inner loop
        : type maxUnit: int
        : param minTotal: minimum value for outer loop
        : type minTotal: int
        : param maxTotal: maximum value for outer loop
        : type maxTotal: int
        """
        self.pbBarUnit.setRange(minUnit, maxUnit)
        self.pbBarTotal.setRange(minTotal, maxTotal)
        if self.taskbarButton:
            self.taskbarButton.progress.setRange(minTotal, maxTotal)

    @Slot(int, int)
    def setValues(self, unit, total):
        """
        Update values of progressbars

        :param unit: value for inner loop
        :type unit: int
        :param total: value for outer loop
        :type total: int
        """

        self.pbBarUnit.setValue(unit)
        self.pbBarTotal.setValue(total)
        if self.taskbarButton:
            self.taskbarButton.progress.setValue(total)

        self.valuesChangedSignal.emit(unit, total)

    @Slot()
    def reset(self):
        if self.taskbarButton:
            self.taskbarButton.progress.reset()

    @Slot()
    def initTaskbarButton(self):

        if platform.system() == "Windows":
            self.taskbarButton.initTaskbarButton()

    def setSizePolicy(self, horizontal, vertical):
        """
        Argument of QSizePolicy.Policy form Qt Documentation

        QSizePolicy.Fixed              0           The QWidget.sizeHint() is the only
                                                   acceptable alternative, so the widget can
                                                   never grow or shrink (e.g. the vertical
                                                   direction of a push button).

        QSizePolicy.Minimum            GrowFlag    The sizeHint() is minimal, and sufficient.
                                                   The widget can be expanded, but there is no
                                                   advantage to it being larger (e.g. the
                                                   horizontal direction of a push button). It
                                                   cannot be smaller than the size provided by
                                                   sizeHint().

        QSizePolicy.Maximum            ShrinkFlag  The sizeHint() is a maximum. The widget can
                                                   be shrunk any amount without detriment if
                                                   other widgets need the space (e.g. a separator
                                                   line). It cannot be larger than the size
                                                   provided by sizeHint().

        QSizePolicy.Preferred          GrowFlag |ShrinkFlag
                                                   The sizeHint() is best, but the widget can be
                                                   shrunk and still be useful. The widget can be
                                                   expanded, but there is no advantage to it
                                                   being larger than sizeHint() (the default
                                                   QWidget policy).

        QSizePolicy.Expanding          GrowFlag | ShrinkFlag | ExpandFlag
                                                   The sizeHint() is a sensible size, but the widget
                                                   can be shrunk and still be useful. The widget can
                                                   make use of extra space, so it should get as much
                                                   space as possible (e.g. the horizontal direction
                                                   of a horizontal slider).
        QSizePolicy.MinimumExpanding   GrowFlag | ExpandFlag
                                                   The sizeHint() is minimal, and sufficient. The
                                                   widget can make use of extra space, so it should
                                                   get as much pace as possible (e.g. the horizontal
                                                   direction of a horizontal slider).
        QSizePolicy.Ignored            ShrinkFlag | GrowFlag | IgnoreFlag
                                                   The sizeHint() is ignored. The widget will get as
                                                   much space as possible.

        Method override is for documentation and use same name as parent also 'pass' did not
        worked as expected

        :param horizontal: horizontal size policy
        :type horizontal: QSizePolicy.Policy
        :param vertical: vertical size policy
        :type vertical: QSizePolicy.Policy
        """

        QWidget.setSizePolicy(self, horizontal, vertical)


if platform.system() == "Windows":

    class TaskbarButtonProgress(QWinTaskbarButton):
        """
        TaskbarProgress taskbar icon progress indicator
        """

        def __init__(self, parent):
            super().__init__(parent)

            self.platform = platform.system()
            self.parent = parent
            self.button = None
            self.progress = None

            if self.platform == "Windows":
                self.button = QWinTaskbarButton(parent)

        def __bool__(self):
            if (self.button is None) or (self.progress is None):
                return False
            return True

        def initTaskbarButton(self):
            """
            initTaskbarButton for late init QWinTaskbarButton
            """

            if self.platform == "Windows":
                self.button.setWindow(self.parent.windowHandle())
                self.progress = self.button.progress()
                self.progress.setRange(0, 100)
                self.progress.setVisible(True)

        @Slot(int, int)
        def setValue(self, init, total):

            self.progress.setValue(total)


else:

    def TaskbarButtonProgress(parent):
        return False


def _VerticalBarSetup(pbBar, label):
    """Vertical progress bar widget"""

    vbox = QVBoxLayout()
    widget = QWidget()

    lbl = QLabel(label)
    lbl.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    vbox.addWidget(pbBar)
    vbox.addWidget(lbl)

    widget.setLayout(vbox)

    return widget


class SpacerWidget(QWidget):
    """
    Utility widget to maintain widgets at same extreme during resizing
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)


if __name__ == "__main__":

    import sys
    from PySide2.QtWidgets import QApplication, QGridLayout, QMainWindow, QPushButton

    class MainWindow(QMainWindow):
        """Test the progress bars"""

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            l = QGridLayout()

            self.pb = DualProgressBar(self)

            b = QPushButton("Test")
            b.pressed.connect(self.test)
            h = QPushButton("Vertical")
            h.pressed.connect(self.vertical)
            v = QPushButton("Horizontal")
            v.pressed.connect(self.horizontal)
            l.addWidget(self.pb, 0, 0)
            l.addWidget(b, 1, 0)
            l.addWidget(h, 2, 0)
            l.addWidget(v, 3, 0)

            w = QWidget()
            w.setLayout(l)

            self.setCentralWidget(w)

            self.show()

            # this has to be defined after
            self.pb.initTaskbarButton()

        def horizontal(self):
            """Horizontal progress bar"""
            self.pb.setAlignment(Qt.Horizontal)

        def vertical(self):
            """Vertical progress bar"""
            self.pb.setAlignment(Qt.Vertical)

        def test(self):
            """Test"""
            i = 0
            j = 0
            t = 0

            self.pb.setMinimum(minTotal=0)
            self.pb.setMaximum(maxTotal=500)

            while j < 5:
                while i < 100:
                    i += 0.001
                    self.pb.setValues(i, t + i)

                t += 100
                j += 1
                i = 0

    # pylint: disable=C0103
    # variables use to construct application not constants
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
