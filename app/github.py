from dataclasses import dataclass

from httpx import Client

class Repo:
    class Owner:
        def __init__(self, data):
            self.login = data['login']

    def __init__(self, data):
        self.fork = data['fork']
        self.forks_count = data['forks_count']

    @property
    def is_fork(self):
        return self.fork

class BaseApi:
    BASE_URL: str = "https://api.github.com"

class GetRepos(BaseApi):
    @dataclass
    class Request:
        org_name: str

    class Response:
        def __init__(self, data: dict):
            self.repos = [Repo(r) for r in data]

        @property
        def total_original_repos(self):
            return len([r for r in self.repos if not r.is_fork])

        @property
        def total_forked_repos(self):
            return sum([r.forks_count for r in self.repos if not r.is_fork])

    @classmethod
    def call(cls, http_client: Client, request: Request):
        url = f'{cls.BASE_URL}/users/{request.org_name}/repos'
        r = http_client.get(url).json()
        return cls.Response(r)
