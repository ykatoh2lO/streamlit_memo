import sys
from dataclasses import dataclass, field, InitVar
from pathlib import Path
from tempfile import NamedTemporaryFile


from src.utils import QUOTE_PATTERN, SECTION_PATTERN


@dataclass
class Section:
    question: str
    str_maxchar: InitVar[str]
    quoted_info: InitVar[str]
    answer_before: str
    suffix: InitVar[str]
    caption: str = field(init=False)
    maxchar: int = field(init=False)
    info: str = field(init=False)
    answer_after: str = field(init=False)
    has_hr: bool = field(init=False)

    def __init__(self, question, str_maxchar, quoted_info, answer_before, suffix):
        self.question = question
        self.caption = question.split('（')[0]
        self.maxchar = int(str_maxchar)
        self.info = QUOTE_PATTERN.sub('', quoted_info)
        self.answer_before = answer_before
        self.answer_after = ''
        self.has_hr = (suffix != '')

    def dump(self):
        quoted_info = '\n'.join(['> [!info]+'] + [f'> {row}' for row in self.info.split('\n')])
        answer_after = '\n'.join(['```txt', self.answer_after.rstrip(), '```'])
        # suffix = '\n\n---' if self.has_hr else ''
        return '\n\n'.join([
            f'## {self.question}: {self.maxchar} 字以内',
            quoted_info,
            answer_after  # + suffix
        ])


def read_md_file(kaonavi_md_file):
    if kaonavi_md_file is None:
        kaonavi_md_path = Path(sys.argv[0]).parent.absolute() / 'src' / 'kaonavi_template.md'
    else:
        with NamedTemporaryFile(delete=False) as tmp_file:
            fp = Path(tmp_file.name)
            fp.write_bytes(kaonavi_md_file.getvalue())
            kaonavi_md_path = tmp_file.name
    #
    with open(kaonavi_md_path, encoding='utf8') as f:
        lst_section_raw = SECTION_PATTERN.findall(f.read())
        return [Section(*tpl_section) for tpl_section in lst_section_raw]


def dump_md_file(title, lst_section):
    return '\n\n'.join([f'# {title}'] + [section.dump() for section in lst_section]) + '\n'
