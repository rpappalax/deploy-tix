import os
import itertools

HOST_GITHUB = 'github.com'
HOST_GITHUB_RAW = 'raw.githubusercontent.com'
MAX_COMPARISONS_TO_SHOW = 4
VERS = 0
SHA = 1
TYPE = 2
LINE = '------------------------------------'
CHANGELOG_NAMES = ['CHANGES', 'CHANGELOG', 'ChangeLog']
EXT = ['', '.rst', '.txt', '.RST', '.md']

CHANGELOG_FILENAMES = []
[CHANGELOG_FILENAMES.append(''.join(parts)) for parts in list(
    itertools.product(*[CHANGELOG_NAMES, EXT]))]

# github API
# unauthenticated: rate_limit = 60 requests / hour
# authenticated: allows for 5000 requests / hour
# Go to: github > Settings > Applications > Generate Access Token
if os.environ['ACCESS_TOKEN']:
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
else:
    ACCESS_TOKEN = ''