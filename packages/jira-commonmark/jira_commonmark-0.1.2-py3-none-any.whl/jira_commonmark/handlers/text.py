from jira_commonmark.handlers.base import Handler


class TextRenderer(Handler):

    def new_paragraph(self, text: str):
        return text

    def line_feed(self):
        return "\n"

    def sub_term_reference(self, match):
        return f"{match.group(1)}"

    def sub_url(self, match):
        return f"{match.group()}"

    def sub_mail(self, match):
        return f"{match.group()}"

    def sub_jira_url(self, match):
        return f"{match.group(1)}"

    def sub_link(self, match):
        return f"{match.group(1)}"
