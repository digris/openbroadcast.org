from django.core.management.base import BaseCommand, make_option

from ratings import models

class Command(BaseCommand):
    """
    Create or update all scores, based on existing votes.
    This is useful if you have to migrate your votes from a legacy table,
    or you want to change the weight of current votes, e.g.::
    
        ./manage.y upsert_scores -w 5
    """
    option_list = BaseCommand.option_list + (
        make_option('-w', "--weight", 
            action='store', dest='weight', default=0, type='int',
            help=('The weight used to calculate average score.')
        ),
    )
    help = "Create or update all scores, based on existing votes."

    def handle(self, **options):
        if int(options.get('verbosity')) > 0:
            verbose = True
            counter = 0
        buffer = set()
        for vote in models.Vote.objects.all():
            content = (vote.content_type, vote.object_id, vote.key)
            if content not in buffer:
                if verbose:
                    counter += 1
                    print u'#%d - model %s id %s key %s' % ((counter,) + content)
                models.upsert_score(content[:2], content[2], options['weight'])
                buffer.add(content)
