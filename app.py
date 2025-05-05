import sys
from PySide6.QtCore import QObject, Slot, Signal, Property, QThread
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from justjoinit_bot import search_jobs, apply_to_job, setup_driver, create_csv, driver_setup_search
import time

# Create a thread to run the Bot because selenium block the main thread
class BotThread(QThread):
    finished = Signal()
    error = Signal(str)
    messageChanged = Signal(str)
    hasJobsChanged = Signal(bool)
    
    def __init__(self, location, position):
        super().__init__()
        self.location = location
        self.position = position
        
    def run(self):
        try:
            self.messageChanged.emit("Setup the bot...")
            driver = setup_driver()
            
            if driver:
                self.messageChanged.emit("Search configuration...")
                driver = driver_setup_search(driver, self.location, self.position)
                
                if driver:
                    print("Driver setup search completed")
                    has_jobs = False
                    self.messageChanged.emit("Search jobs...")
                    for i, (job_url, job) in enumerate(search_jobs(driver), 1):
                        has_jobs=True
                        print(f"Job {i}: {job_url} - {job.text[:50]}")
                        if job_url:
                            self.messageChanged.emit(f"Apply to: {job.text[:50]}...")
                            time.sleep(1)
                            is_applied = apply_to_job(driver, job_url, job)
                            self.messageChanged.emit(f"[{i}] Save...")
                            create_csv(is_applied, job, job_url)
                    
                    self.messageChanged.emit("Search completed.")
                    if has_jobs:
                        self.hasJobsChanged.emit(True)
            else:
                self.messageChanged.emit("Error during driver setup")
                
        except Exception as e:
            self.error.emit(f"Probleme : {str(e)}")
        finally:
            self.finished.emit()

 
class Backend(QObject):
    loadedChanged = Signal(bool)
    loadingMessageChanged = Signal(str)
    hasJobsChanged = Signal(bool)
    
    def __init__(self):
        super().__init__()
        self._location = ""
        self._position = ""
        self._loaded = False
        self._has_jobs = False
        self._loading_message = "Setup the bot..."
        self.worker = None

    @Property(str, notify=loadingMessageChanged)
    def loadingMessage(self):
        return self._loading_message

    @loadingMessage.setter
    def loadingMessage(self, value):
        if self._loading_message != value:
            self._loading_message = value
            self.loadingMessageChanged.emit(self._loading_message)

    @Property(bool, notify=loadedChanged)
    def loaded(self):
        return self._loaded

    @loaded.setter
    def loaded(self, value):
        if self._loaded != value:
            self._loaded = value
            self.loadedChanged.emit(self._loaded)

    @Slot(str, str)
    def set_config(self, location, position):
        self._location = location   
        self._position = position
        self.loaded = False
        self.bot_thread = BotThread(location, position)
        self.bot_thread.hasJobsChanged.connect(lambda has_jobs: setattr(self, 'hasJobs', has_jobs))
        self.bot_thread.messageChanged.connect(lambda msg: setattr(self, 'loadingMessage', msg))
        self.bot_thread.error.connect(lambda msg: setattr(self, 'loadingMessage', msg))
        self.bot_thread.finished.connect(lambda: setattr(self, 'loaded', True))
        self.bot_thread.start()

# Initialisation de l'app
app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
backend = Backend()
engine.rootContext().setContextProperty("backend", backend)
engine.load('app.qml')
engine.quit.connect(app.quit)
sys.exit(app.exec())
