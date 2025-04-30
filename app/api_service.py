import dataclasses
from dataclasses import dataclass

import httpx

from app.github import GHGetRepos, GHGetOrg


class GetRepos:
    @dataclass
    class Response:
        org_name: str
        github_original_repos: int
        github_forked_repos: int
        github_repo_language_counts: dict

        def to_dict(self):
            return dataclasses.asdict(self)

    @classmethod
    def call(cls, org_name: str):
        req = GHGetRepos.Request(org_name=org_name)
        with httpx.Client() as client:
            r_gh = GHGetRepos.call(http_client=client, request=req)
            return cls.Response(
                org_name=org_name,
                github_original_repos=r_gh.total_original_repos,
                github_forked_repos=r_gh.total_forked_repos,
                github_repo_language_counts=r_gh.language_counts
            )

class GetFollowers:
    @dataclass
    class Response:

        @dataclass()
        class Github:
            followers: int

        org_name: str
        github: Github

        def to_dict(self):
            return dataclasses.asdict(self)

    @classmethod
    def call(cls, org_name: str):
        req = GHGetOrg.Request(org_name=org_name)
        with httpx.Client() as client:
            r_gh = GHGetOrg.call(http_client=client, request=req)
            return cls.Response(
                org_name=org_name,
                github=cls.Response.Github(
                    followers=r_gh.followers,
                )
            )
