"""Module for constructing service deployment release notes using github api

Note:

Github tags API only deals with tag objects - so only annotated tags,
not lightweight tags.
"""

import sys
import argparse
import requests
import json
import inspect
from output_helper import OutputHelper

DEBUG = True

HOST_GITHUB = 'github.com'
HOST_GITHUB_RAW = 'raw.githubusercontent.com'
MAX_COMPARISONS_TO_SHOW = 4
VERS = 0
SHA = 1
LINE = '------------------'
NL = '\n'

class NotFoundError(Exception):
    pass

class GithubAPI(object):
    """Used for GET operations against github API.
    """

    def __init__(self, repo='', application='', environment=''):

        self.output = OutputHelper()
        if all([repo, application, environment]):
            self.repo = repo
            self.application = application
            self.environment = environment
        else:
            self.set_args()

        self.api_url = self.get_api_url()
        self.tags = self.get_tags()
        self.num_comparisons = self.get_num_comparisons(self.tags)
        self.latest_tags = self.get_latest_tags()
        self._last_tag = self.latest_tags[3][VERS]

    @property
    def last_tag(self):
        return self._last_tag

    def set_args(self):

        parser = argparse.ArgumentParser(
            description='Scripts for grabbing release tag info from '
                        'github API',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument(
            '-r', '--repo',
            default='mozilla-services',
            required=True)

        parser.add_argument(
            '-a', '--application',
            help='Example: loop-server',
            required=True)

        parser.add_argument(
            '-e', '--environment',
            help='Enter: stage, prod',
            default='stage',
            required=False)

        args = vars(parser.parse_args())

        self.repo = args['repo']
        self.application = args['application']
        self.environment = args['environment'].upper()


    def get_api_url(self):
        """Return github API URL as string"""

        url = 'https://api.{}/repos/{}/{}/git/'.format(
            HOST_GITHUB, self.repo, self.application)
        # print 'URL: {}'.format(url)
        return url


    def get_commit_url(self, commit_sha):
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

        req = requests.get(self.api_url + 'refs/tags')
        try:
            if 'Not Found' in req.text:
                raise NotFoundError
        except NotFoundError:
            err_header = self.output.get_header('ERROR')
            err_msg = '{}\nNothing found at: \n{}\nABORTING!\n\n'.format(
                err_header,
                self.api_url + 'refs/tags')
            sys.exit(err_msg)
        else:
            return json.loads(req.text)


    def get_latest_tags(self):
        """Github API can only return all tags, but we only want the latest.

        Return:
            list of lists containing: [release_num, git sha] for last tags
        """

        start = len(self.tags) - self.num_comparisons
        tags = self.tags
        latest = []
        for i in xrange(len(tags)):
            print
            if i >= start:
                parts = tags[i]['ref'].split('/')
                release_num = parts[2]
                sha = tags[i]['object']['sha']
                tag = [release_num, sha]
                latest.append(tag)
        return latest



    def get_url_tag_release(self, release_num):
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

    def get_num_comparisons(self, tags):
        """Display up to: MAX_COMPARISONS_TO_SHOW (if we have that many tags).
        If not, display comparisons of all tags.

        Returns:
            integer - num of github release comparisons to display
        """

        count = len(tags)
        if count >= MAX_COMPARISONS_TO_SHOW:
            return MAX_COMPARISONS_TO_SHOW
        return count


    def get_tag_object_sha(self, api_url):
        """Get object SHA for tag commit

        Returns:
            string - object sha
        """

        req = self.get_json_response(api_url)
        return req.json()['object']['sha']


    def get_changelog(self, commit_sha):
        """"Parse CHANGELOG for latest tag.

        Return:
            String with log from latest tag.
        """

        url = 'https://{}/{}/{}/{}/CHANGELOG'.format(
            HOST_GITHUB_RAW, self.repo, self.application, commit_sha)
        req = requests.get(url)
        lines = req.text

        first = self.latest_tags[self.num_comparisons - 1][VERS]
        last = self.latest_tags[self.num_comparisons - 2][VERS]
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
        notes = self.output.get_header('RELEASE NOTES')
        notes += 'https://{}/{}/{}/releases'.format(
            HOST_GITHUB, self.repo, self.application) + '\n'
        return notes


    def _get_section_comparisons(self):
        notes = self.output.get_sub_header('COMPARISONS')
        notes += self.get_comparison(self.latest_tags[0][VERS],
                                     self.latest_tags[1][VERS])

        if len(self.latest_tags) >= (MAX_COMPARISONS_TO_SHOW - 1):
            notes += self.get_comparison(self.latest_tags[1][VERS],
                                         self.latest_tags[2][VERS])

        if len(self.latest_tags) >= MAX_COMPARISONS_TO_SHOW:
            notes += self.get_comparison(self.latest_tags[2][VERS],
                                         self.latest_tags[3][VERS])
        return notes


    def _get_section_tags(self):
        notes = self.output.get_sub_header('TAGS')
        notes += self.get_url_tag_release(self.latest_tags[3][VERS]) + '\n'
        if self.application == 'loop-client':
            url = self.get_commit_url(self.latest_tags[3][SHA])
            commit_sha = self.get_tag_object_sha(url)
        else:
            commit_sha = self.latest_tags[3][SHA]

        notes += self.get_url_tag_commit(commit_sha) + '\n'
        notes += self._get_section_changelog(commit_sha)
        return notes


    def _get_section_changelog(self, commit_sha):
        changelog = self.get_changelog(commit_sha)
        if changelog:
            return self.output.get_sub_header('CHANGELOG') + changelog
        else:
            return ''


    def get_release_notes(self):
        """Constructs release notes for Bugzilla service deployment ticket.

        Returns:
            String - with release notes
        """

        notes = self._get_section_release_notes()
        notes += self._get_section_comparisons()
        notes += self._get_section_tags()
        return notes


    def get_commit(self, sha):
        # GET /repos/:owner/:repo/git/commits/:sha
        url = 'https://{}/{}/{}'.format(
            HOST_GITHUB, self.repo, self.application, sha)
        self.get_tag_object_sha(url)


def main():

    api = GithubAPI()
    print api.get_release_notes()


if __name__ == '__main__':
    main()
