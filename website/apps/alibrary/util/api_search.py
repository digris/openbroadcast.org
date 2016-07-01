import requests
import json
import re
import urllib
from django.conf import settings
import logging

DISCOGS_HOST = getattr(settings, 'DISCOGS_HOST', None)

API_MAX_REQUESTS = 5

log = logging.getLogger(__name__)

def sort_results(items):
    return sorted(items, key = lambda r: [r['formatted_title'].lower(), r['index']])

def get_index(title):
    name_pattern = ' \([0-9]+\)'
    m = re.findall(name_pattern, title)
    if m:
        return int(m[0].strip(' ()'))

    return 0


def populate_results(results):

    for r in results[0:10]:
        url = r['resource_url']
        log.debug(url)

        try:

            req = requests.get(url)
            res = req.json()

            if 'realname' in res:
                r['real_name'] = res['realname']

            if 'aliases' in res and res['aliases']:
                r['aliases'] = ', '.join([a['name'] for a in res['aliases']])

            if 'members' in res and res['members']:
                r['members'] = ', '.join([m['name'] for m in res['members']])

        except Exception as e:

            log.debug('unable to populate data for {0} - {1}'.format(url, e))

            pass


    return results



def discogs_ordered_search(query, item_type, limit=100):

    name_pattern = ' \([0-9]+\)'
    q_stripped = query.strip("'\"")

    # special case when searching directly by id
    if q_stripped.isdigit():

        url = 'http://{host}/{item_type}s/{query}'.format(
            host=DISCOGS_HOST,
            query=urllib.quote_plus(query.lower()),
            item_type=item_type
        )

        log.debug('search by id: {0}'.format(url))
        r = requests.get(url)

        if not r.status_code == 200:
            return []


        data = json.loads(r.text.replace('api.discogs.com', DISCOGS_HOST))

        # TODO: not very nice - remap some fields
        if item_type == 'release':

            if 'title' in data:
                data['title'] = re.sub(name_pattern, '', data['title'])

            if 'formats' in data:
                formats = []
                for format in [f['name'] for f in data['formats'] if 'name' in f]:
                    formats.append(format)
                data['format'] = formats

            if 'labels' in data:
                try:
                    data['catno'] = data['labels'][0]['catno']
                except KeyError:
                    pass

        if item_type == 'artist':

            if 'name' in data:
                data['title'] = re.sub(name_pattern, '', data['name'])

            if 'aliases' in data:
                aliases = []
                for alias in [a['name'] for a in data['aliases'] if 'name' in a]:
                    aliases.append(re.sub(name_pattern, '', alias))
                data['aliases'] = aliases

            if 'members' in data:
                members = []
                for member in [m['name'] for m in data['members'] if 'name' in m]:
                    members.append(re.sub(name_pattern, '', member))
                data['members'] = members

            if 'images' in data:

                for image in [i['uri150'] for i in data['images'] if 'type' in i and i['type'] == 'primary']:
                    data['thumb'] = image
                    break





        return [data,]






    url = 'http://{host}/database/search?q={query}&type={item_type}&per_page=100'.format(
        host=DISCOGS_HOST,
        query=urllib.quote_plus(query.lower()),
        item_type=item_type
    )

    results = []
    results_exact = []
    results_start = []
    results_other = []

    x = 0
    while url and x < API_MAX_REQUESTS:

        log.debug(url)
        r = requests.get(url)

        if not r.status_code == 200:
            return []

        data = json.loads(r.text.replace('api.discogs.com', DISCOGS_HOST))

        url = reduce(dict.get, ['pagination', 'urls', 'next'], data)

        for r in data['results']:
            if 'title' in r:
                title = r['title']
                formatted_title = re.sub(name_pattern, '', title)
                r['index'] = get_index(title)
                r['formatted_title'] = formatted_title
                r['uri'] = 'https://www.discogs.com%s' % r['uri']

                if formatted_title.lower() == q_stripped.lower():
                    results_exact.append(r)
                elif formatted_title.lower().startswith(q_stripped.lower()):
                    results_start.append(r)
                else:
                    results_other.append(r)

        x += 1

    results = sort_results(results_exact) + sort_results(results_start)+ sort_results(results_other)

    if item_type == 'artist':
        results = populate_results(results)

    return results[0:limit]
