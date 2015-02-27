"""Module for constructing service deployment release notes using github api

Note:
    Github tags API only deals with tag objects - so
    only annotated tags, not lightweight tags.
"""

import sys
import requests
import json
import itertools
import config
from output_helper import OutputHelper


HOST_GITHUB = 'github.com'
HOST_GITHUB_RAW = 'raw.githubusercontent.com'
MAX_COMPARISONS_TO_SHOW = 4
VERS = 0
SHA = 1
TYPE = 2
LINE = '------------------------------------'
CHANGELOG_NAMES = ['CHANGES', 'CHANGELOG', 'ChangeLog']
EXT = ['', '.rst', '.txt', '.RST', '.md']

CHANGELOG_FILENAMES = []
[CHANGELOG_FILENAMES.append(''.join(parts)) for parts in list(
    itertools.product(*[CHANGELOG_NAMES, EXT]))]


class NotFoundError(Exception):
    pass

class ReleaseNotes(object):
    """Used for GET operations against github API."""

    def __init__(self, repo, application, environment):

        self.output = OutputHelper()
        if all([repo, application, environment]):
            self.repo = repo
            self.application = application
            self.environment = environment.upper()
        else:
            exit('\nMissing github param\n\nABORTING!\n\n')

        self._url_github = self._get_url_github()
        self._url_github_raw = self._get_url_github_raw()
        self._url_github_api = self._get_url_github_api()
        self._token_string = self._get_token_string()
        url = '{}/refs/tags{}'.format(self._url_github_api, self._token_string)
        req = self._get_tags(url)
        self._tags = req.json()
        self._max_comparisons = self._get_max_comparisons(self._tags)
        self._latest_tags = self._get_latest_tags()
        self._last_tag = self._get_last_tag()
        self._last_tag_version = self._last_tag[VERS]

    @property
    def last_tag(self):
        return self._last_tag_version


    def _get_last_tag(self):
        """Return last tag"""

        return self._latest_tags[self._max_comparisons - 1]

    def _get_token_string(self):
        """Return access_token as url param (if exists)"""

        if config.ACCESS_TOKEN:
            return '?access_token={}'.format(config.ACCESS_TOKEN)
        return ''


    def _get_url_github_api(self):
        """Return github API URL as string"""

        return 'https://api.{}/repos/{}/{}/git'.format(
            HOST_GITHUB,
            self.repo,
            self.application
            )


    def _get_url_github(self):
        """Return github root URL as string"""

        return 'https://{}/{}/{}'.format(
            HOST_GITHUB,
            self.repo,
            self.application
        )


    def _get_url_github_raw(self):
        return 'https://{}/{}/{}'.format(
            HOST_GITHUB_RAW,
            self.repo,
            self.application
        )


    def _get_max_comparisons(self, tags):
        """Calculates max comparisons to show

        Note:
            Display up to MAX_COMPARISONS_TO_SHOW (or less)

        Returns:
            integer - num of github release comparisons to display
        """

        count = len(tags)
        if count >= MAX_COMPARISONS_TO_SHOW:
            return MAX_COMPARISONS_TO_SHOW
        else:
            return count


    def _get_tags(self, url):
        """Get all tags as json from Github API."""

        req = requests.get(url)
        try:
            if 'Not Found' in req.text:
                raise NotFoundError
        except NotFoundError:
            err_header = self.output.get_header('ERROR')
            err_msg = '{}\nNothing found at: \n{}\nABORTING!\n\n'.format(
                err_header, url)
            sys.exit(err_msg)
        else:
            return req


    def _parse_tag(self, tag):
        """Parse a tag object for the data we want

        Return:
            list of desired elements
        """

        parts = tag['ref'].split('/')
        release_num = parts[2]
        sha = tag['object']['sha']
        type = tag['object']['type']
        url = tag['object']['url'] + self._token_string
        creation_date = self._get_commit_date(url)
        self.output.log((release_num, creation_date))
        return [release_num, sha, type, url, creation_date]


    def _get_latest_tags(self):
        """Github API returns all tags indiscriminately, but
        we only want the latest.

        Return:
            list of lists containing: [release_num, commit sha,
            object type] for last tags
        """

        self.output.log('Retrieve all tags', True)
        start = len(self._tags) - self._max_comparisons
        tags = self._tags
        tags_unsorted = []
        for i in xrange(len(tags)):
            tag = self._parse_tag(tags[i])
            tags_unsorted.append(tag)

        self.output.log('Sort tags by commit date', True)
        tags_sorted = sorted(
            tags_unsorted, key=lambda tags_sorted: tags_sorted[4])
        self.output.log('DONE!')

        latest = []
        self.output.log('Get last tags from sorted list', True)
        for i in xrange(len(tags_sorted)):
            if i >= start:
                latest.append(tags_sorted[i])
                self.output.log(tags_sorted[i])
        self.output.log(latest)
        return latest


    def _get_commit_sha(self):
        """Return tag commit sha as string.

        Note:
            Varies depending on object type: type='tag' or 'commit'
            type='tag' requires a secondary call to retrieve commit url"""

        last_tag = self._last_tag
        if last_tag[TYPE] == 'tag':
            url = '{}/tags/{}{}'.format(
                self._url_github_api,
                last_tag[SHA],
                self._token_string)

            req = self._get_tags(url)
            return req.json()['object']['sha']
        else:
            return last_tag[SHA]


    def _get_commit_date(self, url):
        """Return tag or commit creation date as string."""

        req = self._get_tags(url)
        if 'git/tags' in url:
            return req.json()['tagger']['date'].split('T')[0]
        else:
            return req.json()['committer']['date'].split('T')[0]


    def _get_changelog(self, commit_sha):
        """"Parse and return CHANGELOG for latest tag as string"""

        for filename in CHANGELOG_FILENAMES:
            url = '{}/{}/{}'.format(self._url_github_raw, commit_sha, filename)
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

        # parse out release notes for this release only
        # only works if version numbers in changelog appear exactly
        # as they are tagged
        vers_latest = self._latest_tags[self._max_comparisons - 1][VERS]
        vers_previous = self._latest_tags[self._max_comparisons - 2][VERS]

        flag = False

        log = ''
        for line in lines.splitlines():
            if vers_latest in line:
                flag = True
            if vers_previous in line:
                flag = False
            if flag:
                log += line + '\n'
        return log


    def _get_section_release_notes(self):
        """Return bugzilla release notes with header as string"""

        notes = self.output.get_header('RELEASE NOTES')
        notes += '{}/releases'.format(self._url_github) + '\n'
        return notes


    def _get_section_comparisons(self):
        """Return release notes - COMPARISONS section as string"""

        notes = self.output.get_sub_header('COMPARISONS')

        for i in xrange(0, self._max_comparisons - 1):
            start = self._latest_tags[i][VERS]
            end = self._latest_tags[i + 1][VERS]
            notes += '{}/compare/{}...{}'.format(self._url_github, start, end) \
                     + '\n'
        self.output.log('comparisons section - DONE!')
        return notes


    def _get_section_tags(self):
        """Return release notes - TAGS section as string"""

        commit_sha = self._get_commit_sha()
        notes = self.output.get_sub_header('TAGS')

        notes += '{}/releases/tag/{}'.format(
            self._url_github,
            self._latest_tags[self._max_comparisons - 1][VERS]) + '\n'

        notes += '{}/commit/{}'.format(self._url_github, commit_sha) + '\n'
        notes += self._get_section_changelog(commit_sha)
        self.output.log('tags section - DONE!')

        return notes


    def _get_section_changelog(self, commit_sha):
        """Return release notes - CHANGELOG section as string"""

        changelog = self._get_changelog(commit_sha)
        self.output.log('changelog section - DONE!')
        if changelog:
            return self.output.get_sub_header('CHANGELOG') + changelog
        else:
            return ''


    def get_release_notes(self):
        """Return release notes for Bugzilla deployment ticket as string"""

        self.output.log('Create release notes', True)
        notes = self._get_section_release_notes()
        notes += self._get_section_comparisons()
        notes += self._get_section_tags()
        return notes


def main():

    notes = ReleaseNotes()


if __name__ == '__main__':
    main()
