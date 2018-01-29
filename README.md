# Open Broadcast - Platform
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fdigris%2Fopenbroadcast.org.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fdigris%2Fopenbroadcast.org?ref=badge_shield)





## mysql 2 pg

./manage.py dumpdata \
auth \
sites \
contenttypes \
--indent 4 --natural-foreign --natural-primary \
-o ../db/01-base.json

./manage.py dumpdata \
-e tagging \
-e auth \
-e sites \
-e contenttypes \
-e djcelery \
-e obp_legacy \
--indent 4 --natural-foreign --natural-primary \
-o ../db/dump.json




## migration steps (empty db)
./manage.py migrate auth --no-initial-data
./manage.py migrate invitation --no-initial-data
./manage.py migrate sites --no-initial-data
./manage.py migrate contenttypes --no-initial-data



./manage.py migrate --no-initial-data



## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fdigris%2Fopenbroadcast.org.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fdigris%2Fopenbroadcast.org?ref=badge_large)