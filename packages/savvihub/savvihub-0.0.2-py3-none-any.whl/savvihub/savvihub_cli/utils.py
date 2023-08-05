import json
import os
import shutil

import typing
import yaml


def make_dir(path):
    if not os.path.exists(path):
        print(" [*] Make directories : {}".format(path))
        os.makedirs(path)


def remove_dir(path):
    if os.path.exists(path):
        print(" [*] Removed: {}".format(path))
        shutil.rmtree(path)


def write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)


def load_json(path):
    with open(path) as f:
        data = json.loads(f.read())
    return data


class AnnotatedObject:
    def __init__(self, d: dict):
        resolved_types = {}
        for cls in self.__class__.mro():
            annotations = getattr(cls, '__annotations__', None)
            if annotations is None:
                continue

            for k, type_ in annotations.items():
                if k in resolved_types:
                    continue

                v = d.get(k, None)
                resolved_types[k] = type_
                if v is None and not self._is_optional_type(type_):
                    # TODO: print warning
                    print(f'{k} is defined in {self.__class__.__name__} but not in {d}')
                    continue
                elif type_ == typing.Union and type(v) not in type_.__args__:
                    # TODO: print warning
                    print(f'{k} is defined in {self.__class__.__name__} but not in {d}')
                    continue
                elif type_ != type(v):
                    # TODO: print warning
                    print(f'{k} is defined in {self.__class__.__name__} as {type_} but {type(v)} in {d}')
                    continue
                if issubclass(type_, AnnotatedObject):
                    v = type_(v)
                setattr(self, k, v)
        self.d = d

    @staticmethod
    def _is_optional_type(type_):
        return typing.Union == type_.__origin__ and len(type_.__args__) == 2 and \
                type(None) == type_.__args__[1]

    def __str__(self):
        return f'[{self.__class__.__name__}] {self.d}'

    @property
    def dict(self):
        return self.d


def get_token_from_config(path):
    try:
        with open(path) as f:
            documents = yaml.full_load(f)
            if not documents:
                raise Exception('Nothing in config file')
            for item, doc in documents.items():
                if item != 'token':
                    raise Exception('No token item')
                elif not doc:
                    raise Exception('Token is not set! Run $savvi init')
                else:
                    return doc
    except EnvironmentError:
        print('Error: Config file not found')


def get_json_headers_with_token(token):
    try:
        authentication = 'token ' + token
    except TypeError:
        print('Token is not set!')
        return

    headers = {
        'Content-Type': 'application/json',
        'Authentication': authentication
    }

    return headers
