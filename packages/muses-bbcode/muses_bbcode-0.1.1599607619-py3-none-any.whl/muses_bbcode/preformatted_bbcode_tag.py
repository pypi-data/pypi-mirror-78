from precise_bbcode.bbcode import BBCodeTag


class PreFormattedBBCodeTag(BBCodeTag):
    def render(self, value, option=None, parent=None):
        return super().render(value=value, option=option, parent=parent)

    name = 'preformatted'
    definition_string = '[pre]{TEXT}[/pre]'
    format_string = '<pre>{TEXT}</pre>'

    class Options:
        render_embedded = False
        strip = False
        end_tag_closes = True
