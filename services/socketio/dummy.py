import redis
import json
import string
import random
import time

rs = redis.StrictRedis()


while True:

    names = ['peter', 'johannes', 'klaus', 'root']

    num = random.randint(5,45)

    str = ''.join(random.choice((string.whitespace *3) + string.ascii_lowercase) for x in range(num))

    rs.publish('push_chat', json.dumps({'type': 'message', 'comment': '%s' % str, 'user': '%s' % random.choice(names)}))
    print 'sleep %s' % num
    time.sleep(num/20)
    time.sleep(5.5)
    
