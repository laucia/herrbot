# -*- coding: utf-8 -*-

from lxml import html
import requests
import re
import random
from germanification import germanifications


IPA_TO_GERMAN = {
    'ɔ': ['o'],
    'ʤ': ['j'],
    'ʌ': ['a'],
    's': ['ß'],
    't': ['t'],
    'k': ['k'],
    'ʊ': ['uh'],
    '0': ['ö'],
    'j': ['i'],
    'm': ['m'],
    'z': ['s'],
    'ð': ['d'],
    'v': ['w'],
    'b': ['b'],
    'ʧ': ['tsch'],
    'ə': ['ö'],
    'θ': ['d', 't'],
    'X': ['ch'],
    'o': ['o'],
    'ɜ': ['ä'],
    'h': ['h'],
    'ɑ': ['ah'],
    'i': ['ie'],
    'ɪ': ['i'],
    'g': ['g'],
    'r': ['r'],
    'ɛ': ['ä'],
    'l': ['l'],
    'T': ['t'],
    'æ': ['ä', "e"],
    'f': ['v'],
    'Q': ['qu'],
    'ŋ': ['ng'],
    'p': ['p'],
    'n': ['n'],
    'P': ['p'],
    'y': ['ü'],
    'u': ['u'],
    'a': ['a'],
    'd': ['d'],
    'w': ['u'],
    'ʃ': ['sch'],
    'e': ['e'],
    'ɒ': ['a'],
    'ː': ['h', 'r'],
}


def english_to_ipa(phrase):
    """Transforms a phrase in English to IPA

        :param: phrase: some text
        :return: an array of IPA characters per word

    """
    url = "http://lingorado.com/ipa/"
    data = {
        'output_dialect': 'am',
        'text_to_transcribe': phrase,
    }
    response = requests.post(url,
        data=data)
    # print(response.text)
    if response.status_code != requests.codes.ok:
        return word
    tree = html.fromstring(response.content)
    ipa = tree.xpath('//div[@id="transcr_output"]/span/text()')
    ipa = " ".join(ipa)
    return ipa


def ipa_to_german(word):
    symbols = list(word)
    letters = [
        random.choice(IPA_TO_GERMAN[symbol]) if symbol in IPA_TO_GERMAN else symbol
        for symbol in symbols
    ]
    return "".join(letters)


space_before_punctuation = re.compile(r'( )+([.,?!])')
two_spaces = re.compile(r'  ')  # weird space-like character

def cleanup_german(phrase):
    result = phrase
    for _, regexp, replacement in germanifications:
        result = regexp.sub(replacement, result)
    # Redo punctuation
    result = space_before_punctuation.sub(r'\2', result)
    result = two_spaces.sub(r' ', result)
    return result
