import os
import unittest
import json
import mock
# from mock import Mock, patch
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



def url_mock(url_remote):
    url_parsed = urlparse(url_remote)
    # path_remote = '{0}://{1}{2}'.format(
    #     url_parsed.scheme,
    #     url_parsed.netloc,
    #     url_parsed.path
    # )
    return '{0}/{1}{2}'.format(
        'deploy_tix/tests/mocks',
        url_parsed.netloc,
        url_parsed.path
    )


def mock_fixture(path_local):
    # path_local = url_mock(url_remote)
    with open(path_local) as f:
        mock_data = f.read()
    return mock_data

@responses.activate
def mock_response(path_remote):
    path_local = url_mock(path_remote)
    path_remote = 'https://api.github.com/repos/mozilla-services/shavar/git/refs/tags'

    # path_local = url_mock(path_remote)
    # url_parsed = urlparse(path_remote)

    # path_remote = '{0}://{1}{2}'.format(
    #     url_parsed.scheme,
    #     url_parsed.netloc,
    #     url_parsed.path
    # )
    # path_local = '{0}/{1}{2}'.format(
    #     'deploy_tix/tests/mocks',
    #     url_parsed.netloc,
    #     url_parsed.path
    # )

    mock_data = mock_fixture(path_local)

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

    return resp


class ReleaseNotesTestCase(unittest.TestCase):
    """Tests for `release_notes.py`."""

    @mock.patch('deploy_tix.release_notes', 'ACCESS_TOKEN="xxxxxxxxxx"')
    def setUp(self):
        self.mock_rel_notes = ReleaseNotes(
            repo_owner=MOCK_REPO_OWNER,
            repo=MOCK_REPO,
            environment=MOCK_ENV
        )
        #
        # self.token_path = self.mock_rel_notes._get_token_string(ACCESS_TOKEN)
        # self.url_github = self.mock_rel_notes._get_url_github(
        #     HOST_GITHUB, MOCK_REPO_OWNER, MOCK_REPO)
        # self.url_github_api = self.mock_rel_notes._get_url_github_api(
        #     HOST_GITHUB, MOCK_REPO_OWNER, MOCK_REPO)

        # req = self._get_tags(url)
        # self._tags = req.json()
        # self._max_comparisons = self._get_max_comparisons(self._tags)
        # self._latest_tags = self._get_latest_tags()
        # self._last_tag = self._get_last_tag()
        # self._last_tag_version = self._last_tag[VERS]
        pass

    def test_get_last_tag(self):

        # print self.mock_rel_notes._get_last_tag.return_value

        pass

    def test_get_token_string(self):

        token_path_match = '?access_token=xxxxxxxxxx'
        self.assertTrue(self.token_path == token_path_match,
                        'Token string path is incorrect')

    def test_get_url_github(self):

        url_match = 'https://HOST/REPO-OWNER/REPO'
        url = self.mock_rel_notes._get_url_github('HOST', 'REPO-OWNER', 'REPO')
        self.assertTrue(url == url_match, 'URL github is incorrect')

    def test_get_url_github_api(self):

        # url_match = 'https://api.github.com/repos/mozilla-services/shavar/git'
        url_match = 'https://api.HOST/repos/REPO-OWNER/REPO/git'
        url = self.mock_rel_notes._get_url_github_api('HOST', 'REPO-OWNER', 'REPO')
        self.assertTrue(url == url_match, 'URL github API is incorrect')

    def test_url_github_api_tags(self):

        # url_match = 'https://api.github.com/repos/mozilla-services/shavar/' \
        #     'git/refs/tags?access_token=xxxxxxxxxx'

        url_match = 'HTTPS://HOST-URL/refs/tags?ACCESS_TOKEN=XXXXXXXX'
        url = self.mock_rel_notes._url_github_api_tags('HTTPS://HOST-URL', '?ACCESS_TOKEN=XXXXXXXX')
        print '**************'
        print url
        print url_match
        print '**************'
        self.assertTrue(url == url_match, 'URL github API is incorrect')


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


    # @mock.patch('deploy_tix.release_notes.requests.get', side_effect=mock_response)
    def test_get_tags(self):
        path_remote = 'https://api.github.com/repos/mozilla-services/shavar/git/refs/tags'
        # print self.mock_rel_notes._get_tags(path_remote)


        path_local = url_mock(path_remote)

        mock_data = mock_fixture(path_local)
        #
        # responses.add(responses.GET,
        #               path_remote,
        #               body=mock_data,
        #               status=200,
        #               content_type='application/json')
        # resp = requests.get(path_remote)



        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = mock_data

            tags = self._mock_rel_notes._get_tags()
            print '*********************'
            print tags.text
            print '*********************'
            assert tags.text == mock_data






        # resp = self.mock_rel_notes._get_tags(path_remote)

        # print '*************'
        # print resp.json()
        # print '*************'
        #
        # assert len(resp) > 1

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
