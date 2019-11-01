from django.utils.translation import gettext
from django.template import Library

register = Library()
@register.filter()
def show_cost(cost):
  return {
        0: gettext('Free!'),
        1: '$',
        2: '$$',
        3: '$$$',
        4: '$$$$'
    }.get(cost, gettext('Unknown'))

@register.filter()
def show_cost_header(cost):
  return {
        0: gettext('Get Started - It’s Free!'),
        1: gettext('Next Steps'),
        2: gettext('Keep Going'),
        3: '$$$',
        4: '$$$$'
    }.get(cost, gettext('Unknown'))