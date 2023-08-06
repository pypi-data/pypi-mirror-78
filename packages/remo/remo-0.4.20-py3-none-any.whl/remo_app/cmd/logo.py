import platform

from remo_app import __version__


def logo_msg(msg: str) -> str:
    return f"""    (\\(\\
    (>':')  {msg}"""


system_logo = (f"""
===============================================
{logo_msg(f'Remo: v{__version__}')}
===============================================
Python: {platform.python_version()}, {platform.platform()}
""")
