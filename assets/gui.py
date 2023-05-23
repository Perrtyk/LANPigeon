import sys
import traceback

from PyQt6.QtWidgets import QApplication, QWidget, QMenuBar, QMenu, QMainWindow, QStatusBar, QToolBar, QHeaderView
from PyQt6.QtGui import QIcon, QAction, QStandardItem, QFont
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


class WidgetWindow(QWidget):
    def __init__(self, treeview):
        super().__init__()
        self.setWindowIcon(QIcon("bit_icon.ico"))
        self.setWindowTitle("LAN Pigeon")
        self.current_dir = os.getcwd()

        self._treeview = treeview


        # Resets working directory for compatibility issues
        print("Current working directory:", self.current_dir)
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        print("New working directory:", os.getcwd())

        self.top_layout1 = QHBoxLayout()
        self.top_layout2 = QHBoxLayout()

        # Load the image using QPixmap
        self.logo = QPixmap("icon_dark.png")

        # resize the pixmap to 50x50
        self.logo = self.logo.scaled(100, 80)

        # Create the top 1 widgets

        top_label1 = QLabel("Top Frame 1")

        self.title = widgets.create_title_label()  # (1)

        self.start_ip_label = widgets.create_start_label()  # (2)

        self.start_ip_entry = widgets.create_start_ip_entry()  # (3)

        self.end_ip_label = widgets.create_end_label()  # (4)
        self.end_ip_entry = widgets.create_end_ip_entry()  # (5)

        # Add the top row 1 widgets
        # top_layout1.addWidget(top_label1)
        self.top_layout1.addWidget(self.title)
        self.top_layout1.addWidget(self.start_ip_label)
        self.top_layout1.addWidget(self.start_ip_entry)
        self.top_layout1.addWidget(self.end_ip_label)
        self.top_layout1.addWidget(self.end_ip_entry)

        # Create the top row 2 widgets
        self.treeview = widgets.create_treeview([])
        self.treeview.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.treeview.customContextMenuRequested.connect(self.show_context_menu)

        self.logo_label = QLabel()
        self.logo_label.setPixmap(self.logo)

        self.top_layout2.addWidget(self.treeview, stretch=1)

        # Create the bottom layout containers
        self.bottom_layout1 = QHBoxLayout()
        self.bottom_layout2 = QHBoxLayout()
        self.bottom_layout3 = QHBoxLayout()

        # Create the bottom widgets

        # Load the image using QPixmap
        self.logo = QPixmap("icon_dark.png")
        # resize the pixmap to 50x50
        self.logo = self.logo.scaled(100, 80)

        self.bottom_layout1.addWidget(self.logo_label)

        self.bottom_label2 = QLabel("Bottom Frame 2")
        bottom_radio_button2 = QRadioButton("Option 2")
        self.bottom_layout2.addWidget(self.bottom_label2)
        self.bottom_layout2.addWidget(bottom_radio_button2)

        self.bottom_label3 = QLabel("Bottom Frame 3")
        bottom_radio_button3 = QRadioButton("Option 3")

        self.bottom_layout3.addWidget(self.bottom_label3)
        self.bottom_layout3.addWidget(bottom_radio_button3)

        # Create the grid layout and add the widgets
        grid_layout = QGridLayout()

        # grid_layout.setColumnStretch(0, 0)

        grid_layout.addLayout(self.top_layout1, 0, 0, 1, 4)
        grid_layout.addLayout(self.top_layout2, 1, 0, 1, 4)
        grid_layout.addLayout(self.bottom_layout1, 2, 0)
        grid_layout.addLayout(self.bottom_layout2, 2, 1)
        grid_layout.addLayout(self.bottom_layout3, 2, 2)

        # Set the stretch factor of the first column to 0
        grid_layout.setRowStretch(1, 0)
        grid_layout.setRowStretch(2, 1)
        grid_layout.setRowStretch(3, 0)

        grid_layout.setColumnStretch(2, 1)

        # Set the main layout to the grid layout

        self.setLayout(grid_layout)

    def update_treeview(self, data):
        model = self.treeview.model()
        model.clear()  # Clear the existing data in the model

        if data is not None:
            headers = ["IP Address", "Hostname", "Ping", "MAC Address"]

            # Add padding to each header
            padded_headers = [f"          {header}          " for header in headers]
            model.setHorizontalHeaderLabels(padded_headers)

            root_item = model.invisibleRootItem()
            for item in data:
                ip_item = QStandardItem(item["ip_address"])
                hostname_item = QStandardItem(item["hostname_status"])
                ping_item = QStandardItem(item["ping_status"])
                mac_item = QStandardItem(item["mac_address"])
                root_item.appendRow([ip_item, hostname_item, ping_item, mac_item])

        # Center align the headers in their columns
        header = self.treeview.header()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set the resize mode to interactive and stretch for adding padding and maintaining manual stretching
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

        # Optionally, you can adjust the font style of the headers
        font = QFont("Arial", 10, QFont.Weight.Bold)
        header.setFont(font)

        QApplication.processEvents()
    def show_context_menu(self, pos):
        index = self.treeview.indexAt(pos)
        if index.isValid():
            menu = QMenu(self.treeview)
            copy_action = menu.addAction("Copy")
            action = menu.exec(self.treeview.mapToGlobal(pos))

            if action == copy_action:
                item = self.treeview.model().itemFromIndex(index)
                if item is not None:
                    value = item.text()
                    clipboard = QApplication.clipboard()
                    clipboard.setText(value)


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
        child_window = WidgetWindow([])
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
        data = [{'ip_address': '192.168.1.1', 'alive_status': 'Yes', 'ping_status': ' 0 ms',
                 'hostname_status': 'router.localdomain', 'mac_address': 'd2:21:f9:c5:84:ef'},
                {'ip_address': '192.168.1.2', 'alive_status': 'Yes', 'ping_status': ' 0 ms', 'hostname_status': 'PC-A',
                 'mac_address': '00:24:25:a3:3e:aa'},
                {'ip_address': '192.168.1.3', 'alive_status': 'Yes', 'ping_status': ' 0 ms', 'hostname_status': 'N/A',
                 'mac_address': 'fg:aa:15:7b:8d:6g'},
                {'ip_address': '192.168.1.254', 'alive_status': 'Yes', 'ping_status': ' 0 ms', 'hostname_status': 'DNS-server',
                 'mac_address': 'fg:aa:15:7b:8d:6g'}
                ]  # Updated data for the treeview

        print('Clicked Run Scan Button!')
        print('Sleep for 5 Seconds, expect responsive GUI.')
        time.sleep(5)
        print('Sleep Complete.')
        self.centralWidget().update_treeview(data)

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
