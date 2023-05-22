from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QLabel, QPushButton, QLineEdit, QTreeView,
                             QRadioButton, QSystemTrayIcon, QMenuBar, QMenu)
from PyQt6.QtCore import Qt, QRunnable, pyqtSlot
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from thread_worker import *
from endpoint import *
from endpoint_list import *
from scan import *

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


def create_title_label():
    label = QLabel("LAN Pigeon")
    # label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    label_font = label.font()
    label_font.setPixelSize(18)
    label.setFont(label_font)
    return label


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


def create_start_scan_button():
    b = QPushButton("Start Scan")
    b.setStyleSheet("background-color: #2e5d4b; color: white; font-weight: bold")
    b.setFixedWidth(70)
    return b

def start_scan_button_trigger(start, end):
    start_ip, end_ip = start, end
    start = list(map(int, start_ip.split('.')))
    end = list(map(int, end_ip.split('.')))

    ips = []
    for i in range(start[3], end[3] + 1):
        ip = f"{start[0]}.{start[1]}.{start[2]}.{i}"
        ips.append(ip)
    cores = cpu_cores()  # amount of cores in CPU
    usage = cpu_usage()  # maps current usage of CPU in %
    x = 3  # thread multiplier, default 3
    endpoints = EndpointArray(thread_workers(scan, ips, cores, usage, x))  # runs function with set amount of threads
    QApplication.processEvents()
    return update_treeview(endpoints)


def create_start_ip_entry():
    s_entry = QLineEdit()
    s_entry.setPlaceholderText("192.168.1.1")
    s_entry.setAlignment(Qt.AlignmentFlag.AlignLeft)
    s_entry.setFixedWidth(150)
    s_entry.setStyleSheet("padding: 4px; border: 4px; border-radius: 1px; margin-left: 10px;")
    return s_entry


def create_end_ip_entry():
    e_entry = QLineEdit()
    e_entry.setPlaceholderText("192.168.1.255")
    e_entry.setAlignment(Qt.AlignmentFlag.AlignLeft)
    e_entry.setFixedWidth(150)
    e_entry.setStyleSheet("padding: 4px; border: 4px; border-radius: 1px; margin-left: 10px;")
    return e_entry


def create_treeview(data):
    headers = ["IP Address", "Hostname", "Ping", "MAC Address"]
    treeview = QTreeView()
    model = QStandardItemModel()
    model.setHorizontalHeaderLabels(headers)
    treeview.setModel(model)

    root_item = model.invisibleRootItem()
    if data is None:
        item = 'test'
        ip_item = QStandardItem(item)
        hostname_item = QStandardItem(item)
        ping_item = QStandardItem(item)
        mac_item = QStandardItem(item)
        root_item.appendRow([ip_item, hostname_item, ping_item, mac_item])
    else:
        for item in data:
            ip_item = QStandardItem(item["ip_address"])
            hostname_item = QStandardItem(item["hostname_status"])
            ping_item = QStandardItem(item["ping_status"])
            mac_item = QStandardItem(item["mac_address"])
            root_item.appendRow([ip_item, hostname_item, ping_item, mac_item])

    return treeview

def update_treeview(tv, data):
    model = tv.treeview.model()
    model.clear()  # Clear the existing data in the model

    if data is not None:
        headers = ["IP Address", "Hostname", "Ping", "MAC Address"]
        model.setHorizontalHeaderLabels(headers)

        root_item = model.invisibleRootItem()
        for item in data:
            ip_item = QStandardItem(item["ip_address"])
            hostname_item = QStandardItem(item["hostname_status"])
            ping_item = QStandardItem(item["ping_status"])
            mac_item = QStandardItem(item["mac_address"])
            root_item.appendRow([ip_item, hostname_item, ping_item, mac_item])

    # Resize the columns to fit the content
    tv.treeview.resizeColumnToContents(0)
    tv.treeview.resizeColumnToContents(1)
    tv.treeview.resizeColumnToContents(2)
    tv.treeview.resizeColumnToContents(3)
    QApplication.processEvents()
