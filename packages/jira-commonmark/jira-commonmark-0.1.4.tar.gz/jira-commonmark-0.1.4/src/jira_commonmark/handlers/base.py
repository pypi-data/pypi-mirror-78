import re
from abc import ABC
from urllib3 import util


class Handler(ABC):
    """
    Handles calls from parser
    """

    def __init__(self, url_base: str=None, internal_hosts: list=None):
        self.url_base = url_base
        if not internal_hosts:
            self.internal_hosts = []
        else:
            self.internal_hosts = internal_hosts

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

    def _is_internal_address(self, url):
        host = util.parse_url(url).host
        for internal_host in self.internal_hosts:
            if internal_host in host:
                return True
        return False
