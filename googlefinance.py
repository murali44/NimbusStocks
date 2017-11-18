from urllib import urlopen
import json, time


class Utils(object):
    @staticmethod
    def request(symbol):
        try:
            url = 'https://finance.google.com/finance?client=ig&output=json&q='
            request = url + symbol
            content = urlopen(request).read().decode('ascii', 'ignore').strip()
            content = content[3:]
            content = json.loads(content)
            return content
        except Exception as e:
            print e
            return False

    @staticmethod
    def get_value(content, key):
        return content[0][key]


class Stock(object):
    def __init__(self, symbol):
        data = Utils.request(symbol)
        if data is False:
            raise Exception
        self.symbol = Utils.get_value(data, 't')
        self.id = Utils.get_value(data, 'id')
        self.exchange = Utils.get_value(data, 'e')
        self.name = Utils.get_value(data, 'name')
        #self.type = Utils.get_value(data, 'type')
        self.percentagechange = Utils.get_value(data, 'cp')
        self.price = Utils.get_value(data, 'l')
