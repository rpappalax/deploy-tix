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
#from deploy_tix.output_helper import OutputHelper
from output_helper import OutputHelper

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

        # print '{}\n{}\n{}'.format(LINE, inspect.stack()[0][3], LINE)
        url = 'https://api.{}/repos/{}/{}/git/refs/tags'.format(
            HOST_GITHUB, self.repo, self.application)
        # print 'URL: {}'.format(url)
        return url


    def get_commit_url(self, git_sha):
        """Return commit URL from github API URL as string"""

        # print '{}\n{}\n{}'.format(LINE, inspect.stack()[0][3], LINE)
        # print HOST_GITHUB, self.repo, self.application
        url = 'https://api.{}/repos/{}/{}/git/tags/{}'.format(HOST_GITHUB,
                  self.repo, self.application, git_sha)
        return url


    def get_json_response(self, url):
        """Get all tags as json from Github API."""

        # print '{}\n{}\n{}'.format(LINE, inspect.stack()[0][3], LINE)
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
            # print 'REQ.TEXT: {}'.format(req.text)
            # print 'REQ.JSON: {}'.format(req.json()['object']['sha'])
            return req


    def get_tags(self):
        """Get all tags as json from Github API."""

        # print '{}\n{}\n{}'.format(LINE, inspect.stack()[0][3], LINE)
        # print 'API_URL: {}'.format(self.api_url)
        req = requests.get(self.api_url)
        try:
            if 'Not Found' in req.text:
                raise NotFoundError
        except NotFoundError:
            err_header = self.output.get_header('ERROR')
            err_msg = '{}\nNothing found at: \n{}\nABORTING!\n\n'.format(
                err_header,
                self.api_url)
            sys.exit(err_msg)
        else:
            return json.loads(req.text)


    def get_latest_tags(self):
        """Github API can only return all tags, but we only want the latest.

        Return:
            list of lists containing: [release_num, git sha] for last tags
        """

        # print '{}\n{}\n{}'.format(LINE, inspect.stack()[0][3], LINE)
        start = len(self.tags) - self.num_comparisons
        # print 'LEN(TAGS): {}, NUM_COMPARISONS: {}'.format(
        #     len(self.tags), self.num_comparisons)
        tags = self.tags
        latest = []
        for i in xrange(len(tags)):
            print
            if i >= start:
                # print 'TAGS: {}'.format(tags[i])
                parts = tags[i]['ref'].split('/')
                release_num = parts[2]
                sha = tags[i]['object']['sha']
                # print sha
                tag = [release_num, sha]
                latest.append(tag)
        return latest



    def get_url_tag_release(self, release_num):
        """Return github tag release URL as string"""

        # print '{}\n{}\n{}'.format(LINE, inspect.stack()[0][3], LINE)
        url = 'https://{}/{}/{}/releases/tag/{}'.format(
            HOST_GITHUB,
            self.repo,
            self.application,
            release_num
        )
        return url


    def get_url_tag_commit(self, git_sha):
        """Return github tag commit SHA URL as string"""

        # print '{}\n{}\n{}'.format(LINE, inspect.stack()[0][3], LINE)
        url = 'https://{}/{}/{}/commit/{}'.format(
            HOST_GITHUB,
            self.repo,
            self.application,
            git_sha
        )
        # print 'URL: {}'.format(url)
        return url


    def get_comparison(self, start, end):
        """Return github compare URL as string"""

        # print '{}\n{}\n{}'.format(LINE, inspect.stack()[0][3], LINE)
        return 'https://{}/{}/{}/compare/{}...{}'.format(
            HOST_GITHUB, self.repo, self.application, start, end) + '\n'

    def get_num_comparisons(self, tags):
        """Display up to: MAX_COMPARISONS_TO_SHOW (if we have that many tags).
        If not, display comparisons of all tags.

        Returns:
            integer - num of github release comparisons to display
        """

        # print '{}\n{}\n{}'.format(LINE, inspect.stack()[0][3], LINE)
        count = len(tags)
        if count >= MAX_COMPARISONS_TO_SHOW:
            return MAX_COMPARISONS_TO_SHOW
        return count


    def get_tag_object_sha(self, api_url):
        """Get object sha for tag commit

        Returns:
            string - object sha
        """

        # print '{}\n{}\n{}'.format(LINE, inspect.stack()[0][3], LINE)
        # print 'API_URL: {}'.format(api_url)
        req = self.get_json_response(api_url)
        return req.json()['object']['sha']


    def get_changelog(self):
        """"Parse CHANGELOG for latest tag.

        Return:
            String with log from latest tag.
        """

        # print '{}\n{}\n{}'.format(LINE, inspect.stack()[0][3], LINE)
        url = 'https://{}/{}/{}/master/CHANGELOG'.format(
            HOST_GITHUB_RAW, self.repo, self.application)
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


    def get_release_notes(self):
        """Constructs release notes for Bugzilla service deployment ticket.

        Returns:
            String - with release notes
        """

        # print '{}\n{}\n{}'.format(LINE, inspect.stack()[0][3], LINE)
        notes = self.output.get_header('RELEASE NOTES')
        notes += 'https://{}/{}/{}/releases'.format(
            HOST_GITHUB, self.repo, self.application) + '\n'

        notes += self.output.get_sub_header('COMPARISONS')
        notes += self.get_comparison(self.latest_tags[0][VERS],
                                     self.latest_tags[1][VERS])

        if len(self.latest_tags) >= (MAX_COMPARISONS_TO_SHOW - 1):
            notes += self.get_comparison(self.latest_tags[1][VERS],
                                         self.latest_tags[2][VERS])

        if len(self.latest_tags) >= MAX_COMPARISONS_TO_SHOW:
            notes += self.get_comparison(self.latest_tags[2][VERS],
                                         self.latest_tags[3][VERS])

        notes += self.output.get_sub_header('TAGS')
        notes += self.get_url_tag_release(self.latest_tags[3][VERS]) + '\n'

        # this returns master commit
        if self.application == 'loop-client':
            url = self.get_commit_url(self.latest_tags[3][SHA])
            git_sha = self.get_tag_object_sha(url)
            # notes += self.get_url_tag_commit(git_sha) + '\n'
        else:
            # notes += self.get_url_tag_commit(self.latest_tags[3][SHA]) + '\n'
            git_sha = self.latest_tags[3][SHA]

        notes += self.get_url_tag_commit(git_sha) + '\n'

        changelog = self.get_changelog()
        if changelog:
            notes += self.output.get_sub_header('CHANGELOG')
            notes += changelog
        return notes

    def get_commit(self, sha):
        # GET /repos/:owner/:repo/git/commits/:sha
        #https://github.com/mozilla-services/loop-server/commit/4a6a294e243fa62a98d311fce10e33fa336828fe
        url = 'https://{}/{}/{}'.format(
            HOST_GITHUB, self.repo, self.application, sha)
        self.get_tag_object_sha(url)

def main():

    api = GithubAPI()
    print api.get_release_notes()


if __name__ == '__main__':
    main()
