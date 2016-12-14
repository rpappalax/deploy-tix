import argparse
from deploy_tix.bugzilla_rest_client import BugzillaRESTClient
from deploy_tix.release_notes import ReleaseNotes
from output_helper import OutputHelper


def main(args=None):

    parser = argparse.ArgumentParser(
        description='Scripts for creating / updating deployment tickets in \
        Bugzilla',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-a', '--application',
        help='Example: loop-server',
        required=True)

    parser.add_argument(
        '-l', '--go-live',
        help='Use this switch to post directly to bugzilla.mozilla.org \
            (without switch posts to: bugzilla-dev.allizom.org)',
        action='store_true',
        default=False,
        required=False)

    subparsers = parser.add_subparsers(help='Ticket action')

    # parser for ticket - {create} option
    parser_create = \
        subparsers.add_parser('NEW', help='Create a NEW deployment ticket.')

    parser_create.add_argument(
        '-o', '--repo-owner',
        help='Example: mozilla-services',
        default='mozilla-services',
        required=False)

    parser_create.add_argument(
        '-e', '--environment',
        help='Enter: STAGE, PROD',
        default='STAGE',
        required=False)

    parser_create.add_argument(
        '-m', '--cc-mail',
        help='Example: xyz-services-dev@mozilla.com \
            NOTE: must be a registered username!',
        default='',
        required=False)

    # parser for ticket - {upate} option
    parser_update = subparsers.add_parser(
        'UPDATE',
        help='UPDATE an existing deployment ticket'
    )
    parser_update.add_argument(
        '-i', '--bug-id',
        help='Example: 1234567',
        required=False)

    parser_update.add_argument(
        '-c', '--comment',
        help='Enter: <your bug comment>',
        required=True)

    args = vars(parser.parse_args())

    application = args['application']
    go_live = args['go_live']

    ticket = BugzillaRESTClient(go_live)

    if all(key in args for key in ['bug_id', 'comment']):
        bug_id = args['bug_id']
        comment = args['comment']

        ticket.bug_update(application, comment, bug_id)

    if all(key in args for key in ['repo_owner', 'application', 'environment']): # noqa
        repo_owner = args['repo_owner']
        environment = args['environment'].lower()
        if args['cc_mail']:
            cc_mail = args['cc_mail']
        else:
            cc_mail = ''
        status = 'NEW'

        output = OutputHelper()
        output.log('Create deployment ticket', True, True)
        notes = ReleaseNotes(repo_owner, application, environment)
        description = notes.get_release_notes()
        release_num = notes.last_tag
        output.log('Release Notes', True)
        output.log(description)

        ticket.bug_create(
            release_num, application, environment, status, description, cc_mail
        )
