from django import template

from django_page_visibility import is_visible_to_user

register = template.Library()

class PermittedLinkNode(template.Node):
    '''
        Node for use with permitted_link tag
    '''
    DELETE = object()
    def __init__(self, path, name, nodelist):
        self.path = path
        self.name = name
        self.nodelist = nodelist
    def render(self, context):
        path = self.path.resolve(context)
        name = self.name
        if not is_visible_to_user(path, context.request.user) :
            return ''

        original_value = context.get(name, self.DELETE)
        context[name] = path
        ret = self.nodelist.render(context)

        if original_value == self.DELETE :
            del(context[name])
        else :
            context[name] = original_value
        return ret
@register.tag
def permitted_link(parser, token):
    '''
        Checks if the passed url path is visible to the current user.
        If it is, the contents of the tag are rendered, and the url path is put in context as "link".
        If not, contents are not rendered.

        usage:

        {% load page_visibility %}
        {% permitted_link "/protected_page/" %}
            <a href="{{link}}">Protected Page</a>
        {% end_permitted_link %}

        or:

        {% load page_visibility %}
        {% permitted_link "/protected_page/" as some_other_name %}
            <a href="{{some_other_name}}">Fake Permission Test</a>
        {% end_permitted_link %}
    '''
    bits = token.split_contents()
    if len(bits) == 2 :
        path = bits[1]
        name = 'link'
    elif len(bits) == 4 and bits[2] == 'as' :
        path = bits[1]
        name = bits[3]
    else :
        raise template.TemplateSyntaxError(
            f'{bits[0]} requires a single argument, or {{% {bits[0]}  "path" as my_link %}} syntax'
        )
    path = template.Variable(path)
    nodelist = parser.parse(('end_permitted_link',))
    parser.delete_first_token()
    return PermittedLinkNode(path, name, nodelist)

@register.filter
def is_permitted_to_see(user, path):
    '''
        usage:

        {% load page_visibility %}
        {% url 'protected_page' as path %}
        {% if request.user|is_permitted_to_see:path %}
            <a href="{{path}}">Protected Page</a>
        {% endif %}
    '''
    return is_visible_to_user(path, user)