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

        A lot of this is taken from django.template.base's InclusionNode, for Django 1.8.6.
        Upgrading Django should mean updating this to match.
        """
        try:
            snugget = self.snugget.resolve(context)
            file_name = snugget.getRelatedTemplate()
            context['snugget'] = snugget
        except (template.base.VariableDoesNotExist):
            return ''

        from django.utils.itercompat import is_iterable
        if isinstance(file_name, template.Template):
            t = file_name
        elif isinstance(getattr(file_name, 'template', None), template.Template):
            t = file_name.template
        elif not isinstance(file_name, six.string_types) and is_iterable(file_name):
            t = context.template.engine.select_template(file_name)
        else:
            t = context.template.engine.get_template(file_name)
        context.render_context[self] = t
        return t.render(context)

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
