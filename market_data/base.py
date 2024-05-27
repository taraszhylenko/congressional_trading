import yfinance as yfi

class TickerPrice:
    def __init__(self, ticker):
        self.ticker = ticker
        self.yfi_ticker = yfi.Ticker(ticker)
        self.price_history = self.yfi_ticker.history(
                                 period='max'
                             ).reset_index(
                             ).assign(
                                     date_str = lambda df: df['Date'].apply(lambda x: x.strftime('%Y%m%d'))
                             )

    def get_price(self, date):
        assert isinstance(date, str)
        assert int(date) > int(self.price_history.date_str.tolist()[0]), f"Don't have price: earlier than available in yfinance"
        assert date in self.price_history.date_str.tolist(), f"Don't have price: weekend or holiday"
        return float(self.price_history[self.price_history.date_str == date].Close.tolist()[0])
