from dataclasses import dataclass

from httpx import Client


class Repo:
    class Owner:
        def __init__(self, data):
            self.login = data['login']

    def __init__(self, data):
        self.fork = data['fork']
        self.forks_count = data['forks_count']
        self.language = data['language'] or 'None'
        self.topics = data['topics']

    @property
    def is_fork(self):
        return self.fork

class BaseApi:
    BASE_URL: str = "https://api.github.com"
    MAX_PAGES: int = 10


class GHGetOrg(BaseApi):
    @dataclass
    class Request:
        org_name: str

    class Response:
        def __init__(self, data: dict):
            self.login = data['login']
            self.followers = data['followers']

    @classmethod
    def call(cls, http_client: Client, request: Request) -> Response:
        url = f'{cls.BASE_URL}/users/{request.org_name}'
        r = http_client.get(url=url)
        return cls.Response(r.json())


class GHGetRepos(BaseApi):
    @dataclass
    class Request:
        org_name: str

    class Response:
        def __init__(self, data: dict):
            self.repos = [Repo(r) for r in data]

        @property
        def total_original_repos(self) -> int:
            return len([r for r in self.repos if not r.is_fork])

        @property
        def total_forked_repos(self) -> int:
            return len([r for r in self.repos if r.is_fork])

        @property
        def total_forks_count(self) -> int:
            return sum([r.forks_count for r in self.repos if not r.is_fork])

        @property
        def language_counts(self) -> dict:
            languages = [r.language for r in self.repos]
            l_counts = dict()
            for lang in languages:
                l_counts[lang] = l_counts.get(lang, 0) + 1
            return l_counts

    @classmethod
    def call(cls, http_client: Client, request: Request) -> Response:
        url = f'{cls.BASE_URL}/users/{request.org_name}/repos'
        results = list()
        for i in range(cls.MAX_PAGES):
            params = {'page': i+1}
            r = http_client.get(url=url, params=params)
            if not r.json():  # If no results, we have finished paginating
                break
            results += r.json()
        return cls.Response(results)
