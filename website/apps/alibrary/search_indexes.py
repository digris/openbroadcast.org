from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex
from alibrary.models import Release, Artist, Media, Label, Playlist

class ReleaseIndex(CelerySearchIndex, indexes.Indexable):

    text = indexes.EdgeNgramField(document=True, use_template=True)
    name = indexes.EdgeNgramField(model_attr='name', boost=1.5)
    releasedate = indexes.DateTimeField(model_attr='releasedate', null=True)
    # autocomplete handling
    text_auto = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Release

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class ArtistIndex(CelerySearchIndex, indexes.Indexable):

    text = indexes.EdgeNgramField(document=True, use_template=True)
    name = indexes.EdgeNgramField(model_attr='name', boost=1.5)
    # autocomplete handling
    text_auto = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Artist

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class MediaIndex(CelerySearchIndex, indexes.Indexable):

    text = indexes.EdgeNgramField(document=True, use_template=True)
    name = indexes.EdgeNgramField(model_attr='name', boost=1.5)
    # autocomplete handling
    text_auto = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Media

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class LabelIndex(CelerySearchIndex, indexes.Indexable):

    text = indexes.EdgeNgramField(document=True, use_template=True)
    name = indexes.EdgeNgramField(model_attr='name', boost=1.5)
    # autocomplete handling
    text_auto = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Label

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class PlaylistIndex(CelerySearchIndex, indexes.Indexable):

    text = indexes.EdgeNgramField(document=True, use_template=True)
    name = indexes.EdgeNgramField(model_attr='name', boost=1.5)
    type = indexes.CharField(model_attr='type', null=True)
    user_pk = indexes.IntegerField(model_attr='user__pk', null=True)
    # autocomplete handling
    text_auto = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Playlist

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
