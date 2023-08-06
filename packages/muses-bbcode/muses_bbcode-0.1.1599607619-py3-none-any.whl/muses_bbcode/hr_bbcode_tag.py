from precise_bbcode.bbcode import BBCodeTag


class HrBBCodeTag(BBCodeTag):

    def render(self, value, option=None, parent=None):
        return super().render(value=value, option=option, parent=parent)

    name = 'hr'
    definition_string = '[hr]'
    format_string = '<hr />'

    class Options:
        render_embedded = False
        strip = False
        standalone = True
