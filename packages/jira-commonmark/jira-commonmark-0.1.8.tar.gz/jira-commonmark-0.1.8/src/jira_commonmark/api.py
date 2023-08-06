from jira_commonmark.handlers.commonmarkup import CommonMarkRenderer
from jira_commonmark.handlers.html import HTMLRenderer
from jira_commonmark.handlers.text import TextRenderer
from jira_commonmark.parser import Jira2CommonMarkParser, Jira2HtmlParser, Jira2TextParser


def jira_to_html(jira_text: str, url_base: str=None, internal_hosts: list=None) -> str:
    """ Jira -> Html converter

    :param jira_text: str:  jiratext input
    :param url_base: str: base url for JIRA term converter
    :param internal_hosts: list: list of internal hosts which shall be replaced by <INTERN LENKE>
    :return str: html output
    """
    handler = HTMLRenderer(
         url_base=url_base,
         internal_hosts=internal_hosts
    )
    parser = Jira2HtmlParser(handler)
    html = parser.parse(jira_text)

    return html


def jira_to_common_markup(jira_text: str, url_base=None, internal_hosts: list=None) -> str:
    """ Jira -> CommonMark

        :param jira_text: str: jiratext input
        :param url_base: str: base url for JIRA term converter
        :param internal_hosts: list: list of internal hosts which shall be replaced by <INTERN LENKE>
        :return str: CommonMark output
    """
    handler = CommonMarkRenderer(
        url_base=url_base,
        internal_hosts=internal_hosts
    )
    parser = Jira2CommonMarkParser(handler)
    commonmark_text = parser.parse(jira_text)

    return commonmark_text


def jira_to_text(jira_text: str, url_base=None, internal_hosts: list=None) -> str:
    """ Jira -> Html converter

        :param jira_text: str: jiratext input
        :param url_base: str: base url for JIRA term converter
        :param internal_hosts: list: list of internal hosts which shall be replaced by <INTERN LENKE>
        :return str: plain text output
    """
    handler = TextRenderer(
        url_base=url_base,
        internal_hosts=internal_hosts
    )
    parser = Jira2TextParser(handler)
    text = parser.parse(jira_text)

    return text
