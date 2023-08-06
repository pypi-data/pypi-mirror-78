from precise_bbcode.bbcode import BBCodeTag


class JustifierBBCodeTag(BBCodeTag):

    def render(self, value, option=None, parent=None):
        return super().render(value=value, option=option, parent=parent)

    name = 'justifier'
    definition_string = '[justifier]{TEXT}[/justifier]'
    format_string = '<p style="text-align:justify">{TEXT}</p>'

    class Options:
        render_embedded = False
        strip = False
        end_tag_closes = True
