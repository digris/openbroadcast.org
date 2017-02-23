from haystack import indexes
from profiles.models import Profile

class ProfileIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    name = indexes.EdgeNgramField(model_attr='get_display_name', boost=1.5)

    def get_model(self):
        return Profile

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


