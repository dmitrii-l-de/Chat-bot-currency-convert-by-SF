import json
from config import keys
import requests

class ConvertionExeption(Exception):
    pass


class CriptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionExeption('unable to convert the same currencies')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExeption('The currency is unexpected. Try to fix the error.')

        try:
            base_ticket = keys[base]
        except KeyError:
            raise ConvertionExeption('The currency is unexpected. Try to fix the error.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption('Сonvertion amount must be a number')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticket}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base