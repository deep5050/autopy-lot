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
INPUT_TYPE = os.environ['INPUT_INPUT_TYPE']  # [ py , ipynb, r]
COMMENT_MAGICS = os.environ['INPUT_COMMENT_MAGICS']  # [ true ]
# [ true ] [ py, ipynb, markdown, rmarkdown, r ]
SPLIT_AT_HEADING = os.environ['INPUT_SPLIT_AT_HEADING']
OUTPUT_TYPE = os.environ['INPUT_OUTPUT_TYPE']
OUTPUT_DIR = os.environ['INPUT_OUTPUT_DIR'] or './autopy-lot/'

OUTPUT_EXT = 'py'


def prepare_command() -> str:

    command = "jupytext"
    global OUTPUT_EXT

    if COMMENT_MAGICS:
        if COMMENT_MAGICS == 'true':
            command = command + " --opt comment_magics=true "
            print(command)
        else:
            print("supported: --opt command_magics: true")

    if SPLIT_AT_HEADING:
        if SPLIT_AT_HEADING == 'true':
            command = command + " --opt split_at_heading=true "
        else:
            print("supported: --opt split_at_heading=true")

    if OUTPUT_TYPE:
        if OUTPUT_TYPE == 'py':
            command = command + ' --to py'
            OUTPUT_EXT = 'py'

        elif OUTPUT_TYPE == 'ipynb':
            command = command + ' --to ipynb'
            OUTPUT_EXT = 'ipynb'

        elif OUTPUT_TYPE == 'markdown':
            command = command + ' --to markdown'
            OUTPUT_EXT = 'md'

        elif OUTPUT_TYPE == 'r':
            command = command + ' --to r'
            OUTPUT_EXT = 'R'

    return command


def get_all_files() -> iter:
    """Get list of all the input files in  this repo.
    """
    files = iglob(f'**/*.{INPUT_TYPE}', recursive=True)
    return files


def get_modified_files() -> list:
    """Get list of all the modified files only in a current commit.
    """
    cmd = 'git diff-tree --no-commit-id --name-only -r HEAD'
    committed_files = sp.getoutput(cmd).split('\n')
    files = [file for file in committed_files if (
        file.endswith(f'.{INPUT_TYPE}') and os.path.isfile(file))]
    return files


def convert_files(files: list, command: str) -> list:
    """Iterates over input file list.
    """
    output_files = []
    for file in files:
        output_file_name = f'{OUTPUT_DIR}{os.path.splitext(file)[0]}.{OUTPUT_EXT}'
        output_files.append(output_file_name)

        temp_command = command + f' {file} -o {output_file_name}'

        # run this command
        sp.call(temp_command, shell=True)
        print(f"converting :{file} -> {output_file_name} ")

    return output_files


def commit_changes(files: list):
    """Commits changes.
    """
    set_email = 'git config --local user.email "autopy-lot@master"'
    set_user = 'git config --local user.name "autopy-lot action"'

    sp.call(set_email, shell=True)
    sp.call(set_user, shell=True)
    file_list = ' '.join(set(files))

    git_checkout = f'git checkout {TARGET_BRANCH}'
    git_add = f'git add {file_list}'
    git_commit = 'git commit -m "Add/Update autopy-lot outputs"'
    print(f'Committing {file_list}...')

    sp.call(git_checkout, shell=True)
    sp.call(git_add, shell=True)
    sp.call(git_commit, shell=True)


def push_changes():
    """Pushes commit.
    """
    set_url = f'git remote set-url origin https://x-access-token:{GITHUB_TOKEN}@github.com/{TARGET_REPOSITORY}'
    git_push = f'git push origin {TARGET_BRANCH}'
    sp.call(set_url, shell=True)
    sp.call(git_push, shell=True)


def main():

    if (GITHUB_EVENT_NAME == 'pull_request') and (GITHUB_ACTOR != GITHUB_REPOSITORY_OWNER):
        return
    sp.call(f'mkdir {OUTPUT_DIR}',shell=True) # creating the output directory

    command = prepare_command()

    if CHECK:
        if CHECK == 'all':
            files = get_all_files()  # select all specifies input files
        elif CHECK == 'latest':
            files = get_modified_files()  # select files only modified in the last commit
        else:
            raise ValueError(
                f'{CHECK} is a wrong value. Expecting all or latest')
    else:
        files = []

    if files:
        output_files = convert_files(files, command)
        if output_files:
            # Commit changes
            commit_changes(output_files)  # add and commit the changes
            # Push
            push_changes()  # push the changes back
        else:
            print('Nothing to add. Nothing to update!')
    else:
        print('There is no modified input files in the current commit.')


if __name__ == '__main__':
    main()
