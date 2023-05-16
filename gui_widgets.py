from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QLabel, QPushButton, QLineEdit, QTreeView,
                             QRadioButton, QSystemTrayIcon, QMenuBar, QMenu)
from PyQt6.QtCore import Qt


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