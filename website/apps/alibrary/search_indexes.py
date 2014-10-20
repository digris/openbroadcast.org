from haystack import indexes
from alibrary.models import Release, Artist, Media, Label

class ReleaseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    releasedate = indexes.DateTimeField(model_attr='releasedate', null=True)
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Release

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        #return self.get_model().objects.filter(releasedate__lte=datetime.datetime.now())
        return self.get_model().objects.all()

class MediaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #releasedate = indexes.DateTimeField(model_attr='releasedate', null=True)
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Media

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        #return self.get_model().objects.filter(releasedate__lte=datetime.datetime.now())
        return self.get_model().objects.all()