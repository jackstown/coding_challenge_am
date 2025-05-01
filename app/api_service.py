import dataclasses
from dataclasses import dataclass

import httpx

from app.github import GHGetRepos, GHGetOrg


class GetRepos:
    @dataclass
    class Response:
        @dataclass
        class Github:
            original_repos: int
            forked_repos: int
            repo_language_counts: dict
            repo_topic_counts: dict

        org_name: str
        github: Github

        def to_dict(self):
            return dataclasses.asdict(self)

    @classmethod
    def call(cls, org_name: str):
        req = GHGetRepos.Request(org_name=org_name)
        with httpx.Client() as client:
            r_gh = GHGetRepos.call(http_client=client, request=req)
            return cls.Response(
                org_name=org_name,
                github=cls.Response.Github(
                    original_repos=r_gh.total_original_repos,
                    forked_repos=r_gh.total_forked_repos,
                    repo_language_counts=r_gh.language_counts,
                    repo_topic_counts=r_gh.topic_counts,
                )
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
