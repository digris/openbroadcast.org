# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math
from django.conf import settings

PAGINATE_BY_DEFAULT = getattr(settings, 'PAGINATE_BY_DEFAULT', 24)


def parse_search_query(request):
    """
    parses query string for search and filter parameters.
    example query string:
        ?filter_country=JP:FR&search_tags=video+game&search_q=sony
    """

    search_prefix = 'search_'
    filter_prefix = 'filter_'
    option_prefix = 'option_'

    _searches = {}
    _filters = {}
    _options = {}

    for key, value in request.GET.iteritems():
        # print(key, value)

        if not value or len(value) < 1:
            continue

        if key.startswith(search_prefix):
            _searches[key.replace(search_prefix, '')] = [v.strip() for v in value.split(':')]

        if key.startswith(filter_prefix):
            _filters[key.replace(filter_prefix, '')] = [v.strip() for v in value.split(':')]

        if key.startswith(option_prefix):
            _options[key.replace(option_prefix, '')] = value == '1'

    _order_by = request.GET.get('order_by', None)

    if not _order_by and _searches.get('q'):
        order_by = ()
    elif _order_by:
        order_by = (_order_by)
    else:
        order_by = ('-created')


    search_query = {
        'searches': _searches,
        'filters': _filters,
        'options': _options,
        'order_by': order_by,
    }

    return search_query


def parse_pagination_query(request):
    """
    parses query string for pagination
    """

    page = int(request.GET.get('page', 1))
    paginate_by = int(request.GET.get('ipp', PAGINATE_BY_DEFAULT))

    slice_start = (page - 1) * paginate_by
    slice_end = slice_start + paginate_by

    pagination_query = {
        'page': page,
        'paginate_by': paginate_by,
        'start': slice_start,
        'end': slice_end,
    }

    return pagination_query


def get_pagination_pages(num_pages, current_page):

    PAGE_RANGE_DISPLAYED = 6
    MARGIN_PAGES_DISPLAYED = 3

    if num_pages <= PAGE_RANGE_DISPLAYED:
        return range(1, num_pages + 1)

    pages = []
    left_side = PAGE_RANGE_DISPLAYED / 2
    right_side = PAGE_RANGE_DISPLAYED - left_side

    if current_page > num_pages - PAGE_RANGE_DISPLAYED / 2:
        right_side = num_pages - current_page
        left_side = PAGE_RANGE_DISPLAYED - right_side

    elif current_page < PAGE_RANGE_DISPLAYED / 2:
        left_side = current_page
        right_side = PAGE_RANGE_DISPLAYED - left_side

    for page in xrange(1, num_pages + 1):
        if page <= MARGIN_PAGES_DISPLAYED:
            pages.append(page)
            continue
        if page > num_pages - MARGIN_PAGES_DISPLAYED:
            pages.append(page)
            continue
        if (page >= current_page - left_side) and (page <= current_page + right_side):
            pages.append(page)
            continue
        if pages[-1]:
            pages.append(None)

    return pages


def get_pagination_data(result, query):

    current_page = query.get('page')
    paginate_by = query.get('paginate_by')
    num_results = result.hits.total
    num_pages = int(math.ceil(num_results / float(paginate_by)))

    pagination = {
        'current_page': current_page,
        'previous_page': current_page - 1 if current_page > 1 else None,
        'next_page': current_page + 1 if current_page < num_pages else None,
        'num_pages': num_pages,
        'num_results': num_results,
        'pages': get_pagination_pages(num_pages, current_page),
    }

    return pagination


def get_ordering_data(order_options, search_query, request):

    #order_by = request.GET.get('order_by')
    order_by = search_query['order_by']
    ordering_data = []

    # if order_by and order_by.startswith('-'):
    #     direction = 'desc'
    #     key = order_by.lstrip('-')
    # elif order_by:
    #     direction = 'asc'
    #     key = order_by
    # else:
    #     direction = 'asc'
    #     ordering_data = []
    #     key = None

    if order_by:
        selected_key = order_by.lstrip('-')
        selected_direction = 'desc' if order_by.startswith('-') else 'asc'
    else:
        selected_key = None
        selected_direction = None


    if search_query.get('searches') and search_query.get('searches').get('q'):
        ordering_data.append({
            'name': 'Best match',
            'query_key': 'order_by',
            'query_value': None,
            'direction': None,
            'selected': selected_key == None,
        })


    for option in order_options:

        if selected_key == option['key']:
            selected = True
            if selected_direction == 'asc':
                query = '-' + option['key']
            else:
                query = option['key']
        else:
            selected = False
            if option['default_direction'] == 'desc':
                query = '-' + option['key']
            else:
                query = option['key']


        ordering_data.append({
            'name': option['name'],
            'query_key': 'order_by',
            'query_value': query,
            'direction': selected_direction if selected else option['default_direction'],
            'selected': selected,
        })


    return ordering_data


def get_filter_data(facets, facets_definition=None):

    _ignore_keys = [
        'tags',
    ]

    _filters = []

    if facets_definition:
        keys = [f[0] for f in facets_definition if not f[0] in _ignore_keys]
    else:
        keys = [k for k in dir(facets) if k in _ignore_keys]

    for key in keys:

        # if key in _ignore_keys:
        #     continue

        options = getattr(facets, key)
        selected_options = [o[0] for o in options if o[2] == True]

        _options = []

        for option in getattr(facets, key):

            if option[2]:
                _q = [o for o in selected_options if not o == option[0]]
            else:
                _q = selected_options + [option[0]]

            #_query = ':'.join((str(x) for x in _q))
            _query = ':'.join(x for x in _q)

            _options.append({
                'name': option[0],
                'num': option[1],
                'selected': option[2],
                'query_key': 'filter_{}'.format(key),
                'query_value': _query,
            })

        _filters.append({
            'title': key,
            'key': key,
            'options': _options,
            'num_selected': len(selected_options),
        })

    return _filters


# Font size distribution algorithms
LOGARITHMIC, LINEAR = 1, 2

def _calculate_thresholds(min_weight, max_weight, steps):
    delta = (max_weight - min_weight) / float(steps)
    return [min_weight + i * delta for i in range(1, steps + 1)]

def _calculate_tag_weight(weight, max_weight, distribution):
    """
    Logarithmic tag weight calculation is based on code from the
    `Tag Cloud`_ plugin for Mephisto, by Sven Fuchs.

    .. _`Tag Cloud`: http://www.artweb-design.de/projects/mephisto-plugin-tag-cloud
    """

    if distribution == LINEAR or max_weight == 1:
        return weight
    elif distribution == LOGARITHMIC:
        return math.log(weight) * max_weight / math.log(max_weight)
    raise ValueError('Invalid distribution algorithm specified: %s.' % distribution)

def get_tagcloud_data(tags, request, steps=6, distribution=LOGARITHMIC, group_by=10):

    # currently selected tags in request
    current_tags = request.GET.get('search_tags', None)
    if current_tags and current_tags != '':
        current_tags = [t.strip() for t in current_tags.split(':')]
    else:
        current_tags = []


    # print(tags)

    # map to dict
    tags = [{'name': t[0], 'count': t[1], 'selected': t[2], 'weight': 1} for t in tags]

    if len(tags) > 0:
        counts = [tag['count'] for tag in tags]
        min_weight = float(min(counts))
        max_weight = float(max(counts))
        thresholds = _calculate_thresholds(min_weight, max_weight, steps)

        # print('counts', counts)
        # print('min_weight', min_weight)
        # print('max_weight', max_weight)
        # print('thresholds', thresholds)

        groups = []
        for i in range(steps):
            groups.append(0)

        hidden = []
        for i in range(steps):
            hidden.append(0)

        for tag in tags:
            weight_set = False
            tag_weight = _calculate_tag_weight(tag['count'], max_weight, distribution)
            for i in range(steps):

                if not weight_set and tag_weight <= thresholds[i]:
                    tag['weight'] = i + 1
                    groups[i] += 1
                    weight_set = True

        total = 0
        cnt = steps - 1
        for i in reversed(groups):
            hide_level = 0
            for x in range(1, steps + 1):
                if total > group_by *x:
                    hide_level +=1
            hidden[cnt] = hide_level
            total += i
            cnt -= 1

        for tag in tags:
            try:
                tag['hide_level'] = hidden[tag['weight'] -1]
            except Exception as e:
                pass


            if tag['name'] in current_tags:
                tag['selected'] = True
                tag['query'] = ':'.join(sorted([t for t in current_tags if not t == tag['name']]))
            else:
                tag['query'] = ':'.join(sorted([tag['name']] + current_tags))


        tags = sorted(tags, key=lambda k: k['name'])

    return tags
