#!/usr/bin/env python
# coding: utf-8

import argparse
import fnmatch
import time
import logging

from common import artifactory, core

log = logging.getLogger(name=__name__)

def main():
    parser = argparse.ArgumentParser(
        description='Clean artifactory repository.')
    subparsers = parser.add_subparsers()
    parser.add_argument(
        '-l',
        '--log-level',
        dest='log_level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='optional. Set the log level.')
    parser.add_argument('--repo',
                        type=str,
                        required=True,
                        help='required. Artifactory repository to scan')

    parser_a = subparsers.add_parser('clean')
    parser_a.add_argument(
        '--days',
        type=int,
        default=45,
        help='optional. default 45. number of days to check for unused artifacts')
    parser_a.add_argument(
        '--skip',
        type=int,
        default=50,
        help='optional. default 50. number of most recent artifacts in unused list to keep')
    parser_a.add_argument(
        '--folder',
        default=[],
        action='append',
        help='folders to group by for cleaning. use \'*\' for all')
    parser_a.add_argument(
        '-i', '--interval',
        type=int,
        default=0,
        help='default 0. Run retention periodically in seconds.')
    parser_a.add_argument(
        '--whatif',
        action='store_true',
        help='default false. don\'t actually delete, show log as if deleting')

    parser_a.set_defaults(func=clean_cli)

    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level))

    args.func(args)


def clean_cli(args):
    if args.interval > 0:
        while True:
            _deleteAction(args)
            time.sleep(args.interval)
    else:
        _deleteAction(args)

def _deleteAction(args):
    days = args.days
    skip = args.skip
    folders = args.folder
    art_repo = args.repo

    fldrs = {}
    items = artifactory.get_unused(days, art_repo)

    if len(folders) == 0:
        folders = ['*']

    for item in items:
        p = item['uri'].split('/api/storage/%s/' % art_repo)
        # dont include the deepest folder or artifact
        fldr = '/'.join(p[1].split('/')[:-2])
        if fldr not in fldrs:
            for f in folders:
                if fnmatch.fnmatch(fldr, f):
                    fldrs[fldr] = []
                    break
        if fldr in fldrs:
            fldrs[fldr].append({
                'uri': item['uri'],
                'folder': fldr,
                'lastDownloaded': time.strptime(item['lastDownloaded'][0:-7],
                                                "%Y-%m-%dT%H:%M:%S.%f")
            })

    item_count = 0
    total_item_count = len(fldrs)
    for fldr in fldrs:
        items = fldrs[fldr]
        items.sort(key=lambda x: x['lastDownloaded'], reverse=True)
        fldrs[fldr] = items[skip:]

    for fldr in fldrs:
        items = fldrs[fldr]
        subfolders = delete_items(items, fldr, art_repo, args)

        if not args.whatif:
            for f in subfolders:
                log.info('Scanning folder %s for empties...' % f)
                artifactory.delete_empty_folders(f, False, whatif=args.whatif)

        item_count += 1

    log.info('=== Retention Summary ===')
    log.info('The following artifacts were removed:')

    for fldr in fldrs:
        items = fldrs[fldr]
        log.info('%s: %s' % (fldr, len(items)))


def delete_items(items, repo, art_repo, args):
    cnt = 0
    subfolders = []
    for d in items:
        p = d['uri'].split('/api/storage/')
        path = p[-1]
        subfolders.append('/'.join(path.split('/')[:3]))
        log.info('Deleting %s (%s)...' % (path, d['lastDownloaded']))

        if not args.whatif:
            artifactory.del_item(path=path)
        cnt += 1
    return unique(subfolders)

def unique(k):
    new_k = []
    for elem in k:
        if elem not in new_k:
            new_k.append(elem)
    return new_k

if __name__ == '__main__':
    main()
