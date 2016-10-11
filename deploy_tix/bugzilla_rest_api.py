"""This module enables CRUD operations with Bugzilla 5.1 REST API

.. _Bugzilla REST API Docs:
   https://wiki.mozilla.org/Bugzilla:REST_API
   http://bugzilla.readthedocs.io/en/latest/api/index.html
"""

import sys
import json
import requests
from output_helper import OutputHelper

URL_BUGZILLA_PROD = 'https://bugzilla.mozilla.org'
URL_BUGZILLA_DEV = 'https://bugzilla-dev.allizom.org'

PRODUCT_PROD = 'Cloud Services'
COMPONENT_PROD = 'Operations: Deployment Requests'

PRODUCT_DEV = 'Mozilla Services'
COMPONENT_DEV = 'General'


class InvalidCredentials(Exception):
    pass


class BugzillaRESTAPI(object):
    """"Used for CRUD operations against Bugzilla REST API"""

    def __init__(self, host, bugzilla_username, bugzilla_password):

        self.output = OutputHelper()
        self.host = host
        self.username = bugzilla_username
        self.password = bugzilla_password
        self.token = self.get_token(host)

    def get_component(self, host):
        """Return Bugzilla component as string

        Note:
            bugzilla-dev doesn't mirror the same components, so
            use 'General'
        """

        if 'dev' in host:
            return PRODUCT_DEV, COMPONENT_DEV
        else:
            return PRODUCT_PROD, COMPONENT_PROD

    def get_json(self, release_num, product, environment, status, description):
        """Create bugzilla JSON to POST to REST API.

        Returns:
            JSON string
        """

        product, component = self.get_component(self.host)
        data = {
            'product': product,
            'component': component,
            'version': 'unspecified',
            'op_sys': 'All',
            'rep_platform': 'All'
        }
        short_desc = 'Please deploy {0} {1} to {2}'.format(
            release_num, product, environment)
        data.update(
            {
                'short_desc': short_desc,
                'description': description, 'status': status
            }
        )
        return data

    def get_token(self, host):
        """Fetch and return bugzilla token.

        Returns:
            string token
        """
        params = {
            'login': self.username,
            'password': self.password
        }
        url = '{0}/rest/login'.format(host)
        req = requests.get(url, params=params)
        decoded = json.loads(req.text)

        try:
            if 'token' not in decoded:
                raise InvalidCredentials
        except InvalidCredentials:
            err_header = self.output.get_header('BUGZILLA ERROR')

            err_msg = '{0}\n{1}\n{2}\n\n'.format(
                err_header,
                decoded['message'],
                decoded['documentation']
            )

            sys.exit(err_msg)
        else:
            return decoded['token']

    def create_bug(
            self, release_num, product, environment, status, description):
        """Create bugzilla bug with description

        Note:
            On bugzilla-dev - available status:
            NEW, UNCONFIRMED, ASSIGNED, RESOLVED

            On bugzilla - available status:
            NEW, UNCONFIRMED, RESOLVED, REOPENED, VERIFIED
            FIXED, INVALID, WONTFIX, DUPLICATE, WORKSFORME, INCOMPLETE

        Returns:
            json string to POST to REST API
        """

        self.output.log('Posting bug to bugzilla API...', True)
        url = '{0}/rest/bug?token={1}'.format(self.host, self.token)
        data = self.get_json(
            release_num, product, environment, status, description)

        self.output.log(data)

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        req = requests.post(url, data=json.dumps(data), headers=headers)
        new_bug_id = req.json()['id']

        self.output.log('\nNew bug ID: {0}\nDONE!\n\n'.format(new_bug_id))
        return new_bug_id


def main():

    bugzilla_username = 'johnnyquest@racebannon.com'
    bugzilla_password = 'hadji_is_a_geek'
    ticket = BugzillaRESTAPI(
        URL_BUGZILLA_DEV, bugzilla_username, bugzilla_password)

    bug_info = {'release_num': '1.2.3',
                'product': 'demo-server',
                'environment': 'STAGE',
                'status': 'NEW',
                'description': 'Lorem ipsum dolor sit amet, \
                ne dicat ancillae...'}

    print ticket.create_bug(**bug_info)


if __name__ == '__main__':

    main()
