from importlib.resources import files

import httpx
import respx

from app.bitbucket import BBGetRepos
from tests.fixtures import TestFixture


class BitbucketTests(TestFixture):
    TEST_BITBUCKET_RESOURCES_PATH = files('tests._resources').joinpath('bitbucket')

    @respx.mock
    def test_get_repos(self):
        mocked_repos_page_1_route = self.create_200_route(
            method='GET',
            url__eq='https://api.bitbucket.org/2.0/repositories/mailchimp?page=1',
            _json=self.get_resource_json('repos.json', path=self.TEST_BITBUCKET_RESOURCES_PATH)
        )

        with httpx.Client(verify=self.SSL_CONTEXT) as client:
            request = BBGetRepos.Request(username='mailchimp')
            response = BBGetRepos.call(
                http_client=client,
                request=request,
                max_pages=1,
            )

        repo_5 = response.repos[4]
        self.assertEqual(repo_5.language, 'javascript')
        self.assertFalse(repo_5.is_fork)

        self.assertEqual(response.total_original_repos, 10)
        self.assertEqual(response.total_forked_repos, 0)
        self.assertDictEqual(
            response.language_counts,
            {
                'dart': 1,
                'javascript': 3,
                'php': 2,
                'python': 2,
                'ruby': 2
            }
        )

        self.assertEqual(mocked_repos_page_1_route.call_count, 1)
