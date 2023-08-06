from precise_bbcode.bbcode import BBCodeTag


class RightBBCodeTag(BBCodeTag):

    def render(self, value, option=None, parent=None):
        return super().render(value=value, option=option, parent=parent)

    name = 'right'
    definition_string = '[right]{TEXT}[/right]'
    format_string = '<div align="right">{TEXT}</div>'

    class Options:
        render_embedded = False
        strip = False
        end_tag_closes = True
