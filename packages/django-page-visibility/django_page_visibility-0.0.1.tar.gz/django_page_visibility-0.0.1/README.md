# django_page_visibility

This package implements a standard protocol allowing developers to ask "can user X currently access page Y?". 

Rather than duplicating the permission checks performed in that view, you ask the view itself whether or not the user can access it.

## Conforming Views

Conforming views must implement a `.test_page_visibilty(request, *args, **kwargs)` method. This will be called with the same `args` and `kwargs` that the actual view would be called with. 

This method must return a truthy value if the user can access the page, and False otherwise. It may also raise an exception, to indicate that the user cannot access the page. See `PAGE_VISIBILITY_EXCEPTIONS` below.

## The Test Function

Developers can call `django_page_visibility.is_visible_to_user(path, user)` (see the code for details) to test visibility. Or, in a template, you can use our `is_permitted_to_see` filter or `permitted_link` tag.

## `PAGE_VISIBILITY_EXCEPTIONS` setting

By default, we return `False` if either `django.http.Http404` or `django.core.exceptions.PermissionDenied` are raised. You can override this by setting (in your django settings) `PAGE_VISIBILITY_EXCEPTIONS` to a list of exception classes. 

We expect most users to override this setting. For example, if you are using `exceptional_auth` and `django_early_return`, then you'll want to set:
```python
PAGE_VISIBILITY_EXCEPTIONS = [
    'django.core.exceptions.PermissionDenied',
    'django.http.Http404',
    'django_early_return.EarlyReturn',
    'exceptional_auth.AuthException',
]
```