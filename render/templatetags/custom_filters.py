from django import template
register = template.Library()

@register.filter
def format_image_number(value):
    return f"{value:02}"

@register.filter
def filter_correct_evaluation(queryset, evaluation):
    return queryset.filter(correct_evaluation=evaluation)
