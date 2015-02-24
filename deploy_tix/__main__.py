
import argparse
from deploy_tix.bugzilla_rest_api import BugzillaRESTAPI
from deploy_tix.github_api import GithubAPI

URL_BUGZILLA_PROD = 'https://bugzilla.mozilla.com'
URL_BUGZILLA_DEV = 'https://bugzilla-dev.allizom.org'


def main(args=None):

    parser = argparse.ArgumentParser(
        description='Scripts for creating / updating deployment tickets in \
        Bugzilla',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-r', '--repo',
        help='Example: mozilla-services',
        default='mozilla-services',
        required=True)

    parser.add_argument(
        '-a', '--application',
        help='Example: loop-server',
        required=True)

    # TODO(rpapa): Need to add code to restrict query to <= release_num
    parser.add_argument(
        '-n', '--release-num',
        help='Example: 0.14.3',
        required=True)

    parser.add_argument(
        '-e', '--environment',
        help='Enter: STAGE, PROD',
        default='STAGE',
        required=False)

    parser.add_argument(
        '-u', '--bugzilla-username',
        required=True)

    parser.add_argument(
        '-p', '--bugzilla-password',
        required=True)


    args = vars(parser.parse_args())

    repo = args['repo']
    application = args['application']
    release_num = args['release_num']
    environment = args['environment'].upper()
    bugzilla_username = args['bugzilla_username']
    bugzilla_password = args['bugzilla_password']
    status = 'NEW'

    api = GithubAPI(repo, application, environment)
    description = api.get_release_notes()
    ticket = BugzillaRESTAPI(
        URL_BUGZILLA_DEV, bugzilla_username, bugzilla_password)

    # TODO(rpapa): add a ticket update method
    print ticket.create_bug(
        release_num, application, environment, status, description)

if __name__ == '__main__':
    main()
