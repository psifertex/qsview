import binaryninjaui
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, QLabel, QTreeWidgetItem, QApplication
from PySide6.QtCore import QSettings, Qt
from binaryninja import PluginCommand

class SettingsTree(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.setWindowTitle("QSettings Tree View")
        self.resize(800, 600)  # Increased the default size of the window

        # Create a QTreeWidget
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Key", "Value"])

        # Adjust the default column width for the key column
        self.tree.setColumnWidth(0, 300)  # Set key column width to 300 pixels

        # Optimize scrolling
        # self.tree.setUniformRowHeights(True)  # Optimize scrolling performance
        self.tree.setVerticalScrollMode(QTreeWidget.ScrollPerPixel)  # Smoother pixel-based scrolling

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        self.setLayout(layout)

        # Populate the tree with settings
        QApplication.setOverrideCursor(Qt.WaitCursor)  # Show busy cursor while loading data
        self.populate_tree(settings)
        QApplication.restoreOverrideCursor()  # Restore cursor after loading data

    def populate_tree(self, settings):
        for key in sorted(settings.allKeys()):
            parts = key.split('/')
            parent_item = self.tree.invisibleRootItem()
            for i, part in enumerate(parts):
                child_item = self.find_child_item(parent_item, part)
                if child_item:
                    parent_item = child_item
                else:
                    if i == len(parts) - 1:
                        # This is the last part, add key-value pair
                        value = settings.value(key)

                        # Add the key and create a QLabel for the value
                        item = QTreeWidgetItem(parent_item, [part])

                        # Create a QLabel for the value with word wrap enabled
                        label = QLabel(str(value))
                        label.setWordWrap(True)
                        
                        # Add the QLabel as the widget for the value column
                        self.tree.setItemWidget(item, 1, label)
                    else:
                        # Create a new parent item
                        parent_item = QTreeWidgetItem(parent_item, [part])

    def find_child_item(self, parent_item, text):
        # Traverse child items of parent_item and return the matching item
        for i in range(parent_item.childCount()):
            child = parent_item.child(i)
            if child.text(0) == text:
                return child
        return None

    # Override keyPressEvent to close window on Esc key press
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()  # Close the window when Esc is pressed
        else:
            super().keyPressEvent(event)

# Assuming a QApplication is already running, instantiate the SettingsTree widget
def show_settings_window(_):
    global mywin
    settings = QSettings()
    mywin = SettingsTree(settings)
    mywin.show()
    mywin.raise_()          
    mywin.activateWindow()

mywin = None

binaryninjaui.UIAction.registerAction("QSettings Viewer")
binaryninjaui.UIActionHandler.globalActions().bindAction("QSettings Viewer", binaryninjaui.UIAction(show_settings_window))
