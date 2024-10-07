import sys
import time
import pyautogui
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
)
from PyQt6.QtCore import QTimer
from qt_material import apply_stylesheet


class AutoClicker(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.clicking = False
        self.click_timer = QTimer()
        self.click_timer.timeout.connect(self.auto_clicker)

    def init_ui(self):
        self.setWindowTitle('Banana Auto Clicker')
        self.setGeometry(100, 100, 300, 400)


        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Deutsch", "Italiano"])
        self.language_combo.currentTextChanged.connect(self.update_language)
        self.language_combo.setCurrentText("English") 
        layout = QVBoxLayout()
        layout.addWidget(self.language_combo)


        self.timeout_label = QLabel('Timeout before starting (seconds):')
        self.timeout_input = QLineEdit("10")  # Default value of 10 seconds
        layout.addWidget(self.timeout_label)
        layout.addWidget(self.timeout_input)

        self.clicks_label = QLabel('Number of clicks per second:')
        self.clicks_input = QLineEdit("10")  # Default value of 10 clicks per second
        layout.addWidget(self.clicks_label)
        layout.addWidget(self.clicks_input)

        self.duration_label = QLabel('Duration of clicking (seconds):')
        self.duration_input = QLineEdit("10")  # Default value of 10 seconds
        layout.addWidget(self.duration_label)
        layout.addWidget(self.duration_input)

        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_clicking)
        layout.addWidget(self.start_button)

        # Theme buttons
        self.theme_dark_button = QPushButton("Dark Theme")
        self.theme_dark_button.clicked.connect(lambda: self.change_theme('dark_teal.xml'))
        layout.addWidget(self.theme_dark_button)

        self.theme_light_button = QPushButton("Light Theme")
        self.theme_light_button.clicked.connect(lambda: self.change_theme('light_teal.xml'))
        layout.addWidget(self.theme_light_button)

        self.setLayout(layout)

        # Set the default language
        self.language = "English"
        self.update_language(self.language)

    def change_theme(self, theme):
        # Apply the selected theme
        apply_stylesheet(app, theme=theme)

    def update_language(self, lang):
        # Update language based on selection
        if lang == "Deutsch":
            self.timeout_label.setText('Timeout vor dem Start (Sekunden):')
            self.clicks_label.setText('Anzahl der Klicks pro Sekunde:')
            self.duration_label.setText('Dauer des Klickens (Sekunden):')
            self.start_button.setText('Start')
            self.theme_dark_button.setText("Dunkles Theme")
            self.theme_light_button.setText("Helles Theme")
            self.language = "German"
        elif lang == "Italiano":
            self.timeout_label.setText('Timeout prima di iniziare (secondi):')
            self.clicks_label.setText('Numero di clic al secondo:')
            self.duration_label.setText('Durata del clic (secondi):')
            self.start_button.setText('Inizia')
            self.theme_dark_button.setText("Tema scuro")
            self.theme_light_button.setText("Tema chiaro")
            self.language = "Italian"
        else:  # Default to English
            self.timeout_label.setText('Timeout before starting (seconds):')
            self.clicks_label.setText('Number of clicks per second:')
            self.duration_label.setText('Duration of clicking (seconds):')
            self.start_button.setText('Start')
            self.theme_dark_button.setText("Dark Theme")
            self.theme_light_button.setText("Light Theme")
            self.language = "English"

    def start_clicking(self):
        try:
            timeout = float(self.timeout_input.text())
            clicks_per_second = float(self.clicks_input.text())
            duration = float(self.duration_input.text())
            self.click_interval = 1 / clicks_per_second  # Interval in seconds
            self.clicking = True

            # Wait for the specified timeout before starting clicking
            QMessageBox.information(self, 'Wait', f'The auto-clicker will start in {timeout} seconds...')
            QTimer.singleShot(int(timeout * 1000), self.start_auto_clicking)  # Timeout timer
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Please enter valid numbers.')

    def start_auto_clicking(self):
        self.start_time = time.time()
        self.click_timer.start(int(self.click_interval * 1000))  # Interval in milliseconds

        # Stop after the defined duration
        QTimer.singleShot(int(self.duration_input.text()) * 1000, self.stop_clicking)  # Duration stop timer

    def stop_clicking(self):
        self.clicking = False
        self.click_timer.stop()
        QMessageBox.information(self, 'Done', 'Auto-clicker stopped.')

    def auto_clicker(self):
        if self.clicking:
            pyautogui.click()  # Click at the current mouse position
            print(f"Click performed: {time.time()}")  # For debugging

    def closeEvent(self, event):
        # Stop the clicker when the window is closed
        self.clicking = False
        self.click_timer.stop()
        event.accept()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Apply the default theme (dark)
    apply_stylesheet(app, theme='dark_teal.xml')

    clicker = AutoClicker()
    clicker.show()
    sys.exit(app.exec())
