import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, \
    QHBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, \
    QTreeView, QRadioButton, QSystemTrayIcon, QMenuBar, QMenu, QMainWindow, QCheckBox, QStatusBar, QToolBar, QSizePolicy, QSpacerItem, QListWidget
from PyQt6.QtGui import QIcon, QFont, QPixmap, QAction
from PyQt6.QtCore import Qt, QSize, QRunnable, QThreadPool, QThread, pyqtSlot
from ui_config import *
from scan_test import *
import gui_widgets as widgets
import os
import platform

class Worker(QRunnable):
    '''
    Worker thread
    '''

    def __init__(self, function):
        super().__init__()
        self.function = function

    @pyqtSlot()
    def run(self):
        '''
        Run the specified function in this worker
        '''
        self.function()

    def run_terminal(self):
        '''
        Run the specified function in a new terminal window based on the platform
        '''
        if platform.system() == 'Windows':
            # Windows
            subprocess.call(['cmd.exe', '/c', 'python -c "from scan_test import scan_app; scan_app()"'])
        elif platform.system() == 'Darwin':
            # macOS
            subprocess.call(['open', '-a', 'Terminal', 'python -c "from scan_test import scan_app; scan_app()"'])
        elif platform.system() == 'Linux':
            # Linux
            subprocess.call(['gnome-terminal', '-e', 'python -c "from scan_test import scan_app; scan_app()"'])


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
        self.ui_config()

    def ui_config(self):
        # Create the top layout containers
        top_layout1 = QHBoxLayout()
        top_layout2 = QHBoxLayout()

        # Load the image using QPixmap
        logo = QPixmap("icon_dark.png")

        # resize the pixmap to 50x50
        logo = logo.scaled(100, 80)


        # Create the top 1 widgets

        top_label1 = QLabel("Top Frame 1")


        title = widgets.create_title_label()               # (1)

        start_ip_label = widgets.create_start_label()      # (2)

        start_ip_entry = widgets.create_start_ip_entry()   # (3)

        end_ip_label = widgets.create_end_label()          # (4)
        end_ip_entry = widgets.create_end_ip_entry()       # (5)

        # Add the top row 1 widgets
        #top_layout1.addWidget(top_label1)
        top_layout1.addWidget(title)
        top_layout1.addWidget(start_ip_label)
        top_layout1.addWidget(start_ip_entry)
        top_layout1.addWidget(end_ip_label)
        top_layout1.addWidget(end_ip_entry)

        # Create the top row 2 widgets
        top_label2 = QLabel("Top Frame 2")
        treeview = QTreeView()


        logo_label = QLabel()
        logo_label.setPixmap(logo)

        top_layout2.addWidget(top_label2)
        top_layout2.addWidget(treeview, stretch=(1))

        # Create the bottom layout containers
        bottom_layout1 = QHBoxLayout()
        bottom_layout2 = QHBoxLayout()
        bottom_layout3 = QHBoxLayout()

        # Create the bottom widgets
        bottom_label1 = QLabel("Bottom Frame 1")

        # Load the image using QPixmap
        logo = QPixmap("icon_dark.png")
        # resize the pixmap to 50x50
        logo = logo.scaled(100, 80)


        bottom_layout1.addWidget(bottom_label1)
        bottom_layout1.addWidget(logo_label)

        bottom_label2 = QLabel("Bottom Frame 2")
        bottom_radio_button2 = QRadioButton("Option 2")
        bottom_layout2.addWidget(bottom_label2)
        bottom_layout2.addWidget(bottom_radio_button2)


        bottom_label3 = QLabel("Bottom Frame 3")
        bottom_radio_button3 = QRadioButton("Option 3")

        bottom_layout3.addWidget(bottom_label3)
        bottom_layout3.addWidget(bottom_radio_button3)

        # Create the grid layout and add the widgets
        grid_layout = QGridLayout()

        #grid_layout.setColumnStretch(0, 0)

        grid_layout.addLayout(top_layout1, 0, 0, 1, 4)
        grid_layout.addLayout(top_layout2, 1, 0, 1, 2)
        grid_layout.addLayout(bottom_layout1, 2, 0)
        grid_layout.addLayout(bottom_layout2, 2, 1)
        grid_layout.addLayout(bottom_layout3, 2, 2)

        # Set the stretch factor of the first column to 0
        grid_layout.setRowStretch(1, 0)
        grid_layout.setRowStretch(2, 1)
        grid_layout.setRowStretch(3, 0)

        grid_layout.setColumnStretch(2, 1)


        # Set the main layout to the grid layout


        self.setLayout(grid_layout)

    @staticmethod
    def create_title_label():
        label = QLabel("LAN Pigeon")
        #label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label_font = label.font()
        label_font.setPixelSize(18)
        label.setFont(label_font)
        return label

    @staticmethod
    def create_start_label():
        label = QLabel("Starting IP Address:")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setStyleSheet("""
               background-color: #2e5d4b;
               color: white;
               font-weight: bold;
               padding: 4px;
               border-radius: 5px;
               """)
        label.setFixedWidth(125)
        return label

    @staticmethod
    def create_end_label():
        label = QLabel("Ending IP Address:")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setStyleSheet("""
               background-color: #932020;
               color: white;
               font-weight: bold;
               padding: 4px;
               border-radius: 5px;
               """)
        label.setFixedWidth(125)
        return label


    @staticmethod
    def create_start_ip_entry():
        s_entry = QLineEdit()
        s_entry.setPlaceholderText("192.168.1.1")
        s_entry.setAlignment(Qt.AlignmentFlag.AlignLeft)
        s_entry.setFixedWidth(150)
        s_entry.setStyleSheet("padding: 4px; border: 4px; border-radius: 1px; margin-left: 1px;")
        return s_entry

    @staticmethod
    def create_end_ip_entry():
        e_entry = QLineEdit()
        e_entry.setPlaceholderText("192.168.1.255")
        e_entry.setAlignment(Qt.AlignmentFlag.AlignLeft)
        e_entry.setFixedWidth(150)
        e_entry.setStyleSheet("padding: 4px; border: 4px; border-radius: 1px; margin-left: 1px;")
        return e_entry


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()

        # Set up the main window
        self.setWindowTitle("LAN Pigeon")
        self.setWindowIcon(QIcon("bit_icon.ico"))
        self.setGeometry(100, 100, 500, 300)
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

    def run_function(self, function):
        worker = Worker(function)
        self.threadpool.start(worker)

    def onMyToolBarButtonClick(self, s):
        print("click", s)

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
        start_scan_action.triggered.connect(self.onMyToolBarButtonClick)
        toolbar.addAction(start_scan_action)

        toolbar.addSeparator()

        stop_scan_action = QAction(QIcon("icons/icon_stop.png"), "&Stop Scan", self)
        stop_scan_action.setStatusTip("Stop Scanning IP Range.")
        stop_scan_action.triggered.connect(self.onMyToolBarButtonClick)
        toolbar.addAction(stop_scan_action)

        toolbar.addSeparator()

        icon_save = QPixmap("icons/icon_save.png").scaled(icon_size)
        save_action = QAction(QIcon(icon_save), "Save Results", self)
        save_action.setStatusTip("Save Scan Results.")
        toolbar.addAction(save_action)

        toolbar.addSeparator()

        icon_terminal = QPixmap("icons/terminal.png").scaled(icon_size)
        cmdver_action = QAction(QIcon(icon_terminal), "&LAN Pigeon Lite (Terminal)", self)
        cmdver_action.triggered.connect(lambda: window.run_function(scan_app))

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

