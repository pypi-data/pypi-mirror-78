import requests
import json

class Currency:
    def __init__(self):
        pass

    def validateCurrencyCode(self, ticker):
        data = requests.get(f'https://api.exchangeratesapi.io/latest?base={ticker}')

        data = self._convertByteToDictionary(data.content)
        if 'error' in data:
            return False, f'Ticker Symbol: "{ticker}" is invalid.'
        return True, data

    def _convertByteToDictionary(self, byteObject):
        return json.loads(byteObject.decode('ascii'))

    def convertCurrency(self, amount, ticker_og, ticker_new):
        validA, resultA = self.validateCurrencyCode(ticker_og)
        if not validA:
            return resultA

        validB, resultB = self.validateCurrencyCode(ticker_new)
        if not validB:
            return resultB

        return amount * resultA.get('rates').get(ticker_new)
