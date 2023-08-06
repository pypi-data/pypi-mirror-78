'''
Clones a git repository into a directory structure based on the URL.
'''
import argparse
import logging
import os
import sys
from pathlib import PurePath
from urllib.parse import urlparse

from git_cu import __version__ as VERSION

logger = logging.getLogger(__name__)


def parse_args(args):
    '''Parses command line options. Returns a Namespace.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-x',
                        '--dry-run',
                        action='store_true',
                        help='don\'t exec git')
    parser.add_argument('url')
    parser.add_argument(
        'args',
        nargs=argparse.REMAINDER,
        help='all further arguments are passed directly to git-clone')
    return parser.parse_args(args)


def git_cu(url, clone_args, dry_run):
    '''Invokes git clone for 'url' with arguments 'clone_args'.
    If 'dry_run' is True git clone is not actually exec()ed'''
    dest_dir = str(get_dest_dir(url))
    cmd = ['git', 'clone']
    cmd.extend(clone_args)
    cmd.append('--')
    cmd.append(url)
    cmd.append(dest_dir)
    cu_dir = os.environ.get('GIT_CU_DIR')
    if cu_dir:
        print(f'Running in GIT_CU_DIR {cu_dir}', file=sys.stderr)
        try:
            os.chdir(cu_dir)
        except FileNotFoundError as exc:
            logger.fatal('%s', exc)
            sys.exit(1)
    logger.debug(cmd)
    if not dry_run:
        os.execvp(cmd[0], cmd)


def main():
    '''Entry point. Parses command line arguments, sets up logging, and runs application.'''
    args = parse_args(sys.argv[1:])
    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.WARNING
    logging.basicConfig(
        level=log_level,
        format='%(levelname)s:%(name)s:%(funcName)s:%(message)s')
    git_cu(args.url, args.args, args.dry_run)


def clean_path(path):
    '''Returns a path with unnecessary components removed'''
    cleaned_path = path
    if cleaned_path.endswith('.git'):
        cleaned_path = cleaned_path[:-4]
    cleaned_path = cleaned_path.lstrip('/')
    logger.debug('%s -> %s', path, cleaned_path)
    return cleaned_path


def parse(url):
    '''Returns a destination path from a URL.'''
    parsed = urlparse(url)
    logger.debug(parsed)
    if parsed.netloc:
        host = parsed.netloc.split('@')[-1]
        logger.debug('host after removing user: %s', host)
        host = host.split(':')[0]
        logger.debug('host after removing port: %s', host)
    return PurePath(host, clean_path(parsed.path))


def parse_scp(url):
    '''Returns a destination path from an scp-style URL.'''
    host, path = url.split(':', maxsplit=1)
    logger.debug('host: %s path: %s', host, path)
    host = host.split('@')[-1]
    logger.debug('host after removing user: %s', host)
    return PurePath(host, clean_path(path))


def parse_local(url):
    '''Returns a destination path from a local path.'''
    return PurePath(url)


def get_dest_dir(url):
    '''Returns a destination directory based on url.'''
    is_url = '://' in url
    # alternative scp-like syntax
    # https://www.git-scm.com/docs/git-clone#URLS
    is_scp = ':' in url and not '/' in url.split(':')[0]
    if is_url:
        parser = parse
    elif is_scp:
        parser = parse_scp
    else:
        parser = parse_local
    return parser(url)
