from django import template
register = template.Library()

@register.filter
def format_image_number(value):
    return f"{value:02}"
