import unicodecsv as csv
from django.http import HttpResponse

from spf.models import Request

def matches_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    #response = HttpResponse(content_type='text/html')
    response = HttpResponse(content_type='text/csv')
    #response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow([
                    'REQ SWP ID',
                    'REQ Title',
                    'REQ Artist',
                    'REQ Duration',
                    'REQ Country',
                    'REQ Recording date',
                    'REQ Publication date',
                    'REQ Label',
                    #
                    '-------',
                    'SWP ID',
                    'Title',
                    'Artist',
                    'Artist credits',
                    'Artist decondary credits',
                    'Duration',
                    'Release list',
                    'ISRC list',
                    'ISWC list',
                    'Match level'
                    ])

    for req in Request.objects.all()[0:1000]:

        matches = req.match_set.all()[0:10]

        if matches.count() > 0:

            for match in matches:

                writer.writerow([
                                 u'%s' % req.swp_id,
                                 u'%s' % req.title,
                                 u'%s' % req.main_artist,
                                 u'%s' % req.duration,
                                 u'%s' % req.recording_country,
                                 u'%s' % req.recording_datex,
                                 u'%s' % req.publication_datex,
                                 u'%s' % req.label,
                                 #
                                 '',
                                 u'%s' % match.mb_id,
                                 u'%s' % match.title,
                                 u'%s' % match.artist,
                                 u'%s' % match.artist_credits,
                                 u'%s' % match.artist_credits_secondary,
                                 u'%s' % match.duration,
                                 u'%s' % match.release_list,
                                 u'%s' % match.isrc_list,
                                 u'%s' % match.iswc_list,
                                 u'%s' % req.level,
                             ])
        else:

            writer.writerow([
                             u'%s' % req.swp_id,
                             u'%s' % req.title,
                             u'%s' % req.main_artist,
                             u'%s' % req.duration,
                             u'%s' % req.recording_country,
                             u'%s' % req.recording_datex,
                             u'%s' % req.publication_datex,
                             u'%s' % req.label,
                             #
                             '',
                             u'%s' % '---',
                             u'%s' % '---',
                             u'%s' % '---',
                             u'%s' % '---',
                             u'%s' % '---',
                             u'%s' % '---',
                             u'%s' % '---',
                             u'%s' % '---',
                             u'%s' % '---',
                             u'%s' % '---',
                         ])

    return response