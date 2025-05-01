import dataclasses
from dataclasses import dataclass

import httpx

from app.bitbucket import BBGetRepos
from app.github import GHGetRepos, GHGetOrg


class GetRepos:
    @dataclass
    class Response:
        @dataclass
        class Service:
            original_repos: int
            forked_repos: int
            repo_language_counts: dict
            repo_topic_counts: dict

        org_name: str
        github: Service
        bitbucket: Service

        def to_dict(self):
            return dataclasses.asdict(self)

    @classmethod
    def call(cls, org_name: str):

        with httpx.Client() as client:
            gh_req = GHGetRepos.Request(org_name=org_name)
            r_gh = GHGetRepos.call(http_client=client, request=gh_req)

            bb_req = BBGetRepos.Request(username=org_name)
            r_bb = BBGetRepos.call(http_client=client, request=bb_req)

            return cls.Response(
                org_name=org_name,
                github=cls.Response.Service(
                    original_repos=r_gh.total_original_repos,
                    forked_repos=r_gh.total_forked_repos,
                    repo_language_counts=r_gh.language_counts,
                    repo_topic_counts=r_gh.topic_counts,
                ),
                bitbucket=cls.Response.Service(
                    original_repos=r_bb.total_original_repos,
                    forked_repos=r_bb.total_forked_repos,
                    repo_language_counts=r_bb.language_counts,
                    repo_topic_counts=dict(),  # Topics don't exist in BitBucket
                )
            )

class GetFollowers:
    @dataclass
    class Response:

        @dataclass()
        class Service:
            followers: int

        org_name: str
        bitbucket: Service
        github: Service

        def to_dict(self):
            return dataclasses.asdict(self)

    @classmethod
    def call(cls, org_name: str):
        req = GHGetOrg.Request(org_name=org_name)
        with httpx.Client() as client:
            r_gh = GHGetOrg.call(http_client=client, request=req)
            return cls.Response(
                org_name=org_name,
                bitbucket=cls.Response.Service(
                    followers=0,  # Total follows count doesn't exist. #TODO Can fan out repo watchers, paginate each one, and sum them together
                ),
                github=cls.Response.Service(
                    followers=r_gh.followers,
                ),
            )
