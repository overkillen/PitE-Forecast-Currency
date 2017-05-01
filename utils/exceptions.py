class ForecastingError(Exception):
    pass


class DataPullError(ForecastingError):
    pass


class InvalidInput(ForecastingError):
    pass

