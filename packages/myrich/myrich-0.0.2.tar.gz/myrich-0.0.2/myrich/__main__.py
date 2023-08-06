#!/usr/bin/env python
# coding: utf-8

# Execute with
# $ python myrich/__main__.py (2.6+)
# $ python -m myrich          (2.7+)

import sys

if __package__ is None and not hasattr(sys, "frozen"):
    # direct call of __main__.py
    import os.path

    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

import myrich

if __name__ == "__main__":
    myrich.main()
