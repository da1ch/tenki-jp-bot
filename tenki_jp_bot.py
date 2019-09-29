from requests.exceptions import Timeout
import requests
import lxml.html

class ForcastData:

    def __init__(self):
        self.weather = []
        self.temperature = []
        self.humidity = []
        self.wind_speed = []
        self.wind_direc = [] # wind direction
        self.precip = [] # precipitation
        self.precip_prob = [] # probability of precipitation


class OneHourForcast:

    _TABLES = [
            'today',
            'tomorrow',
            'overmorrow'
            ]

    _ATTRS = [
            'weather',
            'temperature',
            'humidity',
            'wind_speed',
            'wind_direc',
            'precip',
            'precip_prob'
            ]

    _TABLE2PATH = {
            _TABLES[0] : '/html/body/div[2]/table[1]',
            _TABLES[1] : '/html/body/div[2]/table[2]',
            _TABLES[2] : '/html/body/div[2]/table[3]'
            }

    _TABLEATTR2PATH = {
            _TABLES[0] : {
                _ATTRS[0] : '/tr[4]/td/p',
                _ATTRS[1] : '/tr[6]/td/span',
                _ATTRS[2] : '/tr[10]/td/span',
                _ATTRS[3] : '/tr[12]/td/span',
                _ATTRS[4] : '/tr[11]/td/p',
                _ATTRS[5] : '/tr[9]/td/span',
                _ATTRS[6] : '/tr[7]/td/span'
                },
            _TABLES[1] : {
                _ATTRS[0] : '/tr[4]/td/p',
                _ATTRS[1] : '/tr[6]/td/span',
                _ATTRS[2] : '/tr[10]/td',
                _ATTRS[3] : '/tr[12]/td/span',
                _ATTRS[4] : '/tr[11]/td/p/span',
                _ATTRS[5] : '/tr[9]/td/span',
                _ATTRS[6] : '/tr[7]/td/span'
                },
            _TABLES[2] : {
                _ATTRS[0] : '/tr[4]/td/p',
                _ATTRS[1] : '/tr[6]/td/span',
                _ATTRS[2] : '/tr[10]/td',
                _ATTRS[3] : '/tr[12]/td/span',
                _ATTRS[4] : '/tr[11]/td/p/span',
                _ATTRS[5] : '/tr[9]/td/span',
                _ATTRS[6] : '/tr[7]/td/span'
                }
            }

    def __init__(self):
        self.today = ForcastData()
        self.tomorrow = ForcastData()
        self.overmorrow = ForcastData()
        self.successful = False

    def _address2url(self, address, timeout = 6.0):
        req = 'https://tenki.jp/search/?keyword=' + address
        try: page = requests.get(req, timeout = timeout)
        except Timeout: return ''
        html = lxml.html.fromstring(page.text)
        results = html.xpath('/html/body/div[2]/section/section[1]/div[2]/p/a')
        if len(results) == 1: return 'https://tenki.jp' + results[0].get('href')
        else: return ''

    def _parse_1hour_forcast_table(self, html, table, out):
        table_path = OneHourForcast._TABLE2PATH[table]
        for attr in OneHourForcast._ATTRS: 
            path = table_path + OneHourForcast._TABLEATTR2PATH[table][attr]
            for tag in html.xpath(path):
                # Save a parsed data into a ForcastData object.
                getattr(out, attr).append(tag.text)

    def _parse_1hour_forcast_page(self, html):
        for table in OneHourForcast._TABLES:
            out = getattr(self, table)
            self._parse_1hour_forcast_table(html, table, out) 

    def fetch(self, address, timeout = 6.0):
        url = self._address2url(address, timeout)
        if not url: 
            self.successful = False
            return
        url += '1hour.html'
        try: page = requests.get(url, timeout = timeout)
        except Timeout: 
            self.successful = False
            return
        html = lxml.html.fromstring(page.text)
        self._parse_1hour_forcast_page(html)
        self.successful = True

