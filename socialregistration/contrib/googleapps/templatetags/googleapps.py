from django import template

register = template.Library()

@register.inclusion_tag('socialregistration/googleapps/form.html', takes_context=True)
def googleapps_form(context, domain=None, button=None):
    return {
        'domain': domain,
        'button': button,
        'request': context['request']
    }

