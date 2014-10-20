# Channel: Radio X 
l2 = input.http(id='inl2',poll_delay=5.,autostart=true,'http://mp3.radiox.ch/standard.mp3')
l2 = mksafe(l2)
l2 = rewrite_metadata(insert_missing=true,[("channel","2")],l2)
output.dummy(l2)
l2sample = output.file.wav(id='l2rec',start=false,'samples/l2sample.wav', l2)



# Channel: obp 
l1 = input.http(id='inl1',poll_delay=5.,autostart=true,'http://stream2.openbroadcast.org:80/openbroadcast')
l1 = mksafe(l1)
l1 = rewrite_metadata(insert_missing=true,[("channel","1")],l1)
output.dummy(l1)
l1sample = output.file.wav(id='l1rec',start=false,'samples/l1sample.wav', l1)



