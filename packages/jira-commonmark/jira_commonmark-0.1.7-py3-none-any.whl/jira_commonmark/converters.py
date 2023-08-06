import re

from abc import ABC
from jira_commonmark.handlers.base import Handler
from jira_commonmark.handlers.html import HTMLRenderer
from jira_commonmark.handlers.text import TextRenderer


class Converter(ABC):

    @classmethod
    def convert(cls, text: str, handler: Handler) -> str:
        raise NotImplementedError()


class TermReferenceConverter(Converter):

    pattern = r"\[\s*(.[^\(]*?)\s*\|\s*(.*?)(BEGREP-\d+?)\s*\]"

    @classmethod
    def convert(cls, text: str, handler: Handler) -> str:
        for match in re.finditer(cls.pattern, text):
            text = re.sub(cls.pattern, handler.sub_term_reference(match), text, count=1)
        return text


class EmailConverter(Converter):

    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\w"

    @classmethod
    def convert(cls, text: str, handler: Handler) -> str:
        for match in re.finditer(cls.pattern, text):
            text = re.sub(cls.pattern, handler.sub_mail(match), text, count=1)
        return text


class UrlConverter(Converter):

    pattern = r"(?<!href=)(?<!]\()(?<!\>)(?<!\[)(((?<!\/\/)www|https?:\/\/))[\.\%\w0-9\/\-\?\=\:\+\&\(\)]+\w"

    @classmethod
    def convert(cls, text: str, handler: Handler) -> str:
        for match in re.finditer(cls.pattern, text):
            text = text.replace(match.group(), handler.sub_url(match), 1)
        return text


class JiraUrlConverter(Converter):

    pattern = r"\[\s*([^\s]+[\w,;\.\-\(\)\sæøåÆØÅ§]*[\w,;\.\-\(\)æøåÆØÅ§\/])\s*\|\s*(www|http:|https:+[^\s]+[\w,;\/])\s*\]"

    @classmethod
    def convert(cls, text: str, handler: Handler) -> str:
        for match in re.finditer(cls.pattern, text):
            text = re.sub(cls.pattern, handler.sub_jira_url(match), text, count=1)
        return text


class JiraExpressionConverter(Converter):

    pattern = r"{\.\.\.}\s*|\[\.\.\.\]\s*|{\s*color(\s*:\s*#\w*)?\s*}\s*"

    @classmethod
    def convert(cls, text: str, handler: Handler) -> str:
        text = re.sub(cls.pattern, '', text)
        return text


class TextInBracketsConverter(Converter):

    pattern = r"\[([\w\s\:\/\-\.\?\=\&æøåÆØÅ]+)\](?!\()"

    @classmethod
    def convert(cls, text: str, handler: Handler) -> str:
        for match in re.finditer(cls.pattern, text):
            text = re.sub(cls.pattern, handler.sub_brackets(match), text, count=1)
        return text


class MarkupLinkToTextConverter(Converter):

    pattern = r"\[([a-zA-Z\s]+)\]\([a-zA-Z0-9:\/\.\-]*\)"

    @classmethod
    def convert(cls, text: str, handler: TextRenderer) -> str:
        for match in re.finditer(cls.pattern, text):
            text = re.sub(cls.pattern, handler.sub_link(match), text, count=1)
        return text


class UnorderedListConverter(Converter):

    pattern = r"^[ +]*[\-].*"

    @classmethod
    def convert(cls, text: str, handler: HTMLRenderer) -> str:
        result = ""
        in_list = False
        for line in text.splitlines():
            if in_list and re.compile(cls.pattern).match(line):
                line = UnorderedListItemConverter.convert(line, handler)
            elif re.compile(cls.pattern).match(line):
                line = handler.start_unordered_list() + UnorderedListItemConverter.convert(line, handler)
                in_list = True
            elif in_list:
                line = handler.end_unordered_list() + line
                in_list = False

            result += line + "\n"

        return result


class UnorderedListItemConverter(Converter):

    pattern = r"^[ +]*[\-].*"

    @classmethod
    def convert(cls, text: str, handler: HTMLRenderer) -> str:
        for match in re.finditer(cls.pattern, text):
            text = re.sub(cls.pattern, handler.sub_unordered_listitem(match), text, count=1)
        return text


class OrderedListConverter(Converter):

    pattern = r"^[ +]*[0-9]\..*"

    @classmethod
    def convert(cls, text: str, handler: HTMLRenderer) -> str:
        result = ""
        in_list = False
        for line in text.splitlines():
            if in_list and re.compile(cls.pattern).match(line):
                line = OrderedListItemConverter.convert(line, handler)
            elif re.compile(cls.pattern).match(line):
                line = handler.start_ordered_list() + OrderedListItemConverter.convert(line, handler)
                in_list = True
            elif in_list:
                line = handler.end_ordered_list() + line
                in_list = False

            result += line + "\n"

        return result


class OrderedListItemConverter(Converter):

    pattern = r"^[ +]*[0-9]\..*"

    @classmethod
    def convert(cls, text: str, handler: HTMLRenderer) -> str:
        for match in re.finditer(cls.pattern, text):
            text = re.sub(cls.pattern, handler.sub_ordered_listitem(match), text, count=1)
        return text
