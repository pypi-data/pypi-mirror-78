from precise_bbcode.bbcode import BBCodeTag


class BrBBCodeTag(BBCodeTag):

    def render(self, value, option=None, parent=None):
        return super().render(value=value, option=option, parent=parent)

    name = 'br'
    definition_string = '[br]'
    format_string = '<br />'

    class Options:
        render_embedded = False
        strip = False
        standalone = True
