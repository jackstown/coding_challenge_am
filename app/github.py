from dataclasses import dataclass
from itertools import chain

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
        """
        Call to pull profile metadata from GitHub API
        """
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

        @property
        def topic_counts(self) -> dict:
            topics = list(chain.from_iterable([r.topics for r in self.repos if r.topics]))
            t_counts = dict()
            for topic in topics:
                t_counts[topic] = t_counts.get(topic, 0) + 1
            return t_counts


    @classmethod
    def call(cls, http_client: Client, request: Request, max_pages: int=10) -> Response:
        """
            Call to pull repo metadata from GitHub API
        """
        url = f'{cls.BASE_URL}/users/{request.org_name}/repos'
        results = list()
        for i in range(max_pages):  # Must paginate since api only returns 30 results max
            params = {'page': i+1}
            r = http_client.get(url=url, params=params)
            if not r.json():  # If no results, we have finished paginating
                break
            results += r.json()
        return cls.Response(results)
