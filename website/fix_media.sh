import time
from alibrary.models import Media


mfix = Media.objects.filter(processed=99)

print 'num media to fix %s' % mfix.count()


for m in mfix[0:10000]:
    print 'fixing: %s - %s' % (m.pk, m)
    m.processed = 0
    m.conversion_status = 0
    m.save()
    time.sleep(1)