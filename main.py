import sys
from PyQt6.QtCore import QTimer, QTime
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTimeEdit, QMessageBox
)

# Global stopwatch and timer state variables
sec = 0
min = 0
running = False
timer_duration = 0
is_timer_running = False

class TimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My Clock')
        self.setWindowIcon(QIcon(r"d:/programowanie/python/stopwatch/icon.ico"))

        # Main layout (horizontal)
        self.main_layout = QHBoxLayout()

        # Stopwatch layout
        self.stopwatch_layout = QVBoxLayout()
        self.timer_label = QLabel('00:00', self)
        self.timer_label.setStyleSheet("font-size: 60px; max-width: 178px; font-family: Montserrat; font-weight: bold;")
        self.stopwatch_layout.addWidget(self.timer_label)

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_timer)
        self.start_button.setStyleSheet("height: 50px; max-width: 178px; font-size: 17px; font-family: Montserrat; font-weight: bold;")
        self.stopwatch_layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_timer)
        self.stop_button.setStyleSheet("height: 50px; max-width: 178px; font-size: 17px; font-family: Montserrat; font-weight: bold;")
        self.stop_button.setEnabled(False)
        self.stopwatch_layout.addWidget(self.stop_button)

        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_timer)
        self.reset_button.setStyleSheet("height: 50px; max-width: 178px; font-size: 17px; font-family: Montserrat; font-weight: bold;")
        self.stopwatch_layout.addWidget(self.reset_button)

        # Timer layout
        self.timer_layout = QVBoxLayout()

        self.timer_input = QTimeEdit(self)
        self.timer_input.setStyleSheet("height: 60px; min-width: 178px; max-width: 178px; font-size: 20px;")
        self.timer_input.setDisplayFormat('mm:ss')
        self.timer_input.setTime(QTime(0, 0))
        self.timer_layout.addWidget(self.timer_input)

        self.start_timer_button = QPushButton('Start Timer', self)
        self.start_timer_button.clicked.connect(self.start_countdown)
        self.start_timer_button.setStyleSheet("height: 50px; max-width: 178px; font-size: 17px; font-family: Montserrat; font-weight: bold;")
        self.timer_layout.addWidget(self.start_timer_button)

        self.reset_timer_button = QPushButton('Reset Timer', self)
        self.reset_timer_button.clicked.connect(self.reset_timer_display)
        self.reset_timer_button.setStyleSheet("height: 50px; max-width: 178px; font-size: 17px; font-family: Montserrat; font-weight: bold;")
        self.timer_layout.addWidget(self.reset_timer_button)

        self.stop_timer_button = QPushButton('Stop Timer', self)
        self.stop_timer_button.clicked.connect(self.pause_countdown)
        self.stop_timer_button.setStyleSheet("height: 50px; max-width: 178px; font-size: 17px; font-family: Montserrat; font-weight: bold;")
        self.stop_timer_button.setEnabled(False)
        self.timer_layout.addWidget(self.stop_timer_button)

        self.abort_timer_button = QPushButton('Abort Timer', self)
        self.abort_timer_button.clicked.connect(self.abort_countdown)
        self.abort_timer_button.setStyleSheet("height: 50px; max-width: 178px; font-size: 17px; font-family: Montserrat; font-weight: bold;")
        self.abort_timer_button.setEnabled(False)
        self.timer_layout.addWidget(self.abort_timer_button)

        # Add layouts to main layout
        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(self.stopwatch_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.timer_layout)
        self.main_layout.addSpacing(10)
        self.setLayout(self.main_layout)

        # Stopwatch QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        # Countdown QTimer
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.countdown)

    def set_stopwatch_enabled(self, enabled):
        self.start_button.setEnabled(enabled)
        self.stop_button.setEnabled(enabled and running)
        self.reset_button.setEnabled(enabled)

    def set_timer_enabled(self, enabled):
        self.start_timer_button.setEnabled(enabled)
        self.timer_input.setEnabled(enabled)
        self.stop_timer_button.setEnabled(enabled and is_timer_running)
        self.abort_timer_button.setEnabled(enabled and is_timer_running)
        self.reset_timer_button.setEnabled(enabled)

    def start_timer(self):
        global running
        if not running:
            running = True
            self.timer.start(1000)
            self.set_timer_enabled(False)
            self.set_stopwatch_enabled(True)
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)

    def stop_timer(self):
        global running
        running = False
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def reset_timer(self):
        global sec, min
        sec = 0
        min = 0
        self.update_timer_display()
        self.set_timer_enabled(True)

    def update_timer(self):
        global sec, min
        if sec < 59:
            sec += 1
        else:
            sec = 0
            min += 1
        self.update_timer_display()

    def update_timer_display(self):
        self.timer_label.setText(f'{min:02}:{sec:02}')

    def start_countdown(self):
        global timer_duration, is_timer_running
        time_input = self.timer_input.time()
        if not is_timer_running:
            timer_duration = time_input.minute() * 60 + time_input.second()
        if timer_duration > 0:
            is_timer_running = True
            self.set_stopwatch_enabled(False)
            self.set_timer_enabled(True)
            self.start_timer_button.setEnabled(False)
            self.stop_timer_button.setEnabled(True)
            self.abort_timer_button.setEnabled(True)
            self.timer_input.setEnabled(False)
            self.countdown_timer.start(1000)
        else:
            self.show_error('Please set a valid time greater than 00:00')

    def countdown(self):
        global timer_duration, is_timer_running
        if timer_duration > 0:
            timer_duration -= 1
            minutes = timer_duration // 60
            seconds = timer_duration % 60
            self.timer_label.setText(f'{minutes:02}:{seconds:02}')
        else:
            self.countdown_timer.stop()
            is_timer_running = False
            self.show_message('End timer!', 'Timer has stopped.')
            self.reset_timer_display()

    def pause_countdown(self):
        global is_timer_running
        if is_timer_running:
            self.countdown_timer.stop()
            self.start_timer_button.setEnabled(True)
            self.stop_timer_button.setEnabled(False)

    def abort_countdown(self):
        global timer_duration, is_timer_running
        self.countdown_timer.stop()
        timer_duration = 0
        is_timer_running = False
        self.timer_label.setText('00:00')
        self.timer_input.setTime(QTime(0, 0))
        self.set_stopwatch_enabled(True)
        self.set_timer_enabled(True)

    def reset_timer_display(self):
        global timer_duration, is_timer_running
        self.countdown_timer.stop()
        is_timer_running = False
        time_input = self.timer_input.time()
        timer_duration = time_input.minute() * 60 + time_input.second()
        self.timer_label.setText(f'{time_input.minute():02}:{time_input.second():02}')
        self.set_stopwatch_enabled(True)
        self.set_timer_enabled(True)

    def show_error(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec()

    def show_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.exec()

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimerApp()
    window.show()
    sys.exit(app.exec())
