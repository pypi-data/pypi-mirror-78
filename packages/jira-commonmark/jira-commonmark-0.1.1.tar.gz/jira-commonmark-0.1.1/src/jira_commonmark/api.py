from jira_commonmark.handlers.commonmarkup import CommonMarkRenderer
from jira_commonmark.handlers.html import HTMLRenderer
from jira_commonmark.handlers.text import TextRenderer
from jira_commonmark.parser import Jira2CommonMarkParser, Jira2HtmlParser, Jira2TextParser


def jira_to_html(jira_text: str, url_base: str=None) -> str:
    handler = HTMLRenderer(
         url_base=url_base
    )
    parser = Jira2HtmlParser(handler)
    html = parser.parse(jira_text)

    return html


def jira_to_common_markup(jira_text: str, url_base=None) -> str:
    handler = CommonMarkRenderer(
        url_base=url_base
    )
    parser = Jira2CommonMarkParser(handler)
    commonmark_text = parser.parse(jira_text)

    return commonmark_text


def jira_to_text(jira_text: str, url_base=None) -> str:
    handler = TextRenderer(
        url_base=url_base
    )
    parser = Jira2TextParser(handler)
    text = parser.parse(jira_text)

    return text
