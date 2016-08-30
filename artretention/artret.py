#!/usr/bin/env python
# coding: utf-8

import argparse
import fnmatch
import time

from common import artifactory, core


def main():
    parser = argparse.ArgumentParser(
        description='Clean artifactory repository.')
    parser.add_argument('action', help='action to perform (clean, etc)')
    parser.add_argument(
        '--days',
        type=int,
        default=45,
        help='optional. default 45. number of days to check for unused artifacts')
    parser.add_argument(
        '--skip',
        type=int,
        default=50,
        help='optional. default 50. number of most recent artifacts in unused list to keep')
    parser.add_argument('--repo',
                        type=str,
                        default='docker-wsb-local',
                        help='	required. Artifactory repository to scan')
    parser.add_argument(
        '--folder',
        default=[],
        action='append',
        help='required. folders to group by for cleaning. use \'*\' for all')
    parser.add_argument(
        '--whatif',
        action='store_true',
        help='default false. don\'t actually delete, show log as if deleting')
    parser.add_argument('-v',
                        '--verbose',
                        action='count',
                        help='show detailed logs')

    args = parser.parse_args()
    if args.action == 'clean':
        deleteAction(args)


def deleteAction(args):
    days = args.days
    skip = args.skip
    folders = args.folder
    art_repo = args.repo

    fldrs = {}
    if args.verbose == 0:
        core.progress(0, 1, prefix = '', suffix = 'getting unsed...', decimals = 2)
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
        fldrs[fldr] = items[skip:]

    for fldr in fldrs:
        items = fldrs[fldr]
        if args.verbose == 0:
            core.progress(item_count, total_item_count, prefix = '', suffix = '%s: deleting...' % fldr, decimals = 2)
        delete_items(items, fldr, art_repo, args)

        if args.verbose > 0:
            core.echo('Scanning folder %s for empties...' % fldr)
        else:
            core.progress(item_count, total_item_count, prefix = '', suffix = '%s: folder cleanup...' % fldr, decimals = 2)
        artifactory.delete_empty_folders('%s/%s' % (
            art_repo, fldr), True, verbose=args.verbose, whatif=args.whatif)
        item_count += 1

    core.progress(item_count, total_item_count, prefix = '', suffix = 'done!', decimals = 2)
    core.echo('\n=== Retention Summary ===')
    core.echo('The following artifacts were removed:\n')
    for fldr in fldrs:
        items = fldrs[fldr]
        core.echo('%s: %s' % (fldr, len(items)))


def delete_items(items, repo, art_repo, args):
    items.sort(key=lambda x: x['lastDownloaded'], reverse=True)
    cnt = 0
    for d in items:
        p = d['uri'].split('/api/storage/')
        path = p[-1]
        if args.verbose > 0:
            core.echo('Deleting %s...' % path)

        if not args.whatif:
            artifactory.del_item(path=path)
        cnt += 1


if __name__ == '__main__':
    main()
