import re

from jira_commonmark.handlers.base import Handler


class HTMLRenderer(Handler):
    """
    Render HTML
    """

    def __init__(self, url_base: str=None, internal_hosts: list=None):
        super().__init__(url_base=url_base, internal_hosts=internal_hosts)

    def new_paragraph(self, text: str):
        return "<p>\n" + text + "</p>" + self.line_feed()

    def line_feed(self):
        return "\n\n"

    def start_unordered_list(self):
        return "<ul>\n"

    def end_unordered_list(self):
        return "</ul>\n"

    def start_ordered_list(self):
        return "<ol>\n"

    def end_ordered_list(self):
        return "</ol>\n"

    def sub_unordered_listitem(self, match):
        return re.sub(r"[\-](\s+)?", '<li>', match.group(), count=1) + "</li>"

    def sub_ordered_listitem(self, match):
        return re.sub(r"[0-9]\.(\s+)?", '<li>', match.group(), count=1) + "</li>"

    def sub_term_reference(self, match):
        if self.url_base:
            return f"<a href={self.url_base}/{match.group(3)}>{match.group(1)}</a>"
        else:
            return f"<a href={match.group(2)}{match.group(3)}>{match.group(1)}</a>"

    def sub_url(self, match):
        if self._is_internal_address(match.group()):
            return f'<INTERN LENKE>'
        else:
            return f'<a href={match.group()}>{match.group()}</a>'

    def sub_mail(self, match):
        return f'<a href=mailto:{match.group()}>{match.group()}</a>'

    def sub_jira_url(self, match):
        return f"<a href={match.group(1)}>{match.group(1)}</a>"
