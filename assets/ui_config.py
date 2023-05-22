from PyQt6.QtWidgets import QHBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, \
    QTreeView, QRadioButton
from PyQt6.QtGui import QPixmap
import gui_widgets as widgets


def C_Window_UI(self):
    # Create the top layout containers
    top_layout1 = QHBoxLayout()
    top_layout2 = QHBoxLayout()

    # Load the image using QPixmap
    logo = QPixmap("icon_dark.png")

    # resize the pixmap to 50x50
    logo = logo.scaled(100, 80)

    # Create the top 1 widgets

    top_label1 = QLabel("Top Frame 1")

    title = widgets.create_title_label()  # (1)

    start_ip_label = widgets.create_start_label()  # (2)

    start_ip_entry = widgets.create_start_ip_entry()  # (3)

    end_ip_label = widgets.create_end_label()  # (4)
    end_ip_entry = widgets.create_end_ip_entry()  # (5)

    # Add the top row 1 widgets
    # top_layout1.addWidget(top_label1)
    top_layout1.addWidget(title)
    top_layout1.addWidget(start_ip_label)
    top_layout1.addWidget(start_ip_entry)
    top_layout1.addWidget(end_ip_label)
    top_layout1.addWidget(end_ip_entry)

    # Create the top row 2 widgets
    treeview = widgets.create_treeview([])

    logo_label = QLabel()
    logo_label.setPixmap(logo)

    top_layout2.addWidget(treeview, stretch=1)

    # Create the bottom layout containers
    bottom_layout1 = QHBoxLayout()
    bottom_layout2 = QHBoxLayout()
    bottom_layout3 = QHBoxLayout()

    # Create the bottom widgets

    # Load the image using QPixmap
    logo = QPixmap("icon_dark.png")
    # resize the pixmap to 50x50
    logo = logo.scaled(100, 80)

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

    # grid_layout.setColumnStretch(0, 0)

    grid_layout.addLayout(top_layout1, 0, 0, 1, 4)
    grid_layout.addLayout(top_layout2, 1, 0, 1, 4)
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

if __name__  == "__main__":
    C_Window_UI()