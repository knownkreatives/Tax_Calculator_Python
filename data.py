MAX_INCOME = 1e9

class TaxBracket:
    def __init__(self, symbol_currency: str, percent_rate: float, low_threshold = 0, high_threshold = MAX_INCOME):
        self.symbol_currency = symbol_currency
        self.percent_rate = percent_rate
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold

class TaxSystem:
    def __init__(self, name: str, available_brackets: list[TaxBracket]):
        self.name = name
        self.available_brackets = available_brackets