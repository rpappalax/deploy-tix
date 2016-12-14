***********************************
deploy-tix
***********************************

Python scripts to generate deployment tickets for Mozilla Services in Bugzilla or github.

Note: still under development. FOR FIREFOX TEST ENG ONLY

.. image:: https://travis-ci.org/rpappalax/deploy-tix.svg
    :target: https://travis-ci.org/rpappalax/deploy-tix

.. image:: https://coveralls.io/repos/rpappalax/deploy-tix/badge.svg
    :target: https://coveralls.io/r/rpappalax/deploy-tix




**Supported projects**

 - shavar
 - autopush

**Example**

.. parsed-literal::

 -------------------
 RELEASE NOTES
 -------------------

 `<https://github.com/mozilla/loop-client/releases>`_


 COMPARISONS

 `<https://github.com/mozilla/loop-client/compare/0.13.4...0.13.5>`_
 `<https://github.com/mozilla/loop-client/compare/0.13.5...0.14.0>`_
 `<https://github.com/mozilla/loop-client/compare/0.14.0...0.15.0>`_


 TAGS

 `<https://github.com/mozilla/loop-client/releases/tag/0.15.0>`_
 `<https://github.com/mozilla/loop-client/commit/d706753dbcacfe17081d8c04b54652dbee36302f>`_


 CHANGELOG
 0.15.0 (2015-03-09)
 -------------------

  \- `Bug 1047040 <https://bugzilla.mozilla.org/show_bug.cgi?id=1047040>`_ - Add browser-specific graphic of GUM prompt to the media-wait message
  \- `Bug 1131550 <https://bugzilla.mozilla.org/show_bug.cgi?id=1131550>`_ - Loop-client extraction script should preserve locale information when importing m-c changes
  \- `Bug 1135133 <https://bugzilla.mozilla.org/show_bug.cgi?id=1135133>`_ - Loop-client extraction script should support pulling from different repositories/branches
  \- `Bug 1137469 <https://bugzilla.mozilla.org/show_bug.cgi?id=1137469>`_ - If an uncaught exception occurs whilst processing an action, the dispatcher can fail, rendering parts of Loop inactive
  \- `Bug 1131568 <https://bugzilla.mozilla.org/show_bug.cgi?id=1131568>`_ - Update the OpenTok SDK to version 2.5.0


Setup
--------------------------------------------------------------

Create github access token
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

deploy-tix will make multiple calls to github API.
You're allowed up to 60 calls / hour without authentication, but you'll soon
run out!

Instead, create an access token from your github home page.  Go to:

  1. Settings > Applications > Generate New Token
  2. Create an environment variable 'ACCESS_TOKEN' or enter it into the config.py:

 ::

 $ export ACCESS_TOKEN=<your_access_token_here>



Install
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 ::

 $ make build
 $ source ./venv/bin/activate


Run from Entry Point
--------------------------------------------------------------

Run
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. code:: python

  (venv)$ ticket
  Usage: ticket [args..] [options]

  -h, --help            show this help message and exit
  -o REPO_OWNER, --repo-owner REPO_OWNER Example: mozilla-services  (default: mozilla-services)
  -r REPO, --repo REPO  Example: loop-server (default: None)
  -e ENVIRONMENT, --environment ENVIRONMENT Example: STAGE, PROD (default: STAGE)
  -u BUGZILLA_USERNAME, --bugzilla-username BUGZILLA_USERNAME (default: None)
  -p BUGZILLA_PASSWORD, --bugzilla-password BUGZILLA_PASSWORD (default: None)
  -z, --bugzilla-prod   Add this option, and you'll post to bugzilla prod  (default: False)



Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Post to bugzilla-dev

 ::

 $ ticket -o mozilla-services -r loop-server -e STAGE -u johnny@quest.com -p password123


Post to bugzilla (add -z option)

 ::

 $ ticket -o mozilla-services -r loop-server -e STAGE -u johnny@quest.com -p password123 -z

Import as Library
--------------------------------------------------------------

**Example**

.. code:: python

    from deploy_tix.bugzilla_rest_client import BugzillaRESTClient
    from deploy_tix.release_notes import ReleaseNotes
    from deploy_tix.output_helper import OutputHelper


    # SAMPLE CODE
    bugzilla_mozilla = False # False will post to bugzilla-dev, 
                             # True will post to bugzilla.mozilla
                             # equivalent to -z option when using entry point

    ticket = BugzillaRESTClient(bugzilla_mozilla)
    output = OutputHelper()

    application = 'shavar'
    repo_owner = 'mozilla-services'
    environment = 'stage' # 'dev' # 'prod'
    # TODO: check if registered user must have token etc.,
    cc_mail = '<user email registered to bugzilla>'
    status = 'NEW'

    # OPTIONAL
    #  the following lines will generate a pre-formatted description useful for deployment tickets.
    output.log('Create deployment ticket', True, True)
    notes = ReleaseNotes(repo_owner, application, environment)
    description = notes.get_release_notes()
    release_num = notes.last_tag
    output.log('Release Notes', True)
    output.log(description)

    # Create a new ticket
    ticket.bug_create(
        release_num, application, environment, status, description, cc_mail
    )   

    # Update an existing ticket
    comment = 'a new comment to post in ticket'
    bug_id = '12345678' # Use bug num for Bugzilla, github issue num for github
    ticket.bug_update(application, comment, bug_id)



