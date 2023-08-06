from jira_commonmark.handlers.base import Handler


class TextRenderer(Handler):

    def __init__(self, url_base: str=None, internal_hosts: list=None):
        super().__init__(url_base=url_base, internal_hosts=internal_hosts)

    def new_paragraph(self, text: str):
        return text

    def line_feed(self):
        return "\n"

    def sub_term_reference(self, match):
        return f"{match.group(1)}"

    def sub_url(self, match):
        if self._is_internal_address(match.group()):
            return '<INTERN LENKE>'
        else:
            return f"{match.group()}"

    def sub_mail(self, match):
        return f"{match.group()}"

    def sub_jira_url(self, match):
        if match.group(1) == match.group(2):
            return f"{match.group(1)}"
        else:
            return f"{match.group(1)}: {match.group(2)}"

    def sub_link(self, match):
        return f"{match.group(1)}"
