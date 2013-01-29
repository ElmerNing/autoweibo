""" some rule fuction for filter post"""

def bigger_than(thr):
    """return a fuction which is comparing with thr. """
    def wrap(var):
        return int(var) > thr
    return wrap