#!/usr/bin/python3
import requests
from lxml import html
from csvwriter import *

data_dir = '../data'
csv_path = data_dir + '/data.csv'

class LanguageDetails(object):

    def __init__(self, family: str, name: str, native_name: str, iso_code: str, notes: str):
        self.family = family
        self.name = name
        self.native_name = native_name
        self.iso_code = iso_code
        self.notes = notes


def get_cell_text(cells: list, index: int) -> str:
    return cells[index].text_content().strip()


def get_language_details() -> list:
    res = requests.get('https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes')
    content = html.fromstring(res.content)

    languages = []
    table = content.get_element_by_id('Table')
    for row in table.cssselect('tr'):
        cells = row.cssselect('td')
        if len(cells) == 0:
            continue
        languages.append(LanguageDetails(get_cell_text(cells, 1),
                                         get_cell_text(cells, 2),
                                         get_cell_text(cells, 3),
                                         get_cell_text(cells, 4),
                                         get_cell_text(cells, 8)))
    return languages;

languages = get_language_details()

with open(csv_path, 'w+') as file:
    writer = CsvWriter(file)
    writer.write_row("name", "native name", "iso code")
    for language in languages:
        writer.write_row(language.name, language.native_name, language.iso_code)
