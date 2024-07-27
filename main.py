import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QDateTime
import socketio

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
        self.input_area.textChanged.connect(self.notify_typing)

        self.sio = socketio.Client()
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('message', self.on_message)
        self.sio.on('edit_message', self.on_edit_message)
        self.sio.on('delete_message', self.on_delete_message)
        self.sio.on('typing', self.on_typing)
        self.connect_to_server()

        self.typing_label = QLabel('', self)
        layout.addWidget(self.typing_label)

        self.connected = False

    def connect_to_server(self):
        try:
            self.sio.connect('http://localhost:5000')
        except socketio.exceptions.ConnectionError as e:
            self.chat_area.append('<i>Connection failed. Please check the server and try again.</i>')

    def send_message(self):
        if self.connected:
            message = self.input_area.text()
            if message:
                timestamp = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
                self.sio.emit('message', {'username': self.username_input.text(), 'message': message, 'timestamp': timestamp})
                self.chat_area.append(f'<b>You</b> [{timestamp}]: {message}')
                self.input_area.clear()

    def on_connect(self):
        self.chat_area.append('<i>Connected to server</i>')
        self.connected = True

    def on_disconnect(self):
        self.chat_area.append('<i>Disconnected from server</i>')
        self.connected = False

    def on_message(self, data):
        color = 'blue' if data['username'] == self.username_input.text() else 'green'
        self.chat_area.append(f'<span style="color:{color};"><b>{data["username"]}</b> [{data["timestamp"]}]</span>: {data["message"]}')

    def on_edit_message(self, data):
        self.chat_area.append(f'<i>Message edited by {data["username"]}: {data["message"]}</i>')

    def on_delete_message(self, data):
        self.chat_area.append(f'<i>Message deleted by {data["username"]}</i>')

    def on_typing(self, data):
        self.typing_label.setText(f'{data["username"]} is typing...')

    def notify_typing(self):
        if self.connected:
            self.sio.emit('typing', {'username': self.username_input.text()})

    def closeEvent(self, event):
        if self.connected:
            self.sio.disconnect()
        event.accept()

app = QApplication(sys.argv)
window = ChatWindow()
window.show()
sys.exit(app.exec_())
