#!/usr/bin/env python

"""`jict` provides dictionaries with multiple levels of nested-ness."""

__version__ = '2.5'
from .jict import jict, sqlconnect
from .helpers import evaluate
from collections import deque

try:
    import urwid
    from .menu import jictmt
except Exception as e:
    class jictmt:
        def __init__(self):
            super(jictmt, self).__init__()
            print( 'jictmt requires urwid, install by pip3 install urwid' )

__all__ = ( 'jict', 'sqlconnect', 'evaluate', 'deque', 'jictmt' )
