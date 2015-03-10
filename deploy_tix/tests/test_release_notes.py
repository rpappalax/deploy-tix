import os
import itertools
import unittest
import mock
from deploy_tix import ReleaseNotes


HOST_GITHUB = 'mockhub.com'
HOST_GITHUB_RAW = 'raw.mockhubusercontent.com'
# MOCK_MAX_COMPARISONS_TO_SHOW = 4
MOCK_REPO = 'mozmock-services'
MOCK_APP = 'hollow-deck'
MOCK_ENV = 'STAGE'
ACCESS_TOKEN = 'xxxxxxxxxx'

# config.HOST_GITHUB =  'mockhub.com'
# config.HOST_GITHUB_RAW = 'raw.mockhubusercontent.com'
# config.MAX_COMPARISONS_TO_SHOW = 4
# config.VERS = 0
# config.SHA = 1
# config.TYPE = 2
#
# config.CHANGELOG_NAMES = ['CHANGES', 'CHANGELOG', 'ChangeLog']
# config.EXT = ['', '.rst', '.txt', '.RST', '.md']
#
# CHANGELOG_FILENAMES = []
# [CHANGELOG_FILENAMES.append(''.join(parts)) for parts in list(
#     itertools.product(*[config.CHANGELOG_NAMES, config.EXT]))]

# github API
# unauthenticated: rate_limit = 60 requests / hour
# authenticated: allows for 5000 requests / hour
# Go to: github > Settings > Applications > Generate Access Token
# ACCESS_TOKEN = os.environ['ACCESS_TOKEN']


class ReleaseNotesTestCase(unittest.TestCase):
    """Tests for `release_notes.py`."""


    @mock.patch('deploy_tix.config', 'ACCESS_TOKEN="xxxxxxxxxx"')
    def setUp(self):
        self.mock_rel_notes = ReleaseNotes(repo=MOCK_REPO,
                                        application=MOCK_APP,
                                        environment=MOCK_ENV)

        self.token_path = self.mock_rel_notes._get_token_string(ACCESS_TOKEN)
        self.url_github = self.mock_rel_notes._get_url_github(
            HOST_GITHUB, MOCK_REPO, MOCK_APP)
        self.url_github_api = self.mock_rel_notes._get_url_github_api(
            HOST_GITHUB, MOCK_REPO, MOCK_APP)

        #req = self._get_tags(url)
        #self._tags = req.json()
        #self._max_comparisons = self._get_max_comparisons(self._tags)
        #self._latest_tags = self._get_latest_tags()
        #self._last_tag = self._get_last_tag()
        #self._last_tag_version = self._last_tag[VERS]


    def test_get_last_tag(self):

        # print self.mock_rel_notes._get_last_tag.return_value
        pass


    def test_get_token_string(self):

        token_path_match = '?access_token=xxxxxxxxxx'
        self.assertTrue(self.token_path == token_path_match,
                        'Token string path is incorrect')


    def test_get_url_github(self):

        url_match = 'https://mockhub.com/mozmock-services/hollow-deck'
        self.assertTrue(self.url_github == url_match,
                        'URL github is incorrect')


    def test_get_url_github_api(self):

        url_match = \
            'https://api.mockhub.com/repos/mozmock-services/hollow-deck/git'
        self.assertTrue(self.url_github_api == url_match,
                        'URL github API is incorrect')


    def test_get_url_tags(self):

        url = self.mock_rel_notes._get_url_tags(
            self.url_github_api, self.token_path)
        url_match = \
            'https://api.mockhub.com/repos/mozmock-services/hollow-deck/' \
            'git/refs/tags?access_token=xxxxxxxxxx'
        self.assertTrue(url == url_match,
                        'URL github API is incorrect')


    @mock.patch('deploy_tix.config', 'MAX_COMPARISONS_TO_SHOW=4')
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


    def test_get_tags(self):
        MOCK_TAGS = [{u'url':  u'https://api.mockhub.com/repos/mozmock-services/hollow-deck/git/refs/tags/0.1', u'object': {u'url': u'https://api.mockhub.com/repos/mozmock-services/hollow-deck/git/commits/1c4cff1014a869fd4c50b14f817e9c73ea0625e4', u'sha': u'1c4cff1014a869fd4c50b14f817e9c73ea0625e4', u'type': u'commit'}, u'ref': u'refs/tags/0.1'}, {u'url': u'https://api.mockhub.com/repos/mozmock-services/hollow-deck/git/refs/tags/0.2', u'object': {u'url': u'https://api.mockhub.com/repos/mozmock-services/hollow-deck/git/commits/b42f8444482a738cd239fc438cae49e2a0d7d45b', u'sha': u'b42f8444482a738cd239fc438cae49e2a0d7d45b', u'type': u'commit'}, u'ref': u'refs/tags/0.2'}, {u'url': u'https://api.mockhub.com/repos/mozmock-services/hollow-deck/git/refs/tags/0.3', u'object': {u'url': u'https://api.mockhub.com/repos/mozmock-services/hollow-deck/git/commits/e38d654761d8a1882038670e3f4bf187b6e31d0e', u'sha': u'e38d654761d8a1882038670e3f4bf187b6e31d0e', u'type': u'commit'}, u'ref': u'refs/tags/0.3'}, {u'url': u'https://api.mockhub.com/repos/mozmock-services/hollow-deck/git/refs/tags/0.4', u'object': {u'url': u'https://api.mockhub.com/repos/mozmock-services/hollow-deck/git/commits/f984e506554f1984716974cc7673d11db5e2592a', u'sha': u'f984e506554f1984716974cc7673d11db5e2592a', u'type': u'commit'}, u'ref': u'refs/tags/0.4'}, {u'url': u'https://api.mockhub.com/repos/mozmock-services/hollow-deck/git/refs/tags/0.5', u'object': {u'url': u'https://api.mockhub.com/repos/mozmock-services/hollow-deck/git/commits/956c36c9a470c152abf34c7ae247292e987ede2c', u'sha': u'956c36c9a470c152abf34c7ae247292e987ede2c', u'type': u'commit'}, u'ref': u'refs/tags/0.5'}]
        pass


    def test_parse_tag(self):

        pass


    def test_get_latest_tags(self):

        pass


    def test_get_commit_sha(self):

        pass


    def test_get_commit_date(self):

        pass


    def test_get_changelog(self):

        pass


    def test_get_section_release_notes(self):

        pass


    def test_get_section_comparisons(self):

        pass


    def test_get_section_tags(self):

        pass


    def test_get_section_changelog(self):

        pass


    def test_get_release_notes(self):

        pass


    def tearDown(self):
        pass



    if __name__ == '__main__':
        unittest.main()
