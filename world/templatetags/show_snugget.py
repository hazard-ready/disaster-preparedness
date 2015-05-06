from django import template
from django.utils import six

register = template.Library()


class SnuggetNode(template.Node):

    def __init__(self, var_name):
        self.snugget = template.Variable(var_name)

    def render(self, context):
        """
        Renders the specified template and context. Caches the
        template object in render_context to avoid reparsing and
        loading when used in a for loop.

        A lot of this is token from django.template.base's InclusionNode.
        This behavior should be changed if we upgrade to Django 1.8.
        """
        try:
            snugget = self.snugget.resolve(context)
            file_name = snugget.getRelatedTemplate()
            context['snugget'] = snugget
        except (template.base.VariableDoesNotExist):
            return ''

        if not getattr(self, 'nodelist', False):
            from django.template.loader import get_template, select_template
            from django.utils.itercompat import is_iterable
            if isinstance(file_name, template.Template):
                t = file_name
            elif not isinstance(file_name, six.string_types) and is_iterable(file_name):
                t = select_template(file_name)
            else:
                t = get_template(file_name)
            self.nodelist = t.nodelist
        return self.nodelist.render(context)

    def get_resolved_arguments(self, context):
        """
        This function is also snipped from django.template.base.
        """
        resolved_args = [var.resolve(context) for var in self.args]
        resolved_args = [context] + resolved_args
        resolved_kwargs = {k: v.resolve(context) for k, v in self.kwargs.items()}
        return resolved_args, resolved_kwargs

    @classmethod
    def handle_token(cls, parser, token):
        bits = token.contents.split()
        if len(bits) != 2:
            raise template.TemplateSyntaxError(
                "show_snugget tag takes exactly one argument")

        snugget = bits[1]
        return cls(snugget)


@register.tag
def show_snugget(parser, token):
    return SnuggetNode.handle_token(parser, token)
