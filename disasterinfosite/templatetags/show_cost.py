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