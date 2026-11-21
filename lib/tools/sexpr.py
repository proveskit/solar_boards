"""Minimal reader for KiCad S-expression files."""

import re

_TOKEN = re.compile(r'\s*(?:(\()|(\))|"((?:[^"\\]|\\.)*)"|([^\s()"]+))')


class Sym(str):
    """A bare (unquoted) atom, kept apart from quoted strings."""


def parse(text):
    stack, cur, pos = [], [], 0
    while True:
        m = _TOKEN.match(text, pos)
        if not m or m.end() == pos:
            break
        pos = m.end()
        if m.group(1):
            stack.append(cur)
            cur = []
        elif m.group(2):
            done, cur = cur, stack.pop()
            cur.append(done)
        elif m.group(3) is not None:
            cur.append(m.group(3).replace('\\"', '"').replace("\\\\", "\\"))
        else:
            cur.append(Sym(m.group(4)))
    return cur[0]


def children(node, tag):
    return [c for c in node if isinstance(c, list) and c and c[0] == tag]


def child(node, tag):
    found = children(node, tag)
    return found[0] if found else None


def value(node, tag, default=None):
    c = child(node, tag)
    return c[1] if c and len(c) > 1 else default


def prop(node, name):
    for p in children(node, "property"):
        if p[1] == name:
            return p[2]
    return None
