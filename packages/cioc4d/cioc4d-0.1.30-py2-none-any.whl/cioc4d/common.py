from functools import wraps
import c4d


def to_unicode(value):
    # It seems that c4d python uses utf for str objects.
    # https://plugincafe.maxon.net/topic/11943/how-to-handle-c4d-unicode-in-python-scripting
    try:
        return unicode(value)
    except UnicodeDecodeError:
        return str(value)


def show_exceptions(func):
    @wraps(func)
    def _wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            if not getattr(err, 'exception_already_shown', False):
                c4d.gui.MessageDialog('%s:\n\n%s' % (
                    err.__class__.__name__, to_unicode(err)))
            err.exception_already_shown = True
            raise
        return _wrapped
