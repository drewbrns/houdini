import sys
import getpass
import argparse
from helpers import create_user


def cmd_create_user():
    username = input('username: ')
    password = getpass.getpass('password: ')
    username = username.strip()
    if username is not '' and (password is not '' or password is not ' '):
        create_user(username, password)
    else:
        raise Exception('`username` and `password` are required.')


if __name__ == __name__:
    parser = argparse.ArgumentParser(description='Houdini Utility Script.') 
    parser.add_argument(
        'create_user', nargs='+', 
        help='create a new user'
    )

    args = parser.parse_args()

    try:
        if args.create_user:
            cmd_create_user()
    except KeyboardInterrupt:
        sys.exit(0)