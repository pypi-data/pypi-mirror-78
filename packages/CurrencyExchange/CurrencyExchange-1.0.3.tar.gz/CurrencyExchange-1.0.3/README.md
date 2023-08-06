# CurrencyExchange

Currency Exchange is a Python package that allows your to verify whether a currency code (such as `USD`) is valid. In addition, it allows you to convert currency amounts to various other currecies. 

# How to use

```
import CurrencyExchange

currency = CurrencyExchange.Currency()

currency.convertCurrency(1, 'USD', 'EUR') # Convert 1 USD to 1 EUR
"""
This returns:
0.8485362749
"""

currency.validateCurrencyCode('USD') # Check to see if USD is a valid currency code
"""
This returns: 
(True, {'rates': {'CAD': 1.3171828596, 'HKD': 7.7503606279, 'ISK': 140.2630462452, 'PHP': 48.6491302503, 'DKK': 6.3137038608, 'HUF': 306.6355536699, 'CZK': 22.5040305473, 'GBP': 0.7675265168, 'RON': 4.123462028, 'SEK': 8.8022910479, 'IDR': 14860.033941451, 'INR': 73.9126007637, 'BRL': 5.382011031, 'RUB': 76.386338566, 'HRK': 6.392023759, 'JPY': 106.2367416207, 'THB': 31.4654221468, 'CHF': 0.9181162495, 'EUR': 0.8485362749, 'MYR': 4.1685193042, 'BGN': 1.6595672465, 'TRY': 7.4842596521, 'CNY': 6.8441238863, 'NOK': 9.0549851506, 'NZD': 1.5037759864, 'ZAR': 16.9735256682, 'USD': 1.0, 'MXN': 21.8655070004, 'SGD': 1.3703012304, 'AUD': 1.3819261773, 'ILS': 3.3919389054, 'KRW': 1189.7666525244, 'PLN': 3.7745439118}, 'base': 'USD', 'date': '2020-09-08'})
"""
```

