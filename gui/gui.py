import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
import requests

SERVER_URL = 'http://127.0.0.1:5000'




class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def show_currency(self):
        response = requests.get('%s/currency/forecast/usd' % SERVER_URL)
        print(response.json())

    def initUI(self):
        self.setGeometry(650, 450, 300, 300)
        self.setWindowTitle('Currency Forecasting')
        self.setWindowIcon(QIcon('icon.png'))
        self.get_currency_button = QPushButton('Get currency', self)
        self.get_currency_button.clicked.connect(self.show_currency)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())



