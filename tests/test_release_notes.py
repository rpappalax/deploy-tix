import unittest
import requests
import json
from mock import Mock, MagicMock, patch
from urlparse import urlparse
from deploy_tix.release_notes import ReleaseNotes


HOST_GITHUB = 'github.com'
HOST_GITHUB_RAW = 'raw.githubusercontent.com'
MOCK_MAX_COMPARISONS_TO_SHOW = 4
MOCK_REPO_OWNER = 'mozilla-services'
MOCK_REPO = 'shavar'
MOCK_ENV = 'STAGE'
ACCESS_TOKEN = 'xxxxxxxxxx'


def url_mock(url_remote):
    url_parsed = urlparse(url_remote)
    # path_remote = '{0}://{1}{2}'.format(
    #     url_parsed.scheme,
    #     url_parsed.netloc,
    #     url_parsed.path
    # )
    return '{0}/{1}{2}'.format(
        # 'deploy_tix/tests/mocks',
        'tests/mocks',
        url_parsed.netloc,
        url_parsed.path
    )


def mock_fixture(path_local):
    # path_local = url_mock(url_remote)
    with open(path_local) as f:
        mock_data = f.read()
    return mock_data


class ReleaseNotesTestCase(unittest.TestCase):
    """Tests for `release_notes.py`."""

    def setUp(self):
        self._mock_rel_notes = ReleaseNotes(
            repo_owner=MOCK_REPO_OWNER,
            repo=MOCK_REPO,
            environment=MOCK_ENV
        )
        #
        # self._token_string = self._mock_rel_notes._get_token_string(ACCESS_TOKEN)
        # self.url_github = self._mock_rel_notes._url_github(
        #     HOST_GITHUB, MOCK_REPO_OWNER, MOCK_REPO)
        # self.url_github_api = self._mock_rel_notes._url_github_api(
        #     HOST_GITHUB, MOCK_REPO_OWNER, MOCK_REPO)

        # req = self._get_tags(url)
        # self._tags = req.json()
        # self._max_comparisons = self._get_max_comparisons(self._tags)
        # self._latest_tags = self._get_latest_tags()
        # self._last_tag = self._get_last_tag()
        # self._last_tag_version = self._last_tag[VERS]

    def test_get_last_tag(self):

        # print self._mock_rel_notes._get_last_tag.return_value

        pass

    def test_get_token_string(self):

        token_string_match = '?access_token=XXXXXXXX'
        token_string = self._mock_rel_notes._get_token_string('XXXXXXXX')
        self.assertTrue(token_string == token_string_match,
                        'Token string path is incorrect')

    def test_get_url_github(self):

        url_match = 'https://HOST/REPO-OWNER/REPO'
        url = self._mock_rel_notes._get_url_github('HOST', 'REPO-OWNER', 'REPO')
        self.assertTrue(url == url_match, 'URL github is incorrect')

    def test_get_url_github_api(self):

        # url_match = 'https://api.github.com/repos/mozilla-services/shavar/git'

        url_match = 'https://api.HOST/repos/REPO-OWNER/REPO/git'
        url = self._mock_rel_notes._get_url_github_api(
            'HOST', 'REPO-OWNER', 'REPO')
        self.assertTrue(url == url_match, 'URL github API is incorrect')

    def test_get_url_github_api_tags(self):

        # url_match = 'https://api.github.com/repos/mozilla-services/shavar/' \
        #     'git/refs/tags?access_token=xxxxxxxxxx'

        url_match = 'HTTPS://HOST-URL/refs/tags?ACCESS_TOKEN=XXXXXXXX'
        url = self._mock_rel_notes._get_url_github_api_tags(
            'HTTPS://HOST-URL',
            '?ACCESS_TOKEN=XXXXXXXX'
        )
        self.assertTrue(url == url_match,
                        'URL for github API tags is incorrect')

    def test_get_url_changelog(self):

        url_match = 'HTTPS://HOST/COMMIT-SHA-HERE/CHANGELOG.RST'
        url = self._mock_rel_notes._get_url_changelog(
            'HTTPS://HOST',
            'COMMIT-SHA-HERE',
            'CHANGELOG.RST'
        )
        self.assertTrue(url == url_match, 'URL for CHANGELOG is incorrect')

    # @mock.patch('deploy_tix.release_notes', 'MAX_COMPARISONS_TO_SHOW=4')
    def test_get_max_comparisons(self):
        failure_msg = 'max_comparisons should be <= tags length'
        tags_list = [[0, 1, 2, 3],
                     [0, 1, 2, 3, 4],
                     [0, 1, 2, 3, 4, 5]]
        for tags in tags_list:
            result = self._mock_rel_notes._get_max_comparisons(tags)
            self.assertTrue(result >= 4, failure_msg)

        tags_list = [[0],
                     [0, 1],
                     [0, 1, 2],
                     [0, 1, 2, 3]]
        for tags in tags_list:
            result = self._mock_rel_notes._get_max_comparisons(tags)
            self.assertTrue(result == len(tags), failure_msg)

    def test_get_tags(self):

        url =  'https://api.github.com/repos/mozilla-services/shavar/git/refs/tags?access_token=xxxxxxxx'
        path_local = url_mock(url)
        mock_data = mock_fixture(path_local)

        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = mock_data
            tags = self._mock_rel_notes._get_tags(url)
            self.assertNotEqual(tags, None)
            self.assertEqual(tags.text, mock_data)

    def test_parse_tag(self):
        parsed_tag_match = [
            u'0.1',
            u'1c4cff1014a869fd4c50b14f817e9c73ea0625e4',
            u'commit',
            u'https://api.github.com/repos/mozilla-services/shavar/git/commits/1c4cff1014a869fd4c50b14f817e9c73ea0625e4?access_token=6b4e4a46d34c289f0974283d087e0a1b2124f004',
            u'2014-09-12'
        ]

        url = 'https://api.github.com/repos/mozilla-services/' + \
              'shavar/git/refs/tags'
        path_local = url_mock(url)
        mock_data = mock_fixture(path_local)
        json_data = json.loads(mock_data)
        parsed_tag = self._mock_rel_notes._parse_tag(json_data[0])
        self.assertEqual(parsed_tag, parsed_tag_match)

    # def test_get_latest_tags(self):
    #
    #     pass
    #
    # def test_get_commit_sha(self):
    #
    #     pass
    #
    # def test_get_commit_date(self):
    #
    #     pass
    #
    # def test_get_changelog(self):
    #
    #     pass
    #
    # def test_get_section_release_notes(self):
    #
    #     pass
    #
    # def test_get_section_comparisons(self):
    #
    #     pass
    #
    # def test_get_section_tags(self):
    #
    #     pass
    #
    # def test_get_section_changelog(self):
    #
    #     pass
    #
    # def test_get_release_notes(self):
    #
    #     pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
