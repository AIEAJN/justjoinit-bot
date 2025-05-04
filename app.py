# You don't need comment when code is self explanatory
import sys
from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from justjoinit_bot import search_jobs, apply_to_job


class Backend(QObject):
    def __init__(self):
        super().__init__()
        self._location = ""
        self._position = ""

    @Slot(str, str)
    def set_config(self, location, position):
        self._location = location   
        self._position = position
        search_jobs(self._location, self._position)
        
app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
backend = Backend()
engine.rootContext().setContextProperty("backend", backend)
engine.load('app.qml')
sys.exit(app.exec())