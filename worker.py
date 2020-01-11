from datetime import datetime

import speedtest
from pymongo import MongoClient, DESCENDING
import settings


def size_scale(n_bytes):
    units = ['', 'k', 'm', 'g', 't']
    times = 0
    scaled_size = n_bytes + 0
    while times < len(units):
        if abs(scaled_size) < 1000:
            break
        scaled_size /= 1024
        times += 1

    return '{:.2f}{}bps'.format(scaled_size, units[times])


class SpeedtestResult:
    def __init__(self, data):
        if isinstance(data, speedtest.Speedtest):
            self._data = data.results.dict()
        else:
            self._data = data

        if data and isinstance(self._data['timestamp'], str):
            self._data['timestamp'] = datetime.strptime(self._data['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')

    def __str__(self):
        if self._data:
            return 'SpeedtestResult(D: {}/s, U: {}/s, P: {:.2f})'.format(
                size_scale(self._data['download']),
                size_scale(self._data['upload']),
                self._data['ping']
            )
        return 'SpeedtestResult(empty)'

    def __getattr__(self, item):
        if self._data and item in self._data:
            return self._data[item]
        return self.__getattr__(item)

    def __dict__(self):
        return self._data

    def save(self, collection):
        if not self._data:
            raise RuntimeError('Can\'t store an empty result!')
        collection.insert_one(self._data)


if __name__ == '__main__':
    print('connecting to db...')
    mongo_client = MongoClient(settings.DATABASE_URI)
    db = mongo_client.get_default_database()
    coll = db.get_collection('results')

    print('fetching last result...')
    last_one = SpeedtestResult(coll.find_one(sort=[('timestamp', DESCENDING)]))
    print(last_one)

    s = speedtest.Speedtest()
    s.get_servers([settings.SERVER_ID])

    print('download test... ', end='')
    s.download()
    print(size_scale(s.results.download) + '/s')
    print('upload test... ', end='')
    s.upload()
    print(size_scale(s.results.upload) + '/s')
    print('ping...', s.results.ping, 'ms')
    s.results.share()

    # print(s.results.dict())
    print('storing results...')
    result = SpeedtestResult(s)
    result.save(coll)

    if last_one is not None:
        up_diff = result.upload - last_one.upload
        dn_diff = result.download - last_one.download
        print('download diff: {}{} ({:.2f}%)'.format(
            ['', '+'][dn_diff >= 0],
            size_scale(dn_diff),
            (dn_diff / s.results.download)*100)
        )
        print('upload diff: {}{} ({:.2f}%)'.format(
            ['', '+'][up_diff >= 0],
            size_scale(up_diff),
            (up_diff / s.results.upload)*100)
        )
