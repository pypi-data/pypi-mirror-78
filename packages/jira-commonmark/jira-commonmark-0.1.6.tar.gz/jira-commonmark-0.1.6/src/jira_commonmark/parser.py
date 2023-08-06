from jira_commonmark.converters import *
from jira_commonmark import util


class Parser:
    """
    Generic parser
    """

    def __init__(self, handler):
        self.handler = handler
        self.converters = []

    def add_converter(self, converter) -> None:
        self.converters.append(converter)

    def parse(self, text) -> str:
        result = ""
        for block in util.blocks(text):
            block = self.handler.new_paragraph(block)
            for converter in self.converters:
                block = converter.convert(block, self.handler)
            result += block
        return result[:-len(self.handler.line_feed())]


class Jira2CommonMarkParser(Parser):

    def __init__(self, handler):
        super().__init__(handler)
        self.add_converter(JiraExpressionConverter)
        self.add_converter(TextInBracketsConverter)
        self.add_converter(TermReferenceConverter)
        self.add_converter(EmailConverter)
        self.add_converter(UrlConverter)
        self.add_converter(JiraUrlConverter)


class Jira2HtmlParser(Parser):

    def __init__(self, handler):
        super().__init__(handler)
        self.add_converter(JiraExpressionConverter)
        self.add_converter(TextInBracketsConverter)
        self.add_converter(TermReferenceConverter)
        self.add_converter(EmailConverter)
        self.add_converter(UrlConverter)
        self.add_converter(UnorderedListConverter)
        self.add_converter(OrderedListConverter)
        self.add_converter(JiraUrlConverter)


class Jira2TextParser(Parser):

    def __init__(self, handler):
        super().__init__(handler)
        self.add_converter(JiraExpressionConverter)
        self.add_converter(TextInBracketsConverter)
        self.add_converter(TermReferenceConverter)
        self.add_converter(UrlConverter)
        self.add_converter(MarkupLinkToTextConverter)
        self.add_converter(JiraUrlConverter)
