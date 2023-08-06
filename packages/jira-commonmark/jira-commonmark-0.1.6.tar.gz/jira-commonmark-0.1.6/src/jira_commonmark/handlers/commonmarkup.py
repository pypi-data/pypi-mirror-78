from jira_commonmark.handlers.base import Handler


class CommonMarkRenderer(Handler):
    """
    Render CommonMarkup
    """

    def __init__(self, url_base: str=None, internal_hosts: list=None):
        super().__init__(url_base=url_base, internal_hosts=internal_hosts)

    def new_paragraph(self, text: str):
        return text + self.line_feed()

    def line_feed(self):
        return "\n\n"

    def sub_term_reference(self, match):
        if self.url_base:
            return f"[{match.group(1)}]({self.url_base}/{match.group(3)})"
        else:
            return f"[{match.group(1)}]({match.group(2)}{match.group(3)})"

    def sub_url(self, match):
        if self._is_internal_address(match.group()):
            return '<INTERN LENKE>'
        else:
            return f"[{match.group()}]({match.group()})"

    def sub_mail(self, match):
        return f"<mailto:{match.group()}>"

    def sub_jira_url(self, match):
        return f"[{match.group(1)}]({match.group(1)})"
