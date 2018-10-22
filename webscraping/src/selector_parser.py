import re


SELECTOR_PARSER_TYPES = ['css', 'xpath', 'regex']


def parse_selector(response, selector, one=False):
    return _parse_selector(response, selector['type'], selector['command'], one)


def _parse_selector(response, selector_type, selector_command, one=False):
    if selector_type not in SELECTOR_PARSER_TYPES:
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
