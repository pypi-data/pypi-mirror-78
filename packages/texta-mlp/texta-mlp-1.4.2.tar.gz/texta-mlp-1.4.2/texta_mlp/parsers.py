from abc import ABCMeta, abstractmethod
from typing import Iterator

import regex as re

from .fact import Fact


class ParseResult:
    def __init__(self, value, span):
        self.value = value
        self.span = span


    def to_fact(self, fact_type, doc_path):
        return Fact(
            fact_type=fact_type,
            fact_value=self.value,
            doc_path=doc_path,
            spans=[self.span]
        )


class AbstractParser(metaclass=ABCMeta):

    @abstractmethod
    def parse(self) -> Iterator[ParseResult]:
        raise NotImplemented


class ContactPhoneParser:


    def __init__(self, input_text, months):
        self.text = input_text
        self.months = months


    def parse(self):
        """
        Finds all the phone numbers.
        Arguments:
        text -- A string of text to parse phone numbers from.
        Returns:
        numbers -- A list containing the numbers found.
        """
        months = self.months  # ?\:?[0-9]{2}( ?:[0-9]{2}){0,2} (GMT)?\+[0-9]{2} ?\:? ?[0-9]{2})
        pattern = re.compile(r'(?<![0-9]{2}[\./][0-9]{2}[\./])(?<![0-9]{2} [\./] [0-9]{2} [\./] )(?<!Date: )(?<!Date : )(?:\b|\+|\+\s)\d{1,4}(\s\(\s[0-9]+\s\)\s?)?[ -]?\(?\d{2,4}\)?(?:[ -]?\d{1,4}?\b)+(\s\([0-9]+\))?(?! ?:? ?[0-9]{2}( ?: ?[0-9]{2}){0,2} (GMT)?\+[0-9]{2} ?\:? ?[0-9]{2})')
        for numb in pattern.finditer(self.text):
            match_string = numb.group(0)
            if len(match_string) > 5:
                not_a_date = True
                for month in months:
                    if re.search("[0-9]{1,2} ?" + month + "\.? ?$", self.text[:numb.span()[0]].lower()) or re.search(month + " ?\.?\s[0-9]{1,2} ?\,? ?" + "$", self.text[:numb.span()[0]].lower()):
                        not_a_date = False
                        break
                if not_a_date:
                    replaced = match_string.replace(' ', '').replace('-', '').replace('+', '').replace(')', '').replace('(', '')
                    yield ParseResult(value=replaced, span=numb.span())


class ContactEmailParser(AbstractParser):
    def __init__(self, input_text):
        self.text = input_text


    def parse(self):
        """
        Finds all the emails in the text.
        Arguments:
        text -- A string of text containing text to parse emails from.
        Returns:
        emails -- a list containing the emails found.
        """
        pattern = re.compile(r'([^\s]+\s?\.\s?)?[^\s@]+\s?@\s?[^@.\s]+\s?[.]\s?[^\s]{1,20}')
        for email in pattern.finditer(self.text):
            yield ParseResult(value=email.group(0).replace(' ', ''), span=email.span())


class ContactEmailNamePairParser(AbstractParser):
    def __init__(self, input_text):
        self.text = input_text


    def parse(self):
        """
        Finds all the emails in the text.
        Arguments:
        text -- A string of text containing text to parse emails from.
        Returns:
        emails -- a list containing the emails found.
        """
        pattern = re.compile(r'(?<=(\s|:|"|^))\p{L}+\s\p{L}+"?\s(< )?([^\s]+\s?\.\s?)?[^\s@]+\s?@\s?[^@.\s]+\s?[.]\s?[^\s]{1,20}')
        for email in pattern.finditer(self.text):
            email_splitted = email.group(0).split(" ")
            if len(email_splitted[1]) > 2 and len(email_splitted[0]) > 2 and email_splitted[0].title() == email_splitted[0] and email_splitted[1].title() == email_splitted[1]:
                yield ParseResult(value=email.group(0), span=email.span())


class AddressParser(AbstractParser):
    def __init__(self, text, stanza_entities, language):
        self.text = text
        self.stanza_entities = stanza_entities
        self.language = language


    @staticmethod
    def reescape(text):
        """
        https://stackoverflow.com/questions/43662474/reversing-pythons-re-escape 
        """
        return re.sub(r'\\(.)', r'\1', text)


    @property
    def _text_with_entity_types(self):
        """
        Joins entity words with their entity type/tag, e.g input 'Peeter läks Tallinnasse' outputs to 'Peeter_PER läks Tallinnasse_LOC'
        """
        replaced_text = self.text
        # sort stanza entities and check if they actually exist in text
        ents_to_replace = [(ent, len(ent.text)) for ent in self.stanza_entities if ent.text in self.text]
        for ent in sorted(ents_to_replace, key=lambda l: l[1]):
            ent = ent[0]
            tokens = ent.text.split(' ')
            modified_ent = '{}_{}'.format('_'.join(tokens), ent.type)
            # holy shit this is ugly, but it works...
            replaced_text = replaced_text.replace(" " + ent.text + " ", " " + modified_ent + " ")
        return replaced_text


    def _parse_ru(self):
        pattern = re.compile(
            r'(?:\b)([^\s]+_LOC\s?,?\s?((д\.|дом)\s?)?\s?[0-9]+\s?([а-яА-Я]|\s?/\s?[0-9]+|-[а-я])?)[\s\n,.]')
        for addr in pattern.finditer(self._text_with_entity_types):
            value = addr.group(1).replace('_LOC', '').replace('_', ' ')
            match = re.search(re.escape(value), self.text)
            if not match:
                try:
                    match = re.search(".".join(value.split()), self.text)
                    yield ParseResult(value=value.strip(), span=match.span())
                except:
                    continue
            else:
                yield ParseResult(value=value.strip(), span=match.span())


    def _parse_others(self):
        """
        dummy method for English, Estonian, Arabic
        TODO: proper regular expression for matching addresses in each language, except for Estonian
        """
        pattern = re.compile(r'\s([^\s]+_LOC\s?\s?[0-9]+)(_[A-Z]+)?')
        for addr in pattern.finditer(self._text_with_entity_types):
            value = addr.group(1).replace('_LOC', '').replace('_', ' ')
            match = re.search(re.escape(value), self.text)
            if not match:
                try:
                    match = re.search(".".join(value.split()), self.text)
                    yield ParseResult(value=value.strip(), span=match.span())
                except:
                    continue
            else:
                yield ParseResult(value=value.strip(), span=match.span())


    def parse(self):
        # pattern to search potential addresses
        if self.language == 'ru':
            return self._parse_ru()
        if self.language in ['en', 'et', 'ar']:
            return self._parse_others()

        else:
            raise NotImplementedError(
                f'{self.__class__.__name__}.parse not implemented for language {self.language!r}')
