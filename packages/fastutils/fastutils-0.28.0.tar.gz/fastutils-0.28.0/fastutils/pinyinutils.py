from dragonmapper import hanzi
import string

from . import strutils


def to_pinyin(value, clean=True, clean_chars=string.ascii_letters):
    title = hanzi.to_pinyin(value, accented=False)
    return strutils.camel(title, clean=clean, clean_chars=clean_chars)
