import os
import re
import json
from glob import iglob
import subprocess as sp


GITHUB_EVENT_NAME = os.environ['GITHUB_EVENT_NAME']

# Set repository
CURRENT_REPOSITORY = os.environ['GITHUB_REPOSITORY']
# TODO: How about PRs from forks?
TARGET_REPOSITORY = os.environ['INPUT_TARGET_REPOSITORY'] or CURRENT_REPOSITORY
PULL_REQUEST_REPOSITORY = os.environ['INPUT_PULL_REQUEST_REPOSITORY'] or TARGET_REPOSITORY
REPOSITORY = PULL_REQUEST_REPOSITORY if GITHUB_EVENT_NAME == 'pull_request' else TARGET_REPOSITORY

# Set branches
GITHUB_REF = os.environ['GITHUB_REF']
GITHUB_HEAD_REF = os.environ['GITHUB_HEAD_REF']
GITHUB_BASE_REF = os.environ['GITHUB_BASE_REF']
CURRENT_BRANCH = GITHUB_HEAD_REF or GITHUB_REF.rsplit('/', 1)[-1]
TARGET_BRANCH = os.environ['INPUT_TARGET_BRANCH'] or CURRENT_BRANCH
PULL_REQUEST_BRANCH = os.environ['INPUT_PULL_REQUEST_BRANCH'] or GITHUB_BASE_REF
BRANCH = PULL_REQUEST_BRANCH if GITHUB_EVENT_NAME == 'pull_request' else TARGET_BRANCH

GITHUB_ACTOR = os.environ['GITHUB_ACTOR']
GITHUB_REPOSITORY_OWNER = os.environ['GITHUB_REPOSITORY_OWNER']
GITHUB_TOKEN = os.environ['INPUT_GITHUB_TOKEN']

# command related inputs
CHECK = os.environ['INPUT_CHECK']  # 'all' | 'latest'
INPUT_TYPE = os.environ['INPUT_TYPE']  # [ py , ipynb, r]
COMMENT_MAGICS = os.environ['INPUT_COMMENT_MAGICS']  # [ true ]
SPLIT_AT_HEADING = os.environ['INPUT_SPLIT_AT_HEADING']  # [ true ]
# [ py, ipynb, markdown, rmarkdown, r ]
OUTPUT_TYPE = os.environ['INPUT_OUTPUT_TYPE']


def main():

    if (GITHUB_EVENT_NAME == 'pull_request') and (GITHUB_ACTOR != GITHUB_REPOSITORY_OWNER):
        return

    command = ''
    command = prepare_command()

    if CHECK:
        if CHECK == 'all':
            files = get_all_files()
        elif CHECK == 'latest':
            files = get_modified_files()
        else:
            raise ValueError(
                f'{CHECK} is a wrong value. Expecting all or latest')
    else:
        files = []

    if files:
        modified_files = check_file(files)
        if modified_files:
            # Commit changes
            commit_changes(modified_files)
            # Push
            push_changes()
        else:
            print('Nothing to add. Nothing to update!')
    else:
        print('There is no modified notebooks in a current commit.')







def prepare_command() -> str:
    pass


def get_all_files() -> iter:
    pass


def get_modified_files() -> list:
    pass


def check_file(files: list) -> list:
    pass


def commit_changes(nbs: list):
    pass


def push_changes():
    pass

