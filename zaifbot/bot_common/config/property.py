class System:
    def __init__(self, sleep_time='1m', currency_pair='btc_jpy', retry_count=5):
        self._system = {'sleep_time': sleep_time, 'currency_pair': currency_pair, 'retry_count': retry_count}

    @property
    def sleep_time(self):
        return self._system['sleep_time']

    @sleep_time.setter
    def sleep_time(self, time):
        self._system['sleep_time'] = time

    @property
    def currency_pair(self):
        return self._system['currency_pair']

    @currency_pair.setter
    def currency_pair(self, pair):
        self._system['currency_pair'] = pair

    @property
    def retry_count(self):
        return self._system['retry_count']

    @retry_count.setter
    def retry_count(self, count):
        self._system['retry_count'] = count