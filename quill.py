import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QListWidget, QTextEdit, QPushButton, 
                               QInputDialog, QMessageBox, QSplitter)
from PySide6.QtCore import Qt

class NotesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notes App")
        self.resize(800, 600)
        
        self.notes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes_data")
        if not os.path.exists(self.notes_dir):
            os.makedirs(self.notes_dir)

        self.current_note = None

        self.setup_ui()
        self.apply_dark_theme()
        self.load_notes_list()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QHBoxLayout(main_widget)
        
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # Left Panel (List of notes)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        self.notes_list = QListWidget()
        self.notes_list.itemClicked.connect(self.on_note_selected)
        
        self.new_btn = QPushButton("New Note")
        self.new_btn.clicked.connect(self.create_new_note)
        
        left_layout.addWidget(self.new_btn)
        left_layout.addWidget(self.notes_list)
        
        # Right Panel (Editor)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        self.text_editor = QTextEdit()
        
        self.save_btn = QPushButton("Save Note")
        self.save_btn.clicked.connect(self.save_note)
        
        right_layout.addWidget(self.text_editor)
        right_layout.addWidget(self.save_btn)
        
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        
        splitter.setSizes([200, 600])

    def apply_dark_theme(self):
        # Setting a modern font
        font = self.font()
        font.setFamily("Inter, Roboto, Segoe UI, sans-serif")
        self.setFont(font)
        
        dark_stylesheet = """
            QMainWindow, QWidget {
                background-color: #121212;
                color: #e0e0e0;
                font-family: "Inter", "Roboto", "Segoe UI", sans-serif;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #333333;
                border-radius: 8px;
                padding: 12px;
                font-size: 20px;
            }
            QListWidget {
                background-color: #1a1a1a;
                color: #e0e0e0;
                border: 1px solid #333333;
                border-radius: 8px;
                padding: 8px;
                outline: none;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 6px;
                margin-bottom: 2px;
            }
            QListWidget::item:hover {
                background-color: #2a2a2a;
            }
            QListWidget::item:selected {
                background-color: #0d47a1;
                color: #ffffff;
                font-weight: bold;
            }
            QPushButton {
                background-color: #1976d2;
                color: #ffffff;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
            QSplitter::handle {
                background-color: transparent;
            }
            QInputDialog QLabel, QMessageBox QLabel {
                color: #e0e0e0;
            }
            QInputDialog QLineEdit {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #333333;
                border-radius: 6px;
                padding: 8px;
            }
            QMessageBox QPushButton {
                min-width: 80px;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #424242;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #525252;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """
        self.setStyleSheet(dark_stylesheet)

    def load_notes_list(self):
        self.notes_list.clear()
        for filename in sorted(os.listdir(self.notes_dir)):
            if filename.endswith(".txt"):
                self.notes_list.addItem(filename)

    def on_note_selected(self, item):
        filename = item.text()
        filepath = os.path.join(self.notes_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            self.text_editor.setPlainText(content)
            self.current_note = filename

    def create_new_note(self):
        name, ok = QInputDialog.getText(self, "New Note", "Enter note name:")
        if ok and name:
            if not name.endswith(".txt"):
                name += ".txt"
            filepath = os.path.join(self.notes_dir, name)
            if not os.path.exists(filepath):
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("")
                self.load_notes_list()
                
                items = self.notes_list.findItems(name, Qt.MatchExactly)
                if items:
                    self.notes_list.setCurrentItem(items[0])
                    self.on_note_selected(items[0])
            else:
                QMessageBox.warning(self, "Error", "Note already exists.")

    def save_note(self):
        if self.current_note:
            filepath = os.path.join(self.notes_dir, self.current_note)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(self.text_editor.toPlainText())
            QMessageBox.information(self, "Success", "Note saved successfully.")
        else:
            QMessageBox.warning(self, "Error", "No note selected to save.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NotesApp()
    window.show()
    sys.exit(app.exec())
