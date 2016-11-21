from haystack import indexes
from alibrary.models import Release, Artist, Media, Label

class ReleaseIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    releasedate = indexes.DateTimeField(model_attr='releasedate', null=True)
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Release

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
