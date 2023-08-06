from typing import List


def table(headers: List[str], rows: List[List[str]]):
    columns_width = [len(val) for val in headers]

    for row in rows:
        for i, val in enumerate(row):
            columns_width[i] = max(columns_width[i], len(val))

    columns_width = list(map(lambda x: x + 2, columns_width))

    lines = [
        [f' {val:{width - 1}s}' for width, val in zip(columns_width, headers)],
        ['=' * width for width in columns_width]
    ]
    for row in rows:
        lines.append([f' {val:{width - 1}s}' for width, val in zip(columns_width, row)])

    return '\n'.join(map('|'.join, lines))
