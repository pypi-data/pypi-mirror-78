from precise_bbcode.bbcode import BBCodeTag


class InvisibleBBCodeTag(BBCodeTag):

    def render(self, value, option=None, parent=None):
        return super().render(value=value, option=option, parent=parent)

    name = 'invisible'
    definition_string = '[invisible]{TEXT}[/invisible]'
    format_string = '<span style:"display:none">{TEXT}</span>'

    class Options:
        render_embedded = False
        strip = False
        end_tag_closes = True
