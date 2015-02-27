deploy-tix
=============

Python scripts to generate Bugzilla deployment tickets for Mozilla Services.

Still under heavy development. FOR OPS USE AND DEMO ONLY.

## Projects
 * loop-server
 * loop-client
 * msisdn-gateway
 * shavar
 * pushgo

## Setup
deploy-tix will make multiple calls to github API.
You're allowed up to 60 calls / hour without authentication, but you'll soon
run out!

Instead, create an access token from your github home page.  Go to:

 - Settings > Applications > Generate New Token
 - Create an environment variable 'ACCESS_TOKEN' or enter it into the config.py:
   `$ export ACCESS_TOKEN=<your_access_token_here>`
 - Build and run:
 - `$ make build`
 - `$ source ./build/venv/bin/activate`
 - `$ ticket -h`