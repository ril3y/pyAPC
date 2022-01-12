import urllib3
import json
import time
from Rig import Rig


class PyHive(object):
    def __init__(self, api_key):
        self.data = ""
        self.headers = {"Content-Type": "application/json"}
        self.url = "https://api2.hiveos.farm/api/v2"
        self.api_key = api_key
        self.connection = urllib3.PoolManager()
        self.farm_ids = []
        self.farm_count = 0
        self.authenticated = False
        self.rigs = []
        self._run = False
        self.get_workers_stats()

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value
        self.headers['Authorization'] = "Bearer " + value

    def _add_farm_id(self, id):
        if id not in self.farm_ids:
            self.farm_ids.append(id)
            self.farm_count += 1

    def post(self, url):
        if self.api_key is None:
            raise

    def call_api(self, query_string, method="GET"):
        return self.connection.request(
            method,
            self.url + query_string,
            headers=self.headers)

    def get_farms(self):
        if self.api_key is not None:
            response = self.call_api("/farms")
            self.data = json.loads(response.data.decode('utf-8'))

            if "message" in self.data.keys():
                print("Unauthenticated")
                return
            else:
                self.authenticated = True
                for id in self.data['data']:
                    self._add_farm_id(id['id'])

    def _is_rig_in_rigs(self, name: str):
        for _rig in self.rigs:
            if _rig.name == name:
                return _rig
        return False

    def check_workers_offline(self):
        self.get_workers_stats()
        _offline_workers = []
        for rig in self.rigs:
            if not rig.stats['online']:
                # Worker is offline
                _offline_workers.append(rig)
        return _offline_workers

    def get_workers_stats(self):
        if self.data == "":
            self.get_farms()
        if self.authenticated:
            for farm_id in self.farm_ids:
                response = self.call_api("/farms/{}/workers?platform=1".format(farm_id))
                try:
                    self.data = json.loads(response.data.decode('utf-8'))
                except:
                    print("Error loading json data")
                    continue
                if 'data' in self.data.keys():
                    for rig in self.data['data']:
                        _rig = self._is_rig_in_rigs(rig['name'])
                        if _rig is False:
                            r = Rig(data=rig)
                            self.rigs.append(r)
                        else:
                            # We know about this rig already, we will not update the information on it.
                            self.rigs.remove(_rig)
                            r = Rig(data=rig)
                            self.rigs.append(r)

    def print_data(self):
        for rig in self.rigs:
            print('------------------------------------------')
            print(f'Rig Name: {rig.name}')

            for c in rig.coins:
                print(f'Coin: {c.algo} : Hashrate {c.friendly_hash}')
            print('------------------------------------------')


if __name__ == "__main__":
    with open("hive_api_key.txt", "r") as f:
        api_key = f.read()

    p = PyHive(api_key)
    p.get_workers_stats()
    print("Done")
