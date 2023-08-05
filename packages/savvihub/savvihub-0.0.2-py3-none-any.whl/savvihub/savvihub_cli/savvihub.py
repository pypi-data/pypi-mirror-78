import grequests
import requests
import typing

from savvihub.savvihub_cli.constants import HOST_URL
from savvihub.savvihub_cli.utils import AnnotatedObject


class SavviDatasetFile(AnnotatedObject):
    path: str
    is_dir: bool

    size: int
    hash: str

    download_url: str
    upload_url: str


class PaginatedMixin(AnnotatedObject):
    total: int
    startCursor: str
    endCursor: str
    results: typing.List


class SavviHubPaginatedDatasetFilesResponse(PaginatedMixin, AnnotatedObject):
    results: typing.List[SavviDatasetFile]


class SavviHubClient:
    def __init__(self, token, url=HOST_URL, multi=False):
        self.url = url
        self.token = token
        self.headers = {
            'content-type': 'application/json',
        }
        self.api = requests
        if multi:
            self.api = grequests

    def raise_for_status(self, r):
        if r.status_code != 200:
            print(r.text)
            r.raise_for_status()

    def get(self, url, params=None, raw=False):
        r = self.api.get(f'{self.url}{url}', headers=self.headers, params=params)
        self.raise_for_status(r)
        if raw:
            return r.text
        else:
            return r.json()

    def get_all(self, url, params=None):
        raw_resp = self.get(url, params=params)
        resp = PaginatedMixin(raw_resp)
        results = []

        fetched_items = 0
        while True:
            fetched_items += len(resp.results)
            results.extend(resp.results)
            if fetched_items >= resp.total:
                break
            raw_resp = self.get(url, params={**params, 'after': resp.endCursor})
            resp = PaginatedMixin(raw_resp)
        return results

    def post(self, url, data):
        r = self.api.post(f'{self.url}{url}', json=data, headers=self.headers)
        self.raise_for_status(r)
        return r.json()

    def delete(self, url):
        r = self.api.delete(f'{self.url}{url}', headers=self.headers)
        self.raise_for_status(r)
        return r.json()

    def patch(self, url, data):
        r = self.api.patch(f'{self.url}{url}', json=data, headers=self.headers)
        self.raise_for_status(r)
        return r.json()

    def dataset_file_list(self, workspace, dataset, *, ref='latest') -> typing.List[SavviDatasetFile]:
        results = self.get_all(f'/api/workspaces/{workspace}/datasets/{dataset}/files/', params={'ref': ref})
        return [SavviDatasetFile(x) for x in results]

    def dataset_file_create(self, workspace, dataset, path, is_dir):
        r = self.post(f'/api/workspaces/{workspace}/datasets/{dataset}/files/', {
            'path': path,
            'is_dir': is_dir
        })
        return SavviDatasetFile(r)
