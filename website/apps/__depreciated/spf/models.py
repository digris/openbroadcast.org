import time
from time import mktime
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext as _
from django_extensions.db.fields.json import JSONField

# Create your models here.



DATE_FORMATS = [
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', # '2006-10-25', '10/25/2006', '10/25/06'
    '%d.%m.%Y',                         # '25.10.2006'
    '%b %d %Y', '%b %d, %Y',            # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',            # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
]


class Request(models.Model):

    STATUS_CHOICES = (
        (0, 'Init'),
        (1, 'Searched'),
        (2, 'Matched'),
        (99, 'Error'),
    )
    status = models.PositiveIntegerField(default=0, choices=STATUS_CHOICES)


    # 'incoming' fields
    swp_id = models.PositiveIntegerField(max_length=12, null=True, blank=True)
    title = models.CharField(max_length=1024, blank=True, null=True)

    recording_date = models.CharField(max_length=64, blank=True, null=True)
    recording_datex = models.DateField(blank=True, null=True)

    recording_country = models.CharField(max_length=64, blank=True, null=True)
    duration = models.PositiveIntegerField(max_length=12, null=True, blank=True)
    rome_protected = models.BooleanField(default=False)
    main_artist = models.CharField(max_length=1024, blank=True, null=True)


    publication_date = models.CharField(max_length=64, blank=True, null=True)
    publication_datex = models.DateField(blank=True, null=True)

    composer = models.CharField(max_length=1024, blank=True, null=True)
    label = models.CharField(max_length=1024, blank=True, null=True)
    catalognumber = models.CharField(max_length=256, blank=True, null=True)
    isrc = models.CharField(max_length=256, blank=True, null=True)


    # auto-update
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    # mapping data
    num_results = models.IntegerField(max_length=12, null=True, blank=True)
    level = models.IntegerField(max_length=12, null=True, blank=True)
    obp_legacy_id = models.PositiveIntegerField(max_length=12, null=True, blank=True)

    results_mb = JSONField(blank=True, null=True)


    class Meta:
        app_label = 'spf'
        verbose_name = _('Request')
        verbose_name_plural = _('Requests')
        ordering = ('swp_id', )


    def __unicode__(self):
        return u'[ %s ] %s' % (self.swp_id, self.title)


    def save(self, *args, **kwargs):

        if self.recording_date:
            #print 'recording_date'
            struct = time.strptime(self.recording_date, "%d.%m.%Y")
            self.recording_datex = datetime.fromtimestamp(mktime(struct))

        if self.publication_date:
            #print 'publication_date'
            struct = time.strptime(self.publication_date, "%d.%m.%Y")
            self.publication_datex = datetime.fromtimestamp(mktime(struct))



        super(Request, self).save(*args, **kwargs)


class Match(models.Model):

    STATUS_CHOICES = (
        (0, 'Init'),
        (1, 'Done'),
        (99, 'Error'),
    )
    status = models.PositiveIntegerField(default=0, choices=STATUS_CHOICES)
    request = models.ForeignKey(Request, blank=True, null=True, on_delete=models.SET_NULL)


    # mb mapping
    mb_id = models.CharField(max_length=64, blank=True, null=True)


    # auto-update
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)


    # gathered information

    title = models.CharField(max_length=1024, null=True, blank=True)

    artist = models.CharField(max_length=1024, null=True, blank=True)
    duration = models.PositiveIntegerField(default=0)

    artist_credits = models.TextField(null=True, blank=True)
    artist_credits_secondary = models.TextField(null=True, blank=True)

    release = models.CharField(max_length=512, null=True, blank=True)
    release_list = models.TextField(null=True, blank=True)

    work_list = models.TextField(null=True, blank=True)
    iswc_list = models.TextField(null=True, blank=True)
    isrc_list = models.TextField(null=True, blank=True)



    results_mb = JSONField(blank=True, null=True)



    class Meta:
        app_label = 'spf'
        verbose_name = _('Match')
        verbose_name_plural = _('Matches')
        ordering = ('created', )


    def __unicode__(self):
        return u'%s | %s' % (self.pk, self.artist)


    def save(self, *args, **kwargs):

        """
        if self.recording_date:
            print 'recording_date'
            struct = time.strptime(self.recording_date, "%d.%m.%Y")
            self.recording_datex = datetime.fromtimestamp(mktime(struct))

        if self.publication_date:
            print 'publication_date'
            struct = time.strptime(self.publication_date, "%d.%m.%Y")
            self.publication_datex = datetime.fromtimestamp(mktime(struct))
        """


        super(Match, self).save(*args, **kwargs)
