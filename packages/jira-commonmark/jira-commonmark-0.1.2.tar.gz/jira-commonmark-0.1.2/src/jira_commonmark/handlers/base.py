import re
from abc import ABC


class Handler(ABC):
    """
    Handles calls from parser
    """

    def __init__(self, url_base: str=None):
        self.url_base = url_base

    def line_feed(self):
        raise NotImplementedError()

    def new_paragraph(self, text):
        raise NotImplementedError()

    def sub_term_reference(self, match):
        raise NotImplementedError()

    def sub_url(self, match):
        raise NotImplementedError()

    def sub_mail(self, match):
        raise NotImplementedError()

    def sub_jira_url(self, match):
        raise NotImplementedError()

    def sub_brackets(self, match):
        return re.sub(r"[\[\]]", '', match.group(0))
