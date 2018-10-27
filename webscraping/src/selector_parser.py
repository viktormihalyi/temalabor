import re
from bs4 import BeautifulSoup

SELECTOR_TYPES = ['css', 'xpath', 'regex']
PARSER_TYPES = ['text', 'number', 'raw']

SELECTOR_TYPE = 'type'
SELECTOR_COMMAND = 'command'
SELECTOR_PARSE_AS = 'parse_as'

PARSE_AS_DEFAULT = 'raw'

def parse_selector(response, selector, one=False):
    selection = _parse_selector(response, selector[SELECTOR_TYPE], selector[SELECTOR_COMMAND], one)

    parser_type = selector[SELECTOR_PARSE_AS] if SELECTOR_PARSE_AS in selector else PARSE_AS_DEFAULT

    if one:
        return parse_text_with_type(selection, parser_type)
    else:
        return [parse_text_with_type(s, parser_type) for s in selection]


def _parse_selector(response, selector_type, selector_command, one=False):
    if selector_type not in SELECTOR_TYPES:
        print('ERROR: bad selector type "{}"'.format(selector_type))
        return None

    if selector_type == 'css':
        selected = response.css(selector_command)
        if one:
            return selected.extract_first()
        else:
            return selected.extract()

    elif selector_type == 'xpath':
        selected = response.xpath(selector_command)
        if one:
            return selected.extract_first()
        else:
            return selected.extract()

    elif selector_type == 'regex':
        # always returns the first group
        match = re.search(selector_command, response.text)
        if match:
            return match.group(1)
        else:
            return None

    return None


def parse_text_with_type(parsed_text, property_type):
    if property_type not in PARSER_TYPES:
        print('ERROR: bad property type "{}"'.format(property_type))
        return None

    if property_type == 'text':
        bs_obj = BeautifulSoup(parsed_text, 'html.parser')
        rows = ''.join([str(s).replace('\n', ' ') for s in bs_obj.contents])
        bs_rows = BeautifulSoup(rows, 'html.parser')
        nice_text = bs_rows.get_text(separator='\n')
        return nice_text.strip()

    elif property_type == 'number':
        bs_obj = BeautifulSoup(parsed_text, 'html.parser')
        # select all numbers from a string
        return int(''.join(c for c in bs_obj.text if c.isdigit()))

    elif property_type == 'raw':
        return parsed_text

    print('nothing found :(')
    return None
