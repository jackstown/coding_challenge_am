from importlib.resources import files

import httpx
import respx

from app.github import GHGetOrg
from tests.fixtures import TestFixture


class GithubTests(TestFixture):
    TEST_GITHUB_RESOURCES_PATH = files('tests._resources').joinpath('github')

    @respx.mock
    def test_get_user(self):
        mocked_repos_route = self.create_200_route(
            method='GET',
            url__eq='https://api.github.com/users/mailchimp',
            _json=self.get_resource_json('users.json', path=self.TEST_GITHUB_RESOURCES_PATH)
        )

        with httpx.Client() as client:
            request = GHGetOrg.Request(org_name='mailchimp')
            GHGetOrg.call(
                http_client=client,
                request=request
            )

        self.assertEqual(mocked_repos_route.call_count, 1)
