import os
import unittest
import json
import mock
import requests
import responses
from urlparse import urlparse
from deploy_tix.release_notes import ReleaseNotes


HOST_GITHUB = 'github.com'
HOST_GITHUB_RAW = 'raw.githubusercontent.com'
MOCK_MAX_COMPARISONS_TO_SHOW = 4
MOCK_REPO_OWNER = 'mozilla-services'
MOCK_REPO = 'shavar'
MOCK_ENV = 'STAGE'
ACCESS_TOKEN = 'xxxxxxxxxx'

def response_mock(path_local):
    with open(path_local) as f:
        mock_data = f.read()
    return mock_data

@responses.activate
def test_get_tags(url, path_local):

    url = 'https://api.github.com/repos/mozilla-services/shavar/git/refs/tags'
    url_parsed = urlparse(url)

    path_remote = '{0}://{1}{2}'.format(
        url_parsed.scheme,
        url_parsed.netloc,
        url_parsed.path
    )
    path_local = '{0}/{1}{2}'.format(
        'deploy_tix/tests/mocks',
        url_parsed.netloc,
        url_parsed.path
    )

    mock_data = response_mock(path_local)

    responses.add(responses.GET,
                  path_remote,
                  body=mock_data,
                  status=200,
                  content_type='application/json')
    resp = requests.get(path_remote)

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == path_remote
    assert resp.json() == json.loads(mock_data)
    assert responses.calls[0].response.text == mock_data



class ReleaseNotesTestCase(unittest.TestCase):
    """Tests for `release_notes.py`."""

    @mock.patch('deploy_tix.release_notes', 'ACCESS_TOKEN="xxxxxxxxxx"')
    def setUp(self):
        self.mock_rel_notes = ReleaseNotes(
            repo_owner=MOCK_REPO_OWNER,
            repo=MOCK_REPO,
            environment=MOCK_ENV
        )

        self.token_path = self.mock_rel_notes._get_token_string(ACCESS_TOKEN)
        self.url_github = self.mock_rel_notes._get_url_github(
            HOST_GITHUB, MOCK_REPO_OWNER, MOCK_REPO)
        self.url_github_api = self.mock_rel_notes._get_url_github_api(
            HOST_GITHUB, MOCK_REPO_OWNER, MOCK_REPO)

        # req = self._get_tags(url)
        # self._tags = req.json()
        # self._max_comparisons = self._get_max_comparisons(self._tags)
        # self._latest_tags = self._get_latest_tags()
        # self._last_tag = self._get_last_tag()
        # self._last_tag_version = self._last_tag[VERS]

    def test_get_last_tag(self):

        # print self.mock_rel_notes._get_last_tag.return_value
        pass

    def test_get_token_string(self):

        token_path_match = '?access_token=xxxxxxxxxx'
        self.assertTrue(self.token_path == token_path_match,
                        'Token string path is incorrect')

    def test_get_url_github(self):

        url_match = 'https://github.com/mozilla-services/shavar'
        self.assertTrue(self.url_github == url_match,
                        'URL github is incorrect')

    def test_get_url_github_api(self):

        url_match = \
            'https://api.github.com/repos/mozilla-services/shavar/git'
        self.assertTrue(self.url_github_api == url_match,
                        'URL github API is incorrect')

    def test_get_url_tags(self):

        url = self.mock_rel_notes._get_url_tags(
            self.url_github_api, self.token_path)
        url_match = \
            'https://api.github.com/repos/mozilla-services/shavar/' \
            'git/refs/tags?access_token=xxxxxxxxxx'
        self.assertTrue(url == url_match,
                        'URL github API is incorrect')

    @mock.patch('deploy_tix.release_notes', 'MAX_COMPARISONS_TO_SHOW=4')
    def test_get_max_comparisons(self):
        failure_msg = 'max_comparisons should be <= tags length'
        tags_list = [[0, 1, 2, 3],
                     [0, 1, 2, 3, 4],
                     [0, 1, 2, 3, 4, 5]]
        for tags in tags_list:
            result = self.mock_rel_notes._get_max_comparisons(tags)
            self.assertTrue(result >= 4, failure_msg)

        tags_list = [[0],
                     [0, 1],
                     [0, 1, 2],
                     [0, 1, 2, 3]]
        for tags in tags_list:
            result = self.mock_rel_notes._get_max_comparisons(tags)
            self.assertTrue(result == len(tags), failure_msg)


    # def test_get_tags(self):
    #
    #     pass
    #
    # def test_parse_tag(self):
    #
    #     pass
    #
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
