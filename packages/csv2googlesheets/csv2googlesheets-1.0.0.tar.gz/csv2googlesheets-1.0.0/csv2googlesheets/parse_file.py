"""This module contains some helper functions."""

import os
import sys

from typing import List


def parse_file(path: str, delim: str = ',') -> List[List[str]]:
    """Read data from delim-delimited file and insert data into list."""
    values = []
    with open(path, 'r', encoding='utf-8') as fromF:
        for line in fromF:
            values.append(line.strip().split(delim))
    if not values:
        sys.exit(f'Failed to extract any data from {path}')
    return values


def build_spreadsheet_title(filename: str) -> str:
    """Return file name without full path and extension."""
    _, tail = os.path.split(filename)
    head, _ = os.path.splitext(tail)
    if not head:
        sys.exit(f'Failed to built title for {filename}.')
    return head
