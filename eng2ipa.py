# -*- coding: utf-8 -*-

from lxml import html
import requests


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
    response = requests.post(url, data=data)
    # print(response.text)
    if response.status_code != requests.codes.ok:
        return word
    tree = html.fromstring(response.content)
    ipa = tree.xpath('//div[@id="transcr_output"]/span/text()')
    return ipa
