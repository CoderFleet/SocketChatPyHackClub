import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Anonymous Chat')
        self.setGeometry(100, 100, 600, 400)

        self.chat_area = QTextEdit(self)
        self.chat_area.setReadOnly(True)
        
        self.input_area = QLineEdit(self)
        
        self.send_button = QPushButton('Send', self)
        
        self.username_label = QLabel('Username:', self)
        self.username_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.username_input = QLineEdit(self)
        
        username_layout = QHBoxLayout()
        username_layout.addWidget(self.username_label)
        username_layout.addWidget(self.username_input)
        
        layout = QVBoxLayout()
        layout.addLayout(username_layout)
        layout.addWidget(self.chat_area)
        layout.addWidget(self.input_area)
        layout.addWidget(self.send_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.send_button.clicked.connect(self.send_message)

    def send_message(self):
        message = self.input_area.text()
        self.chat_area.append(f'You: {message}')
        self.input_area.clear()

app = QApplication(sys.argv)
window = ChatWindow()
window.show()
sys.exit(app.exec_())
