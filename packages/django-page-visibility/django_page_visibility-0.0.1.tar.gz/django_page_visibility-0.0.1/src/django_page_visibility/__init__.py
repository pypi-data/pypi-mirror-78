from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test.client import RequestFactory
from django.urls import resolve
from django.urls.exceptions import Resolver404
from django.utils.module_loading import import_string

factory = RequestFactory()

def get_exceptions():
    return [
        import_string(e) if isinstance(e, str) else e
        for e in getattr(settings, 'PAGE_VISIBILITY_EXCEPTIONS', (PermissionDenied, Http404))
    ]
# Note - except clauses only take tuples of exceptions, not lists
EXCEPTIONS = tuple(get_exceptions())

class PageVisibilityError(Exception):
    '''
        Base class for all of the exceptions we raise
    '''
    pass
class ViewDoesNotSupportVisibilityTest(PageVisibilityError):
    pass
class LinkPathDoesNotExist(PageVisibilityError):
    pass

def is_visible_to_user(path, user, raise_exceptions=settings.DEBUG):
    '''
        Checks whether the given user is allowed to make a GET request to the given path.
    '''

    try :
        func, args, kwargs = resolve(path)
    except Resolver404 :
        if not raise_exceptions :
            return False
        raise LinkPathDoesNotExist(f'Link path {path} does not exist')

    '''
        Notice - this funtion is meant to work with special views that have an added "test_page_visibility" attribute.

        This attribute should be a function which takes the same parameters as the view itself, and returns a truthy value if the user can access the page.

        If the user is not allowed to access the page, the test function may either return a falsey value, or raise an exception.
    '''
    try :
        visibility_test = func.test_page_visibility
    except AttributeError :
        if not raise_exceptions :
            return False
        raise ViewDoesNotSupportVisibilityTest(f'Path {path} resolved to view function {func} which does implement test_page_visibility()')

    request = factory.get(path)
    request.user = user

    try :
        return visibility_test(request, *args, **kwargs) != False
    except EXCEPTIONS :
        return False
    return True

def is_visible(path, request, *args, **kwargs):
    '''
        Convenience wrapper around is_visible_to_user, which will cover most use cases
    '''
    return is_visible_to_user(path, request.user, *args, **kwargs)
