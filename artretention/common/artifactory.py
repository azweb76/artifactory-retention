import os

import requests
import logging

from . import core

log = logging.getLogger(name=__name__)


def get_artifactory_url(path):
    base_url = os.environ['ART_URL']
    full_path = '%s/%s' % (base_url, path)
    return full_path


def get_unused(days, repo):
    auth = core.get_credentials(
        'ART', user_env='USER', password_env='PASSWORD')

    url = get_artifactory_url('api/search/aql')
    query = """
items.find({
  "repo": {"$eq" : "%s"},
  "$or": [
    {
        "stat.downloaded": {"$before": "%sd"}
    },
    {
        "$and": [
            {"stat.downloads": {"$eq":null}},
            {"created": {"$before": "%sd"}}
        ]
    }
  ]
}).include("stat.downloaded","stat.downloads","created","repo","path","name")
""" % (repo, days, days)

    log.info('getting old artifacts...')
    r = requests.post(url, query, auth=auth)

    if r.status_code == 200:
        results = r.json()['results']
        storage_url = get_artifactory_url('api/storage')
        ret = [{
            'uri': '%s/%s/%s/%s' % (storage_url, repo, x['path'], x['name']),
            'lastDownloaded': x['stats'][0].get('downloaded', x['created'])
        } for x in results]
        return ret
    elif r.status_code == 404:
        return []
    raise RuntimeError(r.text)


def get_items(path):
    auth = core.get_credentials(
        'ART', user_env='USER', password_env='PASSWORD')
    url = get_artifactory_url('api/storage/%s' % path)
    r = requests.get(url, auth=auth)
    if r.status_code == 200:
        return r.json()


def get_item(item=None, path=None):
    auth = core.get_credentials(
        'ART', user_env='USER', password_env='PASSWORD')
    if path:
        item = get_artifactory_url('api/storage/%s' % path)
    r = requests.get(item, auth=auth)
    if r.status_code == 200:
        return r.json()


def delete_empty_folders(path, is_root, whatif=False):
    log.debug('Checking %s...' % path)
    items = get_items(path)['children']
    if len(items) == 0:
        if not is_root:
            log.info('Delete %s...' % path)
            if not whatif:
                del_item(path=path)
    else:
        for p in items:
            if p['folder']:
                delete_empty_folders((path + p['uri']), False, whatif)


def del_item(item=None, path=None):
    auth = core.get_credentials(
        'ART', user_env='USER', password_env='PASSWORD')
    if path:
        item = get_artifactory_url(path)

    r = requests.delete(item, auth=auth)
    if r.status_code == 204:
        return True
    elif r.status_code == 404:
        return True
    else:
        return False
