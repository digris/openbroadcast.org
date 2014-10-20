import datetime


def ceil_dt(dt, snap=900):
    """
    http://stackoverflow.com/questions/13071384/python-ceil-a-datetime-to-next-quarter-of-an-hour
    """
    #how many secs have passed this hour
    nsecs = dt.minute * 60 + dt.second + dt.microsecond * 1e-6
    #number of seconds to next quarter hour mark
    #Non-analytic (brute force is fun) way:
    #   delta = next(x for x in xrange(0,3601,900) if x>=nsecs) - nsecs
    #anlytic (ARGV BATMAN!, what is going on with that expression) way:
    delta = (nsecs // snap) * snap + snap - nsecs
    #time + number of seconds to quarter hour mark.
    return dt + datetime.timedelta(seconds=delta)


def round_dt(dt=None, snap=900):
    """Round a datetime object to any time laps in seconds
    dt : datetime.datetime object, default now.
    snap : Closest number of seconds to round to, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
    http://stackoverflow.com/questions/3463930/how-to-round-the-minute-of-a-datetime-object-python
    """
    if dt == None: dt = datetime.datetime.now()
    seconds = (dt - dt.min).seconds
    # // is a floor division, not a comment on following line:
    rounding = (seconds + snap / 2) // snap * snap
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)
