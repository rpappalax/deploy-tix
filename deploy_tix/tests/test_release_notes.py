import os
import itertools
import unittest
import mock
from deploy_tix import ReleaseNotes

#
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

HOST_GITHUB = 'mockhub.com'
HOST_GITHUB_RAW = 'raw.mockhubusercontent.com'
MOCK_REPO = 'mozmock-services'
MOCK_APP = 'hollow-deck'
MOCK_ENV = 'STAGE'
ACCESS_TOKEN = 'xxxxxxxxxx'


class ReleaseNotesTestCase(unittest.TestCase):
    """Tests for `release_notes.py`."""


    def setUp(self):
        self.mock_rel_notes = ReleaseNotes(repo=MOCK_REPO,
                                        application=MOCK_APP,
                                        environment=MOCK_ENV)


       #
        #self._url_github = self._get_url_github()
        #self._url_github_raw = self._get_url_github_raw()
        #self._url_github_api = self._get_url_github_api()
        #self._token_string = self._get_token_string()
        #url = '{}/refs/tags{}'.format(self._url_github_api, self._token_string)
        #req = self._get_tags(url)
        #self._tags = req.json()
        #self._max_comparisons = self._get_max_comparisons(self._tags)
        #self._latest_tags = self._get_latest_tags()
        #self._last_tag = self._get_last_tag()
        #self._last_tag_version = self._last_tag[VERS]
        pass



    def test_get_last_tag(self):

        # print self.mock_rel_notes._get_last_tag.return_value
        pass


    @mock.patch('deploy_tix.config', 'ACCESS_TOKEN="xxxxxxxxxx"')
    def test_get_token_string(self):

        token_path = self.mock_rel_notes._get_token_string(ACCESS_TOKEN)
        token_path_match = '?access_token=xxxxxxxxxx'
        self.assertTrue(token_path == token_path_match,
                        'Token string path is incorrect')


    def test_get_url_github(self):

        url = self.mock_rel_notes._get_url_github(
            HOST_GITHUB, MOCK_REPO, MOCK_APP)
        url_match = 'https://mockhub.com/mozmock-services/hollow-deck'
        self.assertTrue(url == url_match, 'URL github is incorrect')


    def test_get_url_github_api(self):

        url = self.mock_rel_notes._get_url_github_api(
            HOST_GITHUB, MOCK_REPO, MOCK_APP)
        url_match = \
            'https://api.mockhub.com/repos/mozmock-services/hollow-deck/git'
        self.assertTrue(url == url_match, 'URL github API is incorrect')



    # def test_get_url_github_raw(self):
    #
    #     pass


    def test_get_max_comparisons(self):

        pass


    def test_get_tags(self):

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
