import re
from datetime import date

QUOTE_PATTERN = re.compile(r'> (.*?)')
SECTION_PATTERN = re.compile(
    r'## (.*?): (\d{3,5}) 字以内\n\n> \[\!info\]\+\n(.*?)\n\n```txt\n(.*?)\n```\n(\n---\n)?',
    re.MULTILINE | re.DOTALL)
TODAY = date.today()


def get_fiscal_year():
    if TODAY.month >= 4:
        return TODAY.year
    else:
        return TODAY.year - 1

def get_yyyymmdd():
    return TODAY.strftime('%Y%m%d')
