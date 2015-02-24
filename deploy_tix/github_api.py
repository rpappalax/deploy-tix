"""Module for constructing service deployment release notes using github api
"""

import sys
import argparse
import requests
import json
from deploy_tix.output_helper import OutputHelper

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

    def __init__(self, repo='', product='', release_num='', environment=''):

        if all([repo, product, release_num, environment]):
            self.repo = repo
            self.product = product
            self.release_num = release_num
            self.environment = environment
        else:
            self.set_args()

        self.api_url = self.get_api_url()
        self.tags = self.get_tags()
        self.num_comparisons = self.get_num_comparisons(self.tags)
        self.latest_tags = self.get_latest_tags()
        self.output = OutputHelper()



    def set_args(self):

        parser = argparse.ArgumentParser(
            description='Scripts for creating / updating deployment tickets in \
            Bugzilla',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument(
            '-r', '--repo',
            default='mozilla-services',
            required=True)

        parser.add_argument(
            '-p', '--product',
            help='Example: loop-server',
            required=True)

        # @TODO: Need to add code to restrict query to <= release_num
        parser.add_argument(
            '-n', '--release-num',
            help='Example: 0.14.3',
            required=True)

        parser.add_argument(
            '-e', '--environment',
            help='Enter: stage, prod',
            default='stage',
            required=False)

        args = vars(parser.parse_args())

        self.repo = args['repo']
        self.product = args['product']
        self.release_num = args['release_num']
        self.environment = args['environment']


    def get_api_url(self):
        """Return github API URL as string"""

        url = 'https://api.{}/repos/{}/{}/git/'.format(HOST_GITHUB, \
                  self.repo, self.product)
        return url

    def get_url_data(self, url):
        req = requests.get(url)
        try:
            if 'Not Found' in req.text:
                raise NotFoundError
        except NotFoundError:
            err_header = self.output.get_header('ERROR')
            err_msg = '{}\nNot found at: \n{}\nABORTING!\n\n'.format(
                err_header,
                self.api_url)
            sys.exit(err_msg)
        else:
            return json.loads(req.text)

    def get_tags(self):
        """Get all tags as json from Github API."""
        return self.get_url_data(self.api_url + 'refs/tags')

    def get_tag(self, sha):
        """Get a specific tag's data from Github API."""
        return self.get_url_data(self.api_url + 'tags/' + sha)

    def get_latest_tags(self):
        """Github API can only return all tags, but we only want the latest.

        Return:
            list of lists containing: [release_num, git sha] for last tags
        """

        start = len(self.tags) - self.num_comparisons
        tags = self.tags
        latest = []
        for i in xrange(len(tags)):
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
            self.product,
            release_num
        )
        return url


    def get_url_tag_commit(self, git_sha):
        """Return github tag commit SHA URL as string"""

        url = 'https://{}/{}/{}/commit/{}'.format(
            HOST_GITHUB,
            self.repo,
            self.product,
            git_sha
        )
        return url


    def get_comparison(self, start, end):
        """Return github compare URL as string"""

        return 'https://{}/{}/{}/compare/{}...{}'.format(HOST_GITHUB, \
            self.repo, self.product, start, end) + '\n'

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


    def get_changelog(self, commit_sha):
        """"Parse CHANGELOG for latest tag.

        Return:
            String with log from latest tag.
        """

        url = 'https://{}/{}/{}/' + commit_sha + '/CHANGELOG'
        url = url.format(HOST_GITHUB_RAW, self.repo, self.product)

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

        notes = self.output.get_header('RELEASE NOTES')
        notes += 'https://{}/{}/{}/releases'.format(HOST_GITHUB, \
                                                    self.repo, self.product) + '\n'

        notes += self.output.get_sub_header('COMPARISONS')
        notes += self.get_comparison(self.latest_tags[0][VERS],
                                     self.latest_tags[1][VERS])

        if len(self.latest_tags) >= (MAX_COMPARISONS_TO_SHOW - 1):
            notes += self.get_comparison(self.latest_tags[1][VERS],
                                         self.latest_tags[2][VERS])

        if len(self.latest_tags) >= MAX_COMPARISONS_TO_SHOW:
            notes += self.get_comparison(self.latest_tags[2][VERS],
                                         self.latest_tags[3][VERS])

        tag_data = self.get_tag(self.latest_tags[3][SHA])

        notes += self.output.get_sub_header('TAGS')
        notes += self.get_url_tag_release(self.latest_tags[3][VERS]) + '\n'
        notes += self.get_url_tag_commit(tag_data["object"]["sha"]) + '\n'

        changelog = self.get_changelog(tag_data["object"]["sha"])
        if changelog:
            notes += self.output.get_sub_header('CHANGELOG')
            notes += changelog
        return notes



def main():

    api = GithubAPI()
    print api.get_release_notes()


if __name__ == '__main__':
    main()
