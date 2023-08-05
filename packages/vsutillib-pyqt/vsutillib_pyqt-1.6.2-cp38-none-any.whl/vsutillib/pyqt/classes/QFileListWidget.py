"""
Sub-class of QTextEdit accepts drag and drop
"""
import logging

from pathlib import Path

from natsort import natsorted, ns

from PySide2.QtCore import Slot, Signal
from PySide2.QtWidgets import QMenu


from .QOutputTextWidget import QOutputTextWidget


MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class QFileListWidget(QOutputTextWidget):
    """
    QTextEdit subclass that accepts dropped files
    displays only the name of the files.
    The full path is save and use internally.
    """

    filesDroppedUpdateSignal = Signal(list)

    def __init__(self, parent):
        super().__init__(parent)

        # self.setDragEnabled(True)
        self.fileList = []
        self.bBlockDrops = False
        self.bFilesDropped = False

    def clear(self):
        self.fileList = []
        self.bBlockDrops = False
        self.bFilesDropped = False
        super().setAcceptDrops(True)
        super().clear()

    def dragEnterEvent(self, event):

        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == "file":
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == "file":
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()

        bUpdate = False
        for f in urls:
            filePath = str(f.path())[1:]

            fPath = Path(filePath)

            if fPath.is_dir():
                files = [x for x in fPath.glob("*.*") if x.is_file()]
                files = natsorted(files, alg=ns.PATH)
                for x in files:
                    if x not in self.fileList:
                        self.fileList.append(x)
                        bUpdate = True
            elif fPath.is_file():
                if fPath not in self.fileList:
                    self.fileList.append(fPath)
                    bUpdate = True

        if bUpdate:
            if not self.bFilesDropped:
                self.bFilesDropped = True

            self._displayFiles()
            self.filesDroppedUpdateSignal.emit(self.fileList)

    def contextMenuEvent(self, event):

        if self.bFilesDropped and self.fileList:
            menu = QMenu(self)
            clearAction = menu.addAction(Actions.Clear)
            sortAction = menu.addAction(Actions.Sort)
            action = menu.exec_(self.mapToGlobal(event.pos()))
            if action == clearAction:
                self.clear()
                self.filesDroppedUpdateSignal.emit(self.fileList)
            elif action == sortAction:
                if self.fileList:
                    self.fileList.sort(key=str)
                    self._displayFiles()
                    self.filesDroppedUpdateSignal.emit(self.fileList)

    def setAcceptDrops(self, value):

        if not self.bBlockDrops:
            # don't check for type to raise error
            super().setAcceptDrops(value)

    @Slot(list)
    def setFileList(self, filesList=None):
        """
        Set the files manually

        Args:
            filesList (list, optional): file list to display. Defaults to None.
        """

        if filesList:
            self.bBlockDrops = True
            self.bFilesDropped = False
            super().setAcceptDrops(False)
            self.fileList = []

            for f in filesList:
                self.fileList.append(f)

            self._displayFiles()

    def _displayFiles(self):
        """display the files on QTextEdit box"""

        super().clear()

        for f in self.fileList:
            self.insertPlainText(f.name + "\n")


class Actions:
    """
    Actions labels for context menu
    """

    Clear = "Clear"
    Sort = "Sort"
