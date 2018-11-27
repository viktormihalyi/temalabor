"""
This module contains all code for parsing selectors.
"""

import re
import logging

from bs4 import BeautifulSoup


# possible selector execution types
SELECTOR_TYPES = ['css', 'xpath', 'regex']

# possible post process types (default is 'raw')
PARSER_TYPES = ['text', 'number', 'raw']

SELECTOR_TYPE = 'type'
SELECTOR_COMMAND = 'command'
SELECTOR_PARSE_AS = 'parse_as'
SELECTOR_MAX = 'max'

PARSE_AS_DEFAULT = 'raw'

logger = logging.getLogger(__name__)


def parse_selector(response, selector, one=False):
    """
    Parses a selector.

    Executes a selector according to its type, and parses the value as defined in the configuration.
    It is possible to only return one value, instead of a list of values.

    Args:
        response: an HTTP response as a scrapy.Response object
        selector: a selector object from the json config
        one: with True, returns a single value

    Returns:
        Either a single value, or a list of values.
    """

    # logger.info('parse_slector("{}", "{}", "{}")'.format(response, selector, one))

    # execute selector
    selection = _execute_selector(response, selector[SELECTOR_TYPE], selector[SELECTOR_COMMAND], one)

    # try to get parse type, default is 'raw'
    parser_type = selector[SELECTOR_PARSE_AS] if SELECTOR_PARSE_AS in selector else PARSE_AS_DEFAULT

    if one:
        return _post_process(selection, parser_type)

    else:
        all_parsed_text = [_post_process(s, parser_type) for s in selection]

        if SELECTOR_MAX in selector:
            # set an upper limit
            max_number = int(selector[SELECTOR_MAX])
            return all_parsed_text[:max_number]
        else:
            return all_parsed_text


def _execute_selector(response, selector_type: str, selector_command: str, one=False):
    """
    Executes a selector on a scrapy.Response object.

    Args:
        response:
        selector_type: how a selector should be parsed (e.g. "css", "xpath", ...)
        selector_command: a selection command as string
        one: with True, returns a single value (insted of a list of values)

    Returns:
        A single selection.
    """

    # logger.info('_execute_selector("{}", "{}", "{}", "{}")'.format(response, selector_type, selector_command, one))

    if selector_type not in SELECTOR_TYPES:
        logger.error('bad selector type "{}"'.format(selector_type))
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
            logger.error('no match for regex "{}"'.format(selector_command))
            return None

    return None


def _post_process(parsed_text: str, property_type: str):
    """
    Parses a selection as text, number, or raw.

    With text, it removes all html tags, and puts in newlines where appropriate.
    With number, it will grab all digits from the text, and turn them into a single number.
    With raw, it does nothing.

    Args:
        parsed_text: selection from _parse_selector
        property_type: variable type

    Returns:
        A single value.
    """

    # logger.info('_post_process("{}", "{}")'.format(parsed_text, property_type))

    if property_type not in PARSER_TYPES:
        logger.error('bad property type "{}"'.format(property_type))
        return None

    # parse as text
    # remove html tags, but keep newlines
    if property_type == 'text':
        bs_obj = BeautifulSoup(parsed_text, 'html.parser')
        rows = ''.join([str(s).replace('\n', ' ') for s in bs_obj.contents])
        bs_rows = BeautifulSoup(rows, 'html.parser')
        nice_text = bs_rows.get_text(separator='\n')
        return nice_text.strip()

    # parse as number
    # only keep the digits
    elif property_type == 'number':
        bs_obj = BeautifulSoup(parsed_text, 'html.parser')
        # select all numbers from a string
        return int(''.join(c for c in bs_obj.text if c.isdigit()))

    # do nothing
    elif property_type == 'raw':
        return parsed_text

    return None
