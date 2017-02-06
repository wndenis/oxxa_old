from datetime import datetime

def plog(msg):
    time = datetime.now()
    dt, mt = time.day, time.month
    h, m, s = time.hour, time.minute, time.second
    time = "%s.%s %s:%s:%s " % (dt, mt, h, m, s)
    if s < 10:
        time += ' '
    if m < 10:
        time += ' '
    if h < 10:
        time += ' '
    if dt < 10:
        time += ' '
    if mt < 10:
        time += ' '
    time += "| "
    print(time + msg)
