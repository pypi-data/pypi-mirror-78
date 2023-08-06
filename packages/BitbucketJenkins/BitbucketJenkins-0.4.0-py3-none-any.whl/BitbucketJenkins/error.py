from decorator import decorator

class GenericException(Exception):
    def __init__(self, response):
        try:
            self.data = response.json()
            msg = "%d: %s" % (response.status_code, self.data)
        except ValueError:
            msg = "Unknown error: %d(%s)" % (response.status_code, response.reason)

        super(GenericException, self).__init__(msg)

def maybe_throw(response):
    if not response.ok:
        e = GenericException(response)
        try:
            e.data = response.json()
        except ValueError:
            e.content = response.content
        raise e

@decorator
def error(fn, *args, **kw):
    response = fn(*args, **kw)
    maybe_throw(response)
    return response.ok