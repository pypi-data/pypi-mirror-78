from precise_bbcode.bbcode import BBCodeTag


class EmailBBCodeTag(BBCodeTag):

    def render(self, value, option=None, parent=None):
        return super().render(value=value, option=option, parent=parent)

    name = 'email'
    definition_string = '[email]{EMAIL}[/email]'
    format_string = '<a href="mailto:{EMAIL}">{EMAIL}</a>'

    class Options:
        render_embedded = False
        strip = False
        end_tag_closes = True