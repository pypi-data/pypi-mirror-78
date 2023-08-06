from functools import wraps

class Migration:
    def __init__(self, slug, sort_key, fn):
        self.slug = slug
        self.sort_key = sort_key
        self._fn = fn

    def __call__(self, *args, **kwargs):
        return self._fn(*args, **kwargs)

def migration(slug, *, sort_key):
    def wrapper(fn):
        return wraps(fn)(Migration(slug, sort_key, fn))
    return wrapper
