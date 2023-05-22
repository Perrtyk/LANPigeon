import sys
import traceback

from PyQt6.QtWidgets import QApplication, QWidget, QMenuBar, QMenu, QMainWindow, QStatusBar, QToolBar
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt, QSize, QRunnable, QThreadPool, pyqtSlot, pyqtSignal, QObject
from ui_config import *
import lanpigeon_lite as lpl
import gui_widgets as widgets
import ui_config
import os
import platform
import time

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

class WorkerThread(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(WorkerThread, self).__init__()
        # Storing constructor arguments (re-use for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        # self.kwargs['progress_callback'] = self.signals.progress --- callback causes thread to crash.

    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit('Done')
            # self.signals.result.emit(result)  # Return the result of the processing [TESTING]
        finally:
            self.signals.finished.emit()  # Done


class ChildWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("bit_icon.ico"))
        self.setWindowTitle("LAN Pigeon")
        self.current_dir = os.getcwd()

        # Resets working directory for compatibility issues
        print("Current working directory:", self.current_dir)
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        print("New working directory:", os.getcwd())
        ui_config.C_Window_UI(self)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.current_dir = os.getcwd()
        # Resets working directory for compatibility issues
        print("Current working directory:", self.current_dir)
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        print("New working directory:", os.getcwd())
        ui_config.C_Window_UI(self)

        # Set up the main window
        self.setWindowTitle("LAN Pigeon")
        self.setWindowIcon(QIcon("bit_icon.ico"))
        self.setGeometry(100, 100, 500, 600)
        self.setMaximumSize(900, 1100)

        # Create the toolbar
        toolbar = self.create_tool_bar()
        self.addToolBar(toolbar)

        # Set up the status bar
        self.setStatusBar(QStatusBar(self))

        # Create the menu bar
        menu_bar = self.create_menu_bar()

        # Set the menu bar
        self.setMenuBar(menu_bar)

        # Create the central widget
        child_window = ChildWindow()
        self.setCentralWidget(child_window)

    def thread_complete(self):
        print("THREAD COMPLETE!\n")

    def run_lanpigeon_lite_thread(self):
        thread = WorkerThread(lpl.scan_app)
        self.threadpool.start(thread)

        thread.signals.finished.connect(self.thread_complete)

    def run_scan_thread(self):
        thread = WorkerThread(self.click_run_scan)
        self.threadpool.start(thread)

        thread.signals.finished.connect(self.thread_complete)

    def run_stop_thread(self):
        thread = WorkerThread(self.click_stop_scan)
        self.threadpool.start(thread)

        thread.signals.finished.connect(self.thread_complete)

    def click_run_scan(self):
        print('Clicked Run Scan Button!')
        print('Sleep for 5 Seconds, expect responsive GUI.')
        time.sleep(5)
        print('Sleep Complete.')

    def click_stop_scan(self):
        print('Clicked Stop Scan!')
        print('Sleep for 5 Seconds, expect responsive GUI.')
        time.sleep(5)
        print('Sleep Complete.')

    def create_menu_bar(self):
        # Create the menu bar and add menu items
        menu_bar = QMenuBar()
        file_menu = QMenu("&File", self)
        about_menu = QMenu("&About", self)
        help_menu = QMenu("&Help", self)
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(about_menu)
        menu_bar.addMenu(help_menu)

        # Create actions for the file menu
        open_action = QAction("&Open", self)
        save_action = QAction("&Save", self)
        exit_action = QAction("&Exit", self)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Create actions for the about menu
        about_action = QAction("&About", self)
        about_menu.addAction(about_action)

        # Create actions for the help menu
        help_action = QAction("&Help", self)
        help_menu.addAction(help_action)

        return menu_bar

    def create_tool_bar(self):
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(35, 35))
        icon_size = QSize(32, 32)  # desired icon size
        self.addToolBar(toolbar)

        start_scan_action = QAction(QIcon("icons/icon_start.png"), "&Start Scan", self)
        start_scan_action.setStatusTip("Start Scanning IP Range.")
        start_scan_action.triggered.connect(self.run_scan_thread)
        toolbar.addAction(start_scan_action)

        toolbar.addSeparator()

        stop_scan_action = QAction(QIcon("icons/icon_stop.png"), "&Stop Scan", self)
        stop_scan_action.setStatusTip("Stop Scanning IP Range.")
        stop_scan_action.triggered.connect(self.run_stop_thread)
        toolbar.addAction(stop_scan_action)

        toolbar.addSeparator()

        icon_save = QPixmap("icons/icon_save.png").scaled(icon_size)
        save_action = QAction(QIcon(icon_save), "Save Results", self)
        save_action.setStatusTip("Save Scan Results.")
        toolbar.addAction(save_action)

        toolbar.addSeparator()

        icon_terminal = QPixmap("icons/terminal.png").scaled(icon_size)
        cmdver_action = QAction(QIcon(icon_terminal), "&LAN Pigeon Lite (Terminal)", self)
        cmdver_action.triggered.connect(self.run_lanpigeon_lite_thread)

        toolbar.addAction(cmdver_action)

        return toolbar

    @staticmethod
    def create_start_scan_button():
        b = QPushButton("Start Scan")
        b.setStyleSheet("background-color: #2e5d4b; color: white; font-weight: bold")
        b.setFixedWidth(70)
        return b

    @staticmethod
    def create_start_ip_entry():
        s_entry = QLineEdit()
        s_entry.setPlaceholderText("192.168.1.1")
        s_entry.setAlignment(Qt.AlignmentFlag.AlignLeft)
        s_entry.setFixedWidth(150)
        s_entry.setStyleSheet("padding: 4px; border: 4px; border-radius: 1px; margin-left: 10px;")
        return s_entry



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion')  # Set the style to Fusion
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

