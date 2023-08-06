from precise_bbcode.bbcode import get_parser
from precise_bbcode.tag_pool import tag_pool
from .email_bbcode_tag import EmailBBCodeTag
from .invisible_bbcode_tag import InvisibleBBCodeTag
from .right_bbcode_tag import RightBBCodeTag
from .justifier_bbcode_tag import JustifierBBCodeTag
from .preformatted_bbcode_tag import PreFormattedBBCodeTag
from .mp3_bbcode_tag import Mp3BBCodeTag
from .br_bbcode_tag import BrBBCodeTag
from .hr_bbcode_tag import HrBBCodeTag

tag_pool.register_tag(EmailBBCodeTag)
tag_pool.register_tag(InvisibleBBCodeTag)
tag_pool.register_tag(RightBBCodeTag)
tag_pool.register_tag(JustifierBBCodeTag)
tag_pool.register_tag(PreFormattedBBCodeTag)
tag_pool.register_tag(Mp3BBCodeTag)
tag_pool.register_tag(BrBBCodeTag)
tag_pool.register_tag(HrBBCodeTag)


def bbcode2html(text):
    parser = get_parser()
    return parser.render(text)
