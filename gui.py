import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,
                            QGridLayout, QComboBox, QLineEdit, QAction, qApp)
from PyQt5.QtGui import QIcon
from currency_forecast_client_api import CurrencyForecastClient

SERVER_URL = 'https://secure-chamber-24424.herokuapp.com'
SERVER_PORT = 443
available_currencies = ['usd', 'eur', 'pln', 'gbp']


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(650, 450, 500, 500)
        self.setWindowTitle('Currency Forecasting')
        self.setWindowIcon(QIcon('icon.png'))
        self.initUI()

    def show_actual_currency(self):
        client = CurrencyForecastClient(self.server_url.text(), int(self.server_port.text()))
        response = client.get_actual_value_for_currency(self.currency_base, self.currency_code)
        self.current_value.setText(str(response[self.currency_base]))
        print(response)

    def show_currency_forecast(self):
        client = CurrencyForecastClient(self.server_url.text(), int(self.server_port.text()))
        response = client.forecast_currency(self.currency_base, self.currency_code)
        self.predicted_value.setText(str(response[self.currency_base]))
        print(response)

    def get_base_currency(self, text):
        self.currency_base = text

    def get_code_currency(self, text):
        self.currency_code = text

    def _setup_currency_base(self):
        self.currency_base_label = QLabel('Base currency', self)
        self.currency_base_combo = QComboBox(self)
        self.currency_base_combo.addItems(available_currencies)
        self.currency_base_combo.activated[str].connect(self.get_base_currency)

    def _setup_currency_code(self):
        self.currency_code_label = QLabel('Output currency', self)
        self.currency_code_combo = QComboBox(self)
        self.currency_code_combo.addItems(available_currencies)
        self.currency_code_combo.activated[str].connect(self.get_code_currency)

    def _setup_grid(self):
        self.grid.addWidget(self.currency_base_label, 0, 0)
        self.grid.addWidget(self.currency_base_combo, 0, 1)
        self.grid.addWidget(self.currency_code_label, 1, 0)
        self.grid.addWidget(self.currency_code_combo, 1, 1)
        self.grid.addWidget(self.get_currency_button, 2, 0)
        self.grid.addWidget(self.current_value, 2, 1)
        self.grid.addWidget(self.get_currency_forecast_button, 3, 0)
        self.grid.addWidget(self.predicted_value, 3, 1)
        self.grid.addWidget(self.server_url, 4, 0)
        self.grid.addWidget(self.server_port, 4, 1)

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.currency_base = self.currency_code = available_currencies[0]

        self._setup_currency_base()

        self._setup_currency_code()

        self.get_currency_button = QPushButton('Get currency', self)
        self.get_currency_button.clicked.connect(self.show_actual_currency)

        self.get_currency_forecast_button = QPushButton('Get currency forecast', self)
        self.get_currency_forecast_button.clicked.connect(self.show_currency_forecast)

        self.current_value = QLabel('', self)
        self.current_value.setObjectName('current_value')
        self.current_value.setStyleSheet('QLabel#current_value {border-style:solid; border-width:2px; border-color:green;}')

        self.predicted_value = QLabel('', self)
        self.predicted_value.setObjectName('predicted_value')
        self.predicted_value.setStyleSheet('QLabel#predicted_value {border-style:solid; border-width:2px; border-color:red;}')

        self.server_url = QLineEdit(SERVER_URL, self)
        self.server_port = QLineEdit(str(SERVER_PORT), self)
        self._setup_grid()

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())



