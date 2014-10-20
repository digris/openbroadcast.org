"""
Class based generic views.
These views are only available if you are using Django >= 1.3.
"""
from django.views.generic.detail import DetailView

from ratings.handlers import ratings

class VotedByView(DetailView):
    """
    Can be used to render a list of users that voted a given object.

    For example, you can add in your *urls.py* a view displaying all
    users that voted a single active article::
    
        from ratings.views.generic import VotedByView
        
        urlpatterns = patterns('',
            url(r'^(?P<slug>[-\w]+)/votes/$', VotedByView.as_view(
                queryset=Article.objects.filter(is_active=True)),
                name="article_voted_by"),
        )
        
    Two context variables will be present in the template:
        - *object*: the voted article
        - *votes*: all the Vote instances for that article
        
    The default template suffix is ``'_voted_by'``, and so the template
    used in our example is ``article_voted_by.html``.
    """
    select_related = 'user'
    context_votes_name = 'votes'
    template_name_suffix = '_voted_by'
    
    def get_context_votes_name(self, obj):
        """
        Get the name to use for the votes.
        """
        return self.context_votes_name
        
    def get_votes(self, obj, request):
        """
        Return a queryset of votes given to *obj*.
        """
        queryset = self.handler.get_votes_for(obj)
        if self.select_related:
            queryset = queryset.select_related(self.select_related)
        return queryset
        
    def get(self, request, **kwargs):
        self.object = self.get_object()
        self.handler = ratings.get_handler(self.object)
        self.votes = self.get_votes(self.object, request)
        kwargs = {
            'object': self.object,
            self.get_context_votes_name(self.object): self.votes,
        }
        context = self.get_context_data(**kwargs)
        response = self.render_to_response(context)
        # FIXME: try to avoid this workaround
        if hasattr(response, 'render') and callable(response.render):
            response.render()
        return response
