import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


class Singleton(type):
    def __init__(cls, name, bases, dict_):
        super().__init__(name, bases, dict_)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kwargs)
        return cls.instance


class DataListIterator:
    def __init__(self, data):
        self.values = (data[key] for key in sorted(data))

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.values)


class DataList:
    _data_path: Path
    _object_class: Any

    def __init__(self):
        with open(self._data_path) as file:
            data = json.load(file)

        self._data = {}
        for key, value in data.items():
            obj = self._object_class(**value)
            self._data[key] = obj
            setattr(self, key, obj)

    def __str__(self):
        return f"{self.__class__.__name__}()"

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return DataListIterator(self._data)


@dataclass(frozen=True, order=True)
class Country:
    english_name: str
    french_name: str
    alpha_2_code: str
    alpha_3_code: str
    numeric_code: int


class Countries(DataList, metaclass=Singleton):
    _data_path = Path(__file__).parent.joinpath("_data/country.json")
    _object_class = Country


@dataclass(frozen=True, order=True)
class Currency:
    code: str
    name: str
    entities: list
    numeric_code: int
    minor_units: Optional[int]


class Currencies(DataList, metaclass=Singleton):
    _data_path = Path(__file__).parent.joinpath("_data/currency.json")
    _object_class = Currency
