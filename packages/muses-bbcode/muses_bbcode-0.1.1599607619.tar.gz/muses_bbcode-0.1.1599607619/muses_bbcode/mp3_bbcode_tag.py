from precise_bbcode.bbcode import BBCodeTag


class Mp3BBCodeTag(BBCodeTag):

    def render(self, value, option=None, parent=None):
        return super().render(value=value, option=option, parent=parent)

    name = 'mp3'
    definition_string = '[mp3]{URL}[/mp3]'
    format_string = '<audio controls src=\"{URL}\">Your browser does not support the <code>audio</code> ' \
                    'element.</audio>'

    class Options:
        render_embedded = False
        strip = False
        replace_links = False
        end_tag_closes = True
