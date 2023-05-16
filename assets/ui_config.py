from PyQt6.QtWidgets import QHBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, \
    QTreeView, QRadioButton
from PyQt6.QtGui import QPixmap


def ui(self):
    # Create the top layout containers
    top_layout1 = QHBoxLayout()
    top_layout2 = QHBoxLayout()

    # Load the image using QPixmap
    logo = QPixmap("icon_dark.png")

    # resize the pixmap to 50x50
    logo = logo.scaled(100, 80)

    # Create the top 1 widgets

    title = self.create_title_label()
    top_button1 = QPushButton("Button 1")
    start_scan_button = self.create_start_scan_button()
    start_ip_entry = self.create_start_ip_entry()

    # Add the top row 1 widgets
    top_layout1.addWidget(title)
    top_layout1.addWidget(top_button1)
    top_layout1.addWidget(start_scan_button)
    top_layout1.addWidget(start_ip_entry)

    # Create the top row 2 widgets
    logo_label = QLabel()
    logo_label.setPixmap(logo)
    top_button3 = QPushButton("Button 3")
    stop_scan_button = QPushButton("Stop Scan")
    stop_scan_button.setStyleSheet("background-color: #932020; color: white; font-weight: bold")
    stop_scan_button.setFixedWidth(70)
    end_ip_entry = self.create_end_ip_entry()

    top_layout2.addWidget(logo_label)
    top_layout2.addWidget(top_button3)
    top_layout2.addWidget(stop_scan_button)
    top_layout2.addWidget(end_ip_entry)

    # Create the bottom layout containers
    bottom_layout1 = QHBoxLayout()
    bottom_layout2 = QHBoxLayout()
    bottom_layout3 = QHBoxLayout()

    # Create the bottom widgets
    bottom_label1 = QLabel("Bottom Frame 1")
    bottom_button1 = QPushButton("Button 5")
    bottom_button2 = QPushButton("Button 6")
    bottom_entry1 = QLineEdit()
    bottom_tree_view1 = QTreeView()

    bottom_layout1.addWidget(bottom_label1)
    bottom_layout1.addWidget(bottom_button1)
    bottom_layout1.addWidget(bottom_button2)
    bottom_layout1.addWidget(bottom_entry1)
    bottom_layout1.addWidget(bottom_tree_view1)

    bottom_label2 = QLabel("Bottom Frame 2")
    bottom_button3 = QPushButton("Button 7")
    bottom_button4 = QPushButton("Button 8")
    bottom_entry2 = QLineEdit()
    bottom_tree_view2 = QTreeView()

    bottom_layout2.addWidget(bottom_label2)
    bottom_layout2.addWidget(bottom_button3)
    bottom_layout2.addWidget(bottom_button4)
    bottom_layout2.addWidget(bottom_entry2)
    bottom_layout2.addWidget(bottom_tree_view2)

    bottom_label3 = QLabel("Bottom Frame 3")
    bottom_radio_button1 = QRadioButton("Option 1")
    bottom_radio_button2 = QRadioButton("Option 2")
    bottom_radio_button3 = QRadioButton("Option 3")

    bottom_layout3.addWidget(bottom_label3)
    bottom_layout3.addWidget(bottom_radio_button1)
    bottom_layout3.addWidget(bottom_radio_button2)
    bottom_layout3.addWidget(bottom_radio_button3)

    # Create the grid layout and add the widgets
    grid_layout = QGridLayout()

    grid_layout.addLayout(top_layout1, 0, 0, 1, 3)
    grid_layout.addLayout(top_layout2, 1, 0, 2, 3)
    grid_layout.addLayout(bottom_layout1, 3, 0)
    grid_layout.addLayout(bottom_layout2, 3, 1)
    grid_layout.addLayout(bottom_layout3, 3, 2)

    grid_layout.setColumnStretch(0, 1)
    grid_layout.setColumnStretch(1, 4)
    grid_layout.setColumnStretch(2, 1)

    # Set the main layout to the grid layout
    self.setLayout(grid_layout)

if __name__  == "__main__":
    ui()