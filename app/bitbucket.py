from dataclasses import dataclass

from httpx import Client


class Repo:
    def __init__(self, data):
        self.full_name = data['full_name']
        self.language = data['language']
        self.parent = data['parent']
        self.type = data['type']

    @property
    def is_fork(self):
        return self.parent is not None


class BaseApi:
    BASE_URL: str = 'https://api.bitbucket.org/2.0'
    MAX_PAGES: int = 10

class BBGetRepos(BaseApi):
    @dataclass
    class Request:
        username: str

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
        def language_counts(self) -> dict:
            languages = [r.language for r in self.repos]
            l_counts = dict()
            for lang in languages:
                l_counts[lang] = l_counts.get(lang, 0) + 1
            return l_counts

    @classmethod
    def call(cls, http_client: Client, request: Request) -> Response:
        """
        Call to pull repositories metadata from Bitbucket API
        """
        url = f'{cls.BASE_URL}/repositories/{request.username}'
        results = list()

        for i in range(cls.MAX_PAGES):  # Must paginate since api only returns 30 results max
            params = {'page': i+1}
            r = http_client.get(url=url, params=params)
            vals = r.json().get('values')
            if not vals:  # If no results, we have finished paginating
                break
            results += vals

        return cls.Response(results)

class BBGetUser(BaseApi):
    @dataclass
    class Request:
        username: str

    class Response:
        def __init__(self, data: dict):
            self.login = data['login']
            self.followers = data['followers']

    @classmethod
    def call(cls, http_client: Client, request: Request) -> Response:
        """
        Call to pull profile metadata from Bitbucket API
        """
        url = f'{cls.BASE_URL}/users/{request.username}'
        r = http_client.get(url=url)
        return cls.Response(r.json())