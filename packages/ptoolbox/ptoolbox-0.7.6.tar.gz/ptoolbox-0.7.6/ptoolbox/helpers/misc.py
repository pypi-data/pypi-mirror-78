# coding=utf-8
import logging

__author__ = 'ThucNC'

from unidecode import unidecode

_logger = logging.getLogger(__name__)


def make_slug(s):
    s = unidecode(s).lower()
    s2 = ""
    for c in s:
        if c.isalnum():
            s2 += c
        else:
            s2 += " "

    return "-".join(s2.split())


def make_problem_code(name):
    name = make_slug(name)
    name = name.strip(" _").replace("-", "_")
    if '0' <= name[0] <= '9':
        name = "p" + name
    return name