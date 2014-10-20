from django.views.generic import DetailView, ListView, UpdateView
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from django.template import RequestContext
from django.contrib import messages
from django.db.models import Q
from django.utils.translation import ugettext as _
from pure_pagination.mixins import PaginationMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from tagging.models import Tag
import reversion

from braces.views import PermissionRequiredMixin, LoginRequiredMixin

from alibrary.models import Label, Release
from alibrary.forms import LabelForm, LabelActionForm, LabelRelationFormSet
from alibrary.filters import LabelFilter


from lib.util import tagging_extra
from lib.util import change_message
from lib.util.form_errors import merge_form_errors



ALIBRARY_PAGINATE_BY = getattr(settings, 'ALIBRARY_PAGINATE_BY', (12,24,36,120))
ALIBRARY_PAGINATE_BY_DEFAULT = getattr(settings, 'ALIBRARY_PAGINATE_BY_DEFAULT', 12)

ORDER_BY = [
    {
        'key': 'name',
        'name': _('Name')
    },
    {
        'key': 'updated',
        'name': _('Last modified')
    },
    {
        'key': 'created',
        'name': _('Creation date')
    },
]

class LabelListView(PaginationMixin, ListView):
    
    # context_object_name = "label_list"
    #template_name = "alibrary/release_list.html"
    
    object = Label
    paginate_by = ALIBRARY_PAGINATE_BY_DEFAULT
    
    model = Release
    extra_context = {}
    
    def get_paginate_by(self, queryset):
        
        ipp = self.request.GET.get('ipp', None)
        if ipp:
            try:
                if int(ipp) in ALIBRARY_PAGINATE_BY:
                    return int(ipp)
            except Exception, e:
                pass

        return self.paginate_by

    def get_context_data(self, **kwargs):
        context = super(LabelListView, self).get_context_data(**kwargs)

        self.extra_context['filter'] = self.filter
        self.extra_context['relation_filter'] = self.relation_filter
        self.extra_context['tagcloud'] = self.tagcloud
        # for the ordering-box
        self.extra_context['order_by'] = ORDER_BY

        # active tags
        if self.request.GET.get('tags', None):
            tag_ids = []
            for tag_id in self.request.GET['tags'].split(','):
                tag_ids.append(int(tag_id))
            self.extra_context['active_tags'] = tag_ids
        #self.extra_context['release_list'] = self.filter
    
        # hard-coded for the moment
        
        self.extra_context['list_style'] = self.request.GET.get('list_style', 'm')
        #self.extra_context['list_style'] = 's'
        
        self.extra_context['get'] = self.request.GET
        
        context.update(self.extra_context)

        return context
    

    def get_queryset(self, **kwargs):

        # return render_to_response('my_app/template.html', {'filter': f})

        kwargs = {}

        self.tagcloud = None

        q = self.request.GET.get('q', None)
        
        qs = Label.objects.active()
        
        if q:
            qs = qs.filter(name__istartswith=q).distinct()
            
            
            
        order_by = self.request.GET.get('order_by', 'created')
        direction = self.request.GET.get('direction', 'descending')
        
        if order_by and direction:
            if direction == 'descending':
                qs = qs.order_by('-%s' % order_by)
            else:
                qs = qs.order_by('%s' % order_by)
            
            
            
        # special relation filters
        self.relation_filter = []
        
        label_filter = self.request.GET.get('label', None)
        if label_filter:
            qs = qs.filter(media_release__label__slug=label_filter).distinct()
            # add relation filter
            fa = Label.objects.filter(slug=label_filter)[0]
            f = {'item_type': 'label' , 'item': fa, 'label': _('Label')}
            self.relation_filter.append(f)
            
        label_filter = self.request.GET.get('label', None)
        if label_filter:
            qs = qs.filter(label__slug=label_filter).distinct()
            # add relation filter
            fa = Label.objects.filter(slug=label_filter)[0]
            f = {'item_type': 'label' , 'item': fa, 'label': _('Label')}
            self.relation_filter.append(f)
            
            

        # filter by import session
        import_session = self.request.GET.get('import', None)
        if import_session:
            from importer.models import Import
            from django.contrib.contenttypes.models import ContentType
            import_session = get_object_or_404(Import, pk=int(import_session))
            ctype = ContentType.objects.get(model='label')
            ids = import_session.importitem_set.filter(content_type=ctype.pk).values_list('object_id',)
            qs = qs.filter(pk__in=ids).distinct()

        # base queryset        
        #qs = Release.objects.all()
        
        # apply filters
        self.filter = LabelFilter(self.request.GET, queryset=qs)
        # self.filter = ReleaseFilter(self.request.GET, queryset=Release.objects.active().filter(**kwargs))
        
        qs = self.filter.qs
        
        
        
        
        stags = self.request.GET.get('tags', None)
        #print "** STAGS:"
        #print stags
        tstags = []
        if stags:
            stags = stags.split(',')
            for stag in stags:
                #print int(stag)
                tstags.append(int(stag))
        
        #print "** TSTAGS:"
        #print tstags
        
        #stags = ('Techno', 'Electronic')
        #stags = (4,)
        if stags:
            qs = Release.tagged.with_all(tstags, qs)
            
            
        # rebuild filter after applying tags
        self.filter = LabelFilter(self.request.GET, queryset=qs)
        
        # tagging / cloud generation
        tagcloud = Tag.objects.usage_for_queryset(qs, counts=True, min_count=0)
        #print '** CLOUD: **'
        #print tagcloud
        #print '** END CLOUD **'
        
        self.tagcloud = tagging_extra.calculate_cloud(tagcloud)
        
        #print '** CALCULATED CLOUD'
        #print self.tagcloud
        
        return qs



class LabelDetailView(DetailView):

    context_object_name = "label"
    model = Label
    extra_context = {}

    
    def render_to_response(self, context):
        return super(LabelDetailView, self).render_to_response(context, mimetype="text/html")
    

        
    def get_context_data(self, **kwargs):

        context = super(LabelDetailView, self).get_context_data(**kwargs)
        obj = kwargs.get('object', None)

        releases = Release.objects.filter(label=obj).order_by('-releasedate').distinct()[:8]
        self.extra_context['releases'] = releases
        self.extra_context['history'] = reversion.get_unique_for_object(obj)

        context.update(self.extra_context)

        return context

    






class LabelEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = Label
    form_class = LabelForm
    template_name = "alibrary/label_edit.html"
    permission_required = 'alibrary.change_label'
    raise_exception = True
    success_url = '#'

    def __init__(self, *args, **kwargs):
        super(LabelEditView, self).__init__(*args, **kwargs)

    def get_initial(self):
        self.initial.update({ 'user': self.request.user })
        return self.initial

    def get_context_data(self, **kwargs):
        ctx = super(LabelEditView, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        # TODO: is this a good way to pass the instance main form?
        ctx['form_errors'] = self.get_form_errors(form=ctx['form'])

        return ctx

    def get_named_formsets(self):

        return {
            'action': LabelActionForm(self.request.POST or None, prefix='action'),
            'relation': LabelRelationFormSet(self.request.POST or None, instance=self.object, prefix='relation'),
        }

    def get_form_errors(self, form=None):

        named_formsets = self.get_named_formsets()
        named_formsets.update({'form': form})
        form_errors = merge_form_errors([formset for name, formset in named_formsets.items()])

        return form_errors

    def form_valid(self, form):

        named_formsets = self.get_named_formsets()

        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save(commit=False)

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()

        msg = change_message.construct(self.request, form, [named_formsets['relation'],])
        d_tags = form.cleaned_data['d_tags']
        if d_tags:
            msg = change_message.parse_tags(obj=self.object, d_tags=d_tags, msg=msg)
            self.object.tags = d_tags


        with reversion.create_revision():
            self.object = form.save()
            reversion.set_user(self.request.user)
            reversion.set_comment(msg)

        messages.add_message(self.request, messages.INFO, msg)


        return HttpResponseRedirect('')

    def formset_relation_valid(self, formset):

        relations = formset.save(commit=False) # self.save_formset(formset, contact)
        for relation in relations:
            #relation.who = self.request.user
            #relation.contact = self.object
            relation.save()

    
# autocompleter views
# TODO: rewrite!
def label_autocomplete(request):

    q = request.GET.get('q', None)
    
    result = []
    
    if q and len(q) > 1:
        
        releases = Release.objects.filter(Q(name__istartswith=q)\
            | Q(media_release__name__icontains=q)\
            | Q(media_release__label__name__icontains=q)\
            | Q(label__name__icontains=q))\
            .distinct()
        for release in releases:
            item = {}
            item['release'] = release
            medias = []
            labels = []
            labels = []
            for media in release.media_release.filter(name__icontains=q).distinct():
                if not media in medias:
                    medias.append(media)
            for media in release.media_release.filter(label__name__icontains=q).distinct():
                if not media.label in labels:
                    labels.append(media.label)
                
            if not len(labels) > 0:
                labels = None
            if not len(medias) > 0:
                medias = None
            if not len(labels) > 0:
                labels = None

            item['labels'] = labels
            item['medias'] = medias
            item['labels'] = labels
            
            result.append(item)
        
    
    #return HttpResponse(json.dumps(list(result)))
    return render_to_response("alibrary/element/autocomplete.html", { 'query': q, 'result': result }, context_instance=RequestContext(request))
    


    
    
    
    
    
