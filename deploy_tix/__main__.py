
import argparse
from deploy_tix.bugzilla_rest_api import BugzillaRESTAPI
from deploy_tix.release_notes import ReleaseNotes
from output_helper import OutputHelper


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
        required=False)

    parser.add_argument(
        '-a', '--application',
        help='Example: loop-server',
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

    parser.add_argument(
        '-z', '--bugzilla-prod',
        help='Add this option, and you\'ll post to bugzilla prod',
        action='store_true',
        required=False)

    args = vars(parser.parse_args())

    repo = args['repo']
    application = args['application']
    environment = args['environment']
    bugzilla_username = args['bugzilla_username']
    bugzilla_password = args['bugzilla_password']
    if args['bugzilla_prod']:
        exit()
        url_bugzilla = URL_BUGZILLA_PROD
    else:
        url_bugzilla = URL_BUGZILLA_DEV

    status = 'NEW'

    output = OutputHelper()
    output.log('Create deployment ticket', True, True)
    notes = ReleaseNotes(repo, application, environment)
    description = notes.get_release_notes()
    release_num = notes.last_tag

    ticket = BugzillaRESTAPI(
        url_bugzilla, bugzilla_username, bugzilla_password)

    resp =  ticket.create_bug(
        release_num, application, environment, status, description)

if __name__ == '__main__':
    main()
