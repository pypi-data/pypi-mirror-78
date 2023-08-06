import sys

from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication

from . import util
from .views import RSSHTControllerWindow


def main(argv=None):
    argv = sys.argv if argv is None else argv
    try:
        util.load_config()
    except IOError:
        pass
    app = QApplication(argv)
    window = RSSHTControllerWindow()
    window.show()
    QTimer.singleShot(0, lambda: window.startUpdater())
    status = app.exec_()
    return status
