import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import requests

SERVER_URL = 'http://127.0.0.1:5000'


def show_currency():
    response = requests.get('%s/currency/forecast/usd' % SERVER_URL)
    print(response.json())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(650, 450)
    w.move(300, 300)
    w.setWindowTitle('Currency Forecasting')

    get_currency_button = QPushButton('Get currency', w)
    get_currency_button.clicked.connect(show_currency)
    w.show()

    sys.exit(app.exec_())

