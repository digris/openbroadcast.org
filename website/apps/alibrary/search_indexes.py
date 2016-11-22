from haystack import indexes
from alibrary.models import Release, Artist, Media, Label

class ReleaseIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', boost=1.5)
    releasedate = indexes.DateTimeField(model_attr='releasedate', null=True)

    def get_model(self):
        return Release

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class ArtistIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', boost=1.5)

    def get_model(self):
        return Artist

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class MediaIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', boost=1.5)

    def get_model(self):
        return Media

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
