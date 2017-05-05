import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from currency_forecast_client_api import CurrencyForecastClient

SERVER_URL = 'https://secure-chamber-24424.herokuapp.com'


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def show_currency(self):
        client = CurrencyForecastClient(SERVER_URL)
        response = client.get_actual_value_for_currency("usd")
        print(response)

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



