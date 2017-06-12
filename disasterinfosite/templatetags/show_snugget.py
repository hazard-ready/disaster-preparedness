from django import template

register = template.Library()


class SnuggetNode(template.Node):

    def __init__(self, var_name):
        self.snugget = template.Variable(var_name)

    def render(self, context):
        """
        Renders the right snugget template.
        """
        try:
            snugget = self.snugget.resolve(context)
            file_name = snugget.getRelatedTemplate()
            context['snugget'] = snugget
            t = context.template.engine.get_template(file_name)
            return t.render(context)
        except (template.base.VariableDoesNotExist):
            return ''

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
