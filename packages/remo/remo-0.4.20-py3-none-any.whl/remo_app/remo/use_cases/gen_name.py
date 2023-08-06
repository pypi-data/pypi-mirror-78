import re

from typing import List


def gen_unique_name(name: str, names: List[str]) -> str:
    if not names:
        return name
    
    rgx = re.compile(rf'^{name} \(([\d]+)\)$')
    results = list(map(lambda a: int(a[0]), filter(bool, map(rgx.findall, names))))
    max_val = 0
    if results:
        max_val = max(results)
    return f'{name} ({max_val + 1})'
