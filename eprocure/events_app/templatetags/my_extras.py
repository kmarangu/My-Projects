from django import template

register = template.Library()

# registering method with decorators
@register.filter(name='cut')
def cut(value,arg):
    """
    This cuts out all values of "arg" from string
    """

    return value.replace(arg,'')

# registering method without decorator
# register.filter('cut',cut)
