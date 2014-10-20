import slumber
API_ENDPOINT = 'http://localhost:8080/api/v1/'
API_AUTH = ("root", "root")
api = slumber.API(API_ENDPOINT, auth=API_AUTH, format='json')

class options(object):
    channel = 1
    title = 'testing api'

channel = api.channel(int(options.channel)).get()
post = api.playout.post({'title': options.title, 'channel': options.channel})

channel_id = channel['id']

sample_path = 'samples/l%ssample.wav' % channel_id
sample_path_mp3 = 'samples/l%ssample.mp3' % channel_id

sample_path = 'samples/l0sample.wav'

print 'Putting sample: %s' % sample_path

put = api.playout(post["id"]).put({'status': 2, 'sample': open(sample_path)})  
