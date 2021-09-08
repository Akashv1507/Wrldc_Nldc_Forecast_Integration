import datetime as dt
from colored import fg, attr


def printWithTs(printStr, clr=None):
    attrStr = ''
    fgStr = ''
    if clr != None:
        fgStr = fg(clr)
        attrStr = attr('reset')
    print('{0}{1}: {2}{3}'.format(fgStr, dt.datetime.strftime(
        dt.datetime.now(), '%Y-%b-%d %H:%M:%S'), printStr, attrStr))