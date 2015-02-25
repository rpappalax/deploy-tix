"""Module for constructing service deployment release notes using github api

Note:
    Github tags API only deals with tag objects - so
    only annotated tags, not lightweight tags.
"""

import sys
import requests
import json
import itertools
from output_helper import OutputHelper


HOST_GITHUB = 'github.com'
HOST_GITHUB_RAW = 'raw.githubusercontent.com'
MAX_COMPARISONS_TO_SHOW = 4
VERS = 0
SHA = 1
TYPE = 2
LINE = '------------------'
LOG_NAMES = ['CHANGES', 'CHANGELOG', 'ChangeLog']
EXT = ['', '.rst', '.txt', '.RST', '.md']

LOG_FILES = []
[LOG_FILES.append(''.join(parts)) for parts in list(
    itertools.product(*[LOG_NAMES, EXT]))]


class NotFoundError(Exception):
    pass

class GithubAPI(object):
    """Used for GET operations against github API."""

    def __init__(self, repo, application, environment):

        self.output = OutputHelper()
        if all([repo, application, environment]):
            self.repo = repo
            self.application = application
            self.environment = environment.upper()
        else:
            exit('\nMissing github param\n\nABORTING!\n\n')

        self._api_url = self._get_api_url()
        self._tags = self.get_tags()
        self._max_comparisons = self._get_max_comparisons(self._tags)
        self.latest_tags = self._get_latest_tags()
        self._last_tag = self._get_last_tag()
        self._last_tag_version = \
            self._last_tag[VERS]

    @property
    def last_tag(self):
        return self._last_tag_version

    @last_tag.setter
    def last_tag(self, value):
        return self._last_tag_version


    def _get_last_tag(self):
        return self.latest_tags[self._max_comparisons - 1]


    def _get_max_comparisons(self, tags):
        """Calculates max comparisons to show

        Note:
            Display up to: MAX_COMPARISONS_TO_SHOW (if we have that many tags).
            otherwise, displays what we do have.

        Returns:
            integer - num of github release comparisons to display
        """

        count = len(tags)
        if count >= MAX_COMPARISONS_TO_SHOW:
            return MAX_COMPARISONS_TO_SHOW
        else:
            return count


    def _get_api_url(self):
        """Return github API URL as string"""

        url = 'https://api.{}/repos/{}/{}/git/'.format(
            HOST_GITHUB, self.repo, self.application)
        return url


    def _get_commit_url(self, commit_sha):
        """Return commit URL from github API URL as string"""

        url = 'https://api.{}/repos/{}/{}/git/tags/{}'.format(HOST_GITHUB,
                  self.repo, self.application, commit_sha)
        return url


    def get_json_response(self, url):
        """Get all tags as json from Github API."""

        req = requests.get(url)
        try:
            if 'Not Found' in req.text:
                raise NotFoundError
        except NotFoundError:
            err_header = self.output.get_header('ERROR')
            err_msg = '{}\nNothing found at: \n{}\nABORTING!\n\n'.format(
                err_header,
                url)
            sys.exit(err_msg)
        else:
            return req


    def get_tags(self):
        """Get all tags as json from Github API."""

        req = requests.get(self._api_url + 'refs/tags')
        try:
            if 'Not Found' in req.text:
                raise NotFoundError
        except NotFoundError:
            err_header = self.output.get_header('ERROR')
            err_msg = '{}\nNothing found at: \n{}\nABORTING!\n\n'.format(
                err_header,
                self._api_url + 'refs/tags')
            sys.exit(err_msg)
        else:
            return json.loads(req.text)


    def _get_latest_tags(self):
        """Github API returns all tags indiscriminately, but
        we only want the latest.

        Return:
            list of lists containing: [release_num, commit sha,
            object type] for last tags
        """

        start = len(self._tags)  - self._max_comparisons
        tags = self._tags
        latest = []
        for i in xrange(len(tags)):
            if i >= start:
                parts = tags[i]['ref'].split('/')
                release_num = parts[2]
                sha = tags[i]['object']['sha']
                type = tags[i]['object']['type']
                tag = [release_num, sha, type]
                latest.append(tag)

        return latest


    def _get_commit_sha(self):
        """Return tag commit sha as string.

        Note:
            Varies depending on object type: type='tag' or 'commit'
            type='tag' requires a secondary call to retrieve commit url"""

        latest_tag = self._last_tag
        if latest_tag[TYPE] == 'tag':
            url = self._get_commit_url(latest_tag[SHA])
            req = self.get_json_response(url)
            return req.json()['object']['sha']
        else:
            return latest_tag[SHA]


    def _get_url_tag_release(self, release_num):
        """Return github tag release URL as string"""

        url = 'https://{}/{}/{}/releases/tag/{}'.format(
            HOST_GITHUB,
            self.repo,
            self.application,
            release_num
        )
        return url


    def get_url_tag_commit(self, commit_sha):
        """Return github tag commit SHA URL as string"""

        url = 'https://{}/{}/{}/commit/{}'.format(
            HOST_GITHUB,
            self.repo,
            self.application,
            commit_sha
        )
        return url


    def get_comparison(self, start, end):
        """Return github compare URL as string"""

        return 'https://{}/{}/{}/compare/{}...{}'.format(
            HOST_GITHUB, self.repo, self.application, start, end) + '\n'


    def _get_changelog(self, commit_sha):
        """"Parse and return CHANGELOG for latest tag as string"""

        url = 'https://{}/{}/{}/{}/CHANGELOG'.format(
            HOST_GITHUB_RAW, self.repo, self.application, commit_sha)

        for log_name in LOG_FILES:
            url = 'https://{}/{}/{}/{}/{}'.format(
                HOST_GITHUB_RAW, self.repo,
                self.application, commit_sha, log_name)
            req = requests.get(url)
            try:
                if 'Not Found' in req.text:
                    raise NotFoundError
            except NotFoundError:
                pass
            else:
                break

        if req.text  == 'Not Found':
            return ''

        lines = req.text
        first = self.latest_tags[self._max_comparisons - 1][VERS]
        last = self.latest_tags[self._max_comparisons - 2][VERS]
        flag = False

        log = ''
        for line in lines.splitlines():
            if first in line:
                flag = True
            if last in line:
                flag = False
            if flag:
                log += line + '\n'
        return log


    def _get_section_release_notes(self):
        """Return bugzilla release notes with header as string"""

        notes = self.output.get_header('RELEASE NOTES')
        notes += 'https://{}/{}/{}/releases'.format(
            HOST_GITHUB, self.repo, self.application) + '\n'
        return notes


    def _get_section_comparisons(self):
        """Return github links to tag comparisons"""

        notes = self.output.get_sub_header('COMPARISONS')
        for i in xrange(0, self._max_comparisons - 1):
            notes += self.get_comparison(self.latest_tags[i][VERS],
                                         self.latest_tags[i + 1][VERS])
        return notes


    def _get_section_tags(self):
        commit_sha = self._get_commit_sha()
        notes = self.output.get_sub_header('TAGS')
        notes += self._get_url_tag_release(
            self.latest_tags[self._max_comparisons - 1][VERS]) + '\n'
        notes += self.get_url_tag_commit(commit_sha) + '\n'
        notes += self._get_section_changelog(commit_sha)
        return notes


    def _get_section_changelog(self, commit_sha):
        changelog = self._get_changelog(commit_sha)
        if changelog:
            return self.output.get_sub_header('CHANGELOG') + changelog
        else:
            return ''


    def get_release_notes(self):
        """Return release notes as string for Bugzilla deployment ticket."""

        notes = self._get_section_release_notes()
        notes += self._get_section_comparisons()
        notes += self._get_section_tags()
        return notes


def main():

    api = GithubAPI()
    print api.get_release_notes()


if __name__ == '__main__':
    main()
