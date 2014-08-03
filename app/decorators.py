# =======================================================================================
# Copyright 2014 Matt Clyde, Shawn Forgie, Blake Wellington
# Licensed under GPL v2 (https://github.com/mclyde/HousePlantMonitor/blob/master/LICENSE)
# =======================================================================================

from threading import Thread

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper