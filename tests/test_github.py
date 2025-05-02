from importlib.resources import files

import httpx
import respx

from app.github import GHGetOrg, GHGetRepos
from tests.fixtures import TestFixture


class GithubTests(TestFixture):
    TEST_GITHUB_RESOURCES_PATH = files('tests._resources').joinpath('github')

    @respx.mock
    def test_get_repos(self):
        mocked_repos_page_1_route = self.create_200_route(
            method='GET',
            url__eq='https://api.github.com/users/mailchimp/repos?page=1',
            _json=self.get_resource_json('repos.json', path=self.TEST_GITHUB_RESOURCES_PATH)
        )

        with httpx.Client(verify=self.SSL_CONTEXT) as client:
            request = GHGetRepos.Request(org_name='mailchimp')
            response = GHGetRepos.call(
                http_client=client,
                request=request,
                max_pages=1,
            )

        repo_5 = response.repos[4]
        self.assertFalse(repo_5.fork)
        self.assertEqual(repo_5.forks_count, 236)
        self.assertEqual(repo_5.language, 'None')
        self.assertListEqual(repo_5.topics, [])
        self.assertFalse(repo_5.is_fork)

        self.assertEqual(response.total_original_repos, 26)
        self.assertEqual(response.total_forked_repos, 4)
        self.assertEqual(response.total_forks_count, 3771)
        self.assertDictEqual(
            response.language_counts,
            {
                'CSS': 1,
                'Java': 1,
                'JavaScript': 4,
                'Kotlin': 1,
                'Mustache': 1,
                'None': 2,
                'Objective-C': 2,
                'PHP': 8,
                'Python': 3,
                'Ruby': 6,
                'Swift': 1
            }
        )
        self.assertDictEqual(
            response.topic_counts,
            {
                'android-sdk': 1,
                'ecommerce': 2,
                'email-marketing': 2,
                'ios-sdk': 1,
                'kotlin': 1,
                'magento': 2,
                'magento2': 1,
                'mailchimp': 11,
                'mailchimp-api': 5,
                'mailchimp-api-v3': 5,
                'mailchimp-api-wrapper': 5,
                'mailchimp-php': 1,
                'mailchimp-sdk': 11,
                'mandrill': 4,
                'mandrill-api': 4,
                'mandrill-api-wrapper': 4,
                'mandrill-node': 1,
                'node': 1,
                'nodejs': 2,
                'php': 3,
                'python': 2,
                'ruby': 2,
                'sdk': 2,
                'sdk-android': 1,
                'sdk-ios': 1,
                'swift': 1
            }
        )

        self.assertEqual(mocked_repos_page_1_route.call_count, 1)

    @respx.mock
    def test_get_user(self):
        mocked_repos_route = self.create_200_route(
            method='GET',
            url__eq='https://api.github.com/users/mailchimp',
            _json=self.get_resource_json('users.json', path=self.TEST_GITHUB_RESOURCES_PATH)
        )

        with httpx.Client(verify=self.SSL_CONTEXT) as client:
            request = GHGetOrg.Request(org_name='mailchimp')
            response = GHGetOrg.call(
                http_client=client,
                request=request
            )

        self.assertEqual(response.followers, 112)

        self.assertEqual(response.login, 'mailchimp')

        self.assertEqual(mocked_repos_route.call_count, 1)
