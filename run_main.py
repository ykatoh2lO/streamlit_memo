import sys
from pathlib import Path
import tomllib

import streamlit.web.cli as stcli

from gui.utils import HOME_DIR


def parse_config_to_argv():
    with open(HOME_DIR / '.streamlit' / 'config.toml', 'rb') as f:
        config_data = tomllib.load(f)

    return [
        f'--{table_name}.{key}={str(val).lower() if isinstance(val, bool) else val}'
        for table_name, table_data in config_data.items() for key, val in table_data.items()]

def streamlit_run():
    sys.argv = ['streamlit', 'run', HOME_DIR / 'main.py'] + parse_config_to_argv()
    sys.exit(stcli.main())

if __name__ == '__main__':
    streamlit_run()
