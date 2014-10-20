# TODO: these two lines kill everything?
#from actstream.models import Follow
#from actstream.models import user_stream as ac_user_stream
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.template import Variable, Library, Node, TemplateSyntaxError
from django.template.base import TemplateDoesNotExist
from django.template.loader import render_to_string, find_template


register = Library()


def _is_following_helper(context, actor):
    from actstream.models import Follow
    return Follow.objects.is_following(context.get('user'), actor)


class DisplayActivityFollowUrl(Node):
    def __init__(self, actor, actor_only=True):
        self.actor = Variable(actor)
        self.actor_only = actor_only

    def render(self, context):
        actor_instance = self.actor.resolve(context)

        try:
            content_type = ContentType.objects.get_for_model(actor_instance).pk
            from actstream.models import Follow
            if Follow.objects.is_following(context.get('user'), actor_instance):
                return reverse('actstream_unfollow', kwargs={
                    'content_type_id': content_type, 'object_id': actor_instance.pk})
            if self.actor_only:
                return reverse('actstream_follow', kwargs={
                    'content_type_id': content_type, 'object_id': actor_instance.pk})
            return reverse('actstream_follow_all', kwargs={
                'content_type_id': content_type, 'object_id': actor_instance.pk})
        except:
            pass


class DisplayActivityActorUrl(Node):
    def __init__(self, actor):
        self.actor = Variable(actor)

    def render(self, context):
        actor_instance = self.actor.resolve(context)
        content_type = ContentType.objects.get_for_model(actor_instance).pk
        return reverse('actstream_actor', kwargs={
            'content_type_id': content_type, 'object_id': actor_instance.pk})


class AsNode(Node):
    """
    Base template Node class for template tags that takes a predefined number
    of arguments, ending in an optional 'as var' section.
    """
    args_count = 1

    @classmethod
    def handle_token(cls, parser, token):
        """
        Class method to parse and return a Node.
        """
        bits = token.split_contents()
        args_count = len(bits) - 1
        if args_count >= 2 and bits[-2] == 'as':
            as_var = bits[-1]
            args_count -= 2
        else:
            as_var = None
        if args_count != cls.args_count:
            arg_list = ' '.join(['[arg]' * cls.args_count])
            raise TemplateSyntaxError("Accepted formats {%% %(tagname)s "
                "%(args)s %%} or {%% %(tagname)s %(args)s as [var] %%}" %
                {'tagname': bits[0], 'args': arg_list})
        args = [parser.compile_filter(token) for token in
            bits[1:args_count + 1]]
        return cls(args, varname=as_var)

    def __init__(self, args, varname=None):
        self.args = args
        self.varname = varname

    def render(self, context):
        result = self.render_result(context)
        if self.varname is not None:
            context[self.varname] = result
            return ''
        return result

    def render_result(self, context):
        raise NotImplementedError("Must be implemented by a subclass")


class DisplayAction(AsNode):

    def render_result(self, context, timestamped=False):
        action_instance = self.args[0].resolve(context)
        templates = [
            'actstream/%s/action.html' % action_instance.verb.replace(' ', '_'),
            'actstream/action.html',
            'activity/%s/action.html' % action_instance.verb.replace(' ', '_'),
            'activity/action.html',
        ]
        return render_to_string(templates, {'action': action_instance, 'timestamped': timestamped},
            context)


def display_action(parser, token):
    """
    Renders the template for the action description

    Example::

        {% display_action action %}
    """
    return DisplayAction.handle_token(parser, token)


def display_timestamped_action(parser, token, timestamped=True):
    """
    Renders the template for the action description

    Example::

        {% display_timestamped_action action %}
    """
    return DisplayAction.handle_token(parser, token)


def is_following(user, actor):
    """
    Returns true if the given user is following the actor

    Example::

        {% if request.user|is_following:another_user %}
            You are already following {{ another_user }}
        {% endif %}
    """
    from actstream.models import Follow
    try:
        return Follow.objects.is_following(user, actor)
    except:
        pass


def follow_url(parser, token):
    """
    Renders the URL of the follow view for a particular actor instance

    Example::

        <a href="{% follow_url other_user %}">
            {% if request.user|is_following:other_user %}
                stop following
            {% else %}
                follow
            {% endif %}
        </a>
    """
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError("Accepted format {% follow_url [instance] %}")
    else:
        return DisplayActivityFollowUrl(bits[1])


def follow_all_url(parser, token):
    """
    Renders the URL to follow an object as both actor and target

    Example::

        <a href="{% follow_all_url other_user %}">
            {% if request.user|is_following:other_user %}
                stop following
            {% else %}
                follow
            {% endif %}
        </a>
    """
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError("Accepted format {% follow_all_url [instance] %}")
    else:
        return DisplayActivityFollowUrl(bits[1], actor_only=False)


def actor_url(parser, token):
    """
    Renders the URL for a particular actor instance

    Example::

        <a href="{% actor_url request.user %}">View your actions</a>
        <a href="{% actor_url another_user %}">{{ another_user }}'s actions</a>

    """
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError("Accepted format "
                                  "{% actor_url [actor_instance] %}")
    else:
        return DisplayActivityActorUrl(*bits[1:])

register.filter(is_following)
register.tag(display_action)
register.tag(display_timestamped_action)
register.tag(follow_url)
register.tag(follow_all_url)
register.tag(actor_url)

@register.filter
def backwards_compatibility_check(template_name):
    backwards = False
    try:
        find_template('actstream/action.html')
    except TemplateDoesNotExist:
        backwards = True
    if backwards:
        template_name = template_name.replace('actstream/', 'activity/')
    return template_name




@register.inclusion_tag('actstream/templatetags/user_stream.html', takes_context=True)
def user_stream(context, user):
    from actstream.models import user_stream as ac_user_stream
    stream = ac_user_stream(user)[0:15]
    context.update({'stream': stream})
    return context

@register.filter
def user_stream_count(user):
    from actstream.models import user_stream as ac_user_stream
    return ac_user_stream(user).count()

