from django import template

register = template.Library()


@register.filter
def cell(obj, name):
    """Render attribute ``name`` of ``obj`` for a table cell (choices -> display label)."""
    display = getattr(obj, f'get_{name}_display', None)
    value = display() if callable(display) else getattr(obj, name, None)
    if callable(value):
        value = value()
    if value is None or value == '':
        return '—'
    if isinstance(value, bool):
        return 'Yes' if value else 'No'
    return value
