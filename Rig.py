import json
import re
import locale


class Rig(object):
    locale.setlocale(locale.LC_ALL, '')

    def __init__(self, *args, **kwargs):
        self.coins = []

        data = kwargs['data']
        self.id = data['id']
        self.name = data['name']
        if 'miners_summary' in data.keys():
            self.miners_summary = data['miners_summary']
            self.parse_coins(data['miners_summary']['hashrates'])
        self.stats = data['stats']

    def parse_coins(self, coin_data):
        for c in coin_data:
            if 'algo' in c.keys():
                tmp_coin = self.Coin(c)
                self.coins.append(tmp_coin)

    def get_coins(self):
        s = ""
        for c in self.coins:
            s = s + " Algo: {}, Hashrate: {}".format(c.algo, c.hashrate)
        return s

    def __repr__(self):
        return repr(f'Name: {self.name} Coins: {self.get_coins()} ')

    class Coin(object):

        @staticmethod
        def parse_size(size):
            pass

        def determine_hash_string(self):
            units = {"Khs": 2 ** 10, "Mhs": 2 ** 20, "Ghs": 2 ** 30, "Ths": 2 ** 40}

            if self.hashrate <= units['Khs']:
                self.units = 'Khs'

            elif self.hashrate <= units['Mhs']:
                self.units = "Mhs"

            elif self.hashrate <= units['Ghs']:
                self.units = "Ghs"

            elif self.hashrate <= units['Ths']:
                self.units = "Ths"

        def __init__(self, coin_data):
            try:
                self.algo = coin_data['algo']
                self.hashrate = coin_data['hash']
                self.friendly_hash = locale.format("%d", coin_data['hash'], grouping=True)
                self.units = ""
                self.determine_hash_string()
            except KeyError:
                print(f'Invalid Data, skipping')

        @property
        def hash_rate(self):
            return

        @hash_rate.setter
        def hash_rate(self, value):
            if len(value['hash'] == 6):
                pass

        def __repr__(self):
            return repr(f'Algo: {self.algo}  ')
