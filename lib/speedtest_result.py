from datetime import datetime

import speedtest
from pymongo import DESCENDING

from lib.common import size_scale, get_database


class SpeedtestResult:
    def __init__(self, data):
        if isinstance(data, speedtest.Speedtest):
            self._data = data.results.dict()
        else:
            self._data = data or {}

        if data and isinstance(self._data['timestamp'], str):
            self._data['timestamp'] = datetime.strptime(self._data['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')

        self._data = {
            **self._data,
            'download_human': None if not self._data else size_scale(self._data['download']),
            'download_diff': None,
            'download_diff_human': None,
            'download_diff_p': 0,
            'upload_human': None if not self._data else size_scale(self._data['upload']),
            'upload_diff': None,
            'upload_diff_human': 0,
            'upload_diff_p': 0,
        }

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
        return super().__getattr__(item)

    @property
    def data(self):
        data_copy = {**self._data}
        del data_copy['_id']
        return data_copy

    def save(self):
        if not self._data:
            raise RuntimeError('Can\'t store an empty result!')
        self.__class__.get_collection().insert_one(self._data)

    def add_comparison(self, other):
        up_diff = self.upload - other.upload
        dn_diff = self.download - other.download

        self._data['download_diff'] = dn_diff
        self._data['download_diff_human'] = ['', '+'][dn_diff >= 0] + size_scale(dn_diff)
        self._data['download_diff_p'] = (dn_diff / self.download) * 100
        self._data['upload_diff'] = up_diff
        self._data['upload_diff_human'] = ['', '+'][up_diff >= 0] + size_scale(up_diff)
        self._data['upload_diff_p'] = (up_diff / self.upload) * 100

    __collection = None

    @classmethod
    def get_collection(cls):
        if cls.__collection is None:
            cls.__collection = get_database().get_collection('results')
        return cls.__collection

    @classmethod
    def get_last(cls):
        col = cls.get_collection()
        return cls(col.find_one(sort=[('timestamp', DESCENDING)]))

    @classmethod
    def get(cls, limit=10, raw=False):
        col = cls.get_collection()
        result = col.find(limit=limit).sort('timestamp', DESCENDING)
        return result if raw else [cls(i) for i in result]
