deploy-tix
=============

Python scripts to generate Bugzilla deployment tickets for Mozilla Services.

Note: still under development. FOR OPS USE ONLY.

.. image:: https://travis-ci.org/rpappalax/deploy-tix.svg?branch=dev-rpapa
    :target: https://travis-ci.org/rpappalax/deploy-tix


**Supported projects**
 - loop-server
 - loop-client
 - msisdn-gateway
 - shavar
 - pushgo

**Example**

::

 -------------------
 RELEASE NOTES
 -------------------

.. parsed-literal::

 `<https://github.com/mozilla/loop-client/releases>`_
 |

::

 COMPARISONS

.. parsed-literal::

  `<https://github.com/mozilla/loop-client/compare/0.13.4...0.13.5>`_
  `<https://github.com/mozilla/loop-client/compare/0.13.5...0.14.0>`_
  `<https://github.com/mozilla/loop-client/compare/0.14.0...0.15.0>`_
 |

::

 TAGS

.. parsed-literal::

  `<https://github.com/mozilla/loop-client/releases/tag/0.15.0>`_
  `<https://github.com/mozilla/loop-client/commit/d706753dbcacfe17081d8c04b54652dbee36302f>`_
  |

::


 CHANGELOG
 0.15.0 (2015-03-09)
 -------------------

.. parsed-literal::

  \- `Bug 1047040 <https://bugzilla.mozilla.org/show_bug.cgi?id=1047040>`_ - Add browser-specific graphic of GUM prompt to the media-wait message
  \- `Bug 1131550 <https://bugzilla.mozilla.org/show_bug.cgi?id=1131550>`_ - Loop-client extraction script should preserve locale information when importing m-c changes
  \- `Bug 1135133 <https://bugzilla.mozilla.org/show_bug.cgi?id=1135133>`_ - Loop-client extraction script should support pulling from different repositories/branches
  \- `Bug 1137469 <https://bugzilla.mozilla.org/show_bug.cgi?id=1137469>`_ - If an uncaught exception occurs whilst processing an action, the dispatcher can fail, rendering parts of Loop inactive
  \- `Bug 1131568 <https://bugzilla.mozilla.org/show_bug.cgi?id=1131568>`_ - Update the OpenTok SDK to version 2.5.0


Setup
-----------
deploy-tix will make multiple calls to github API.
You're allowed up to 60 calls / hour without authentication, but you'll soon
run out!

Instead, create an access token from your github home page.  Go to:
#. Settings > Applications > Generate New Token
#. Create an environment variable 'ACCESS_TOKEN' or enter it into the config.py:

 ::

 $ export ACCESS_TOKEN=<your_access_token_here>



Build
-----------

 ::

 $ make build
 $ source ./build/venv/bin/activate



Run
-----------


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
----------------

Post to bugzilla-dev

 ::

 $ ticket -h -r mozilla-services -a loop-server -e STAGE -u johnny@quest.com -p password123


Post to bugzilla (add -z option)

 ::

 $ ticket -h -r mozilla-services -a loop-server -e STAGE -u johnny@quest.com -p password123 -z

