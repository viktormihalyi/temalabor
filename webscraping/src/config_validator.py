import logging
from tags import *

ENABLED_DEFAULT_VALUE = True

logger = logging.getLogger(__name__)


def _get_referenced_selectors_in_method(method):
    if TAG_FOLLOW_LINKS in method:
        follow_links = method[TAG_FOLLOW_LINKS]
        for link in follow_links:
            yield link[TAG_SELECTOR]


def _get_referenced_collectors_in_method(method):
    if TAG_CALL_COLLECTORS in method:
        data_collectors = method[TAG_CALL_COLLECTORS]
        for collector in data_collectors:
            yield collector


def _get_referenced_selectors_in_collector(collector):
    for prop in collector[TAG_PROPERTIES]:
        if TAG_SELECTOR in prop:
            yield prop[TAG_SELECTOR]


def _get_referenced_methods(method):
    if TAG_FOLLOW_LINKS in method:
        called_methods = method[TAG_FOLLOW_LINKS]
        for link in called_methods:
            yield link[TAG_CALL_METHOD]


class ErrorCounter:
    def __init__(self):
        self.errors = 0
        self.warnings = 0


def _check_ids(possible_ids, referenced_ids, warns_errors, type_='id'):
    for ref_id in referenced_ids:
        if ref_id not in possible_ids:
            logger.error('{} "{}" is not defined'.format(type_, ref_id))
            warns_errors.errors += 1

    for id_ in set(possible_ids):
        def_count = possible_ids.count(id_)
        if def_count > 1:
            logger.error('{} "{}" is defined multiple times (must be unique)'.format(type_, id_, def_count))
            warns_errors.errors += 1

    for id_ in possible_ids:
        used_count = referenced_ids.count(id_)
        if used_count == 0:
            logger.error('{} "{}" is never used'.format(type_, id_))
            warns_errors.warnings += 1


def validate_spider_configuration(spider_config):
    logger.info('validating spider config')

    warns_errors = ErrorCounter()

    if TAG_SPIDER_NAME not in spider_config:
        logger.error('no name defined, exiting')
        return False

    spider_name = spider_config[TAG_SPIDER_NAME]

    enabled = spider_config[TAG_ENABLED] if TAG_ENABLED in spider_config else ENABLED_DEFAULT_VALUE

    # skip validation if spider is disabled
    if not enabled:
        logger.info('spider "{}" is disabled, not validating'.format(spider_name))
        return
    else:
        logger.debug('validating spider "{}"'.format(spider_name))

    if TAG_STARTING_URLS not in spider_config:
        logger.error('no starting url defined, exiting')
        return False

    # collect referenced names here
    selectors_referenced = []
    collectors_referenced = []
    methods_referenced = []

    for starting in spider_config[TAG_STARTING_URLS]:
        if 'method' not in starting:
            logger.error('no method defined in starting_urls, exiting')
            return False
        else:
            methods_referenced.append(starting['method'])

    # collect referenced names in methods
    if TAG_METHODS not in spider_config:
        logger.error('no methods defined')
        warns_errors.errors += 1
    else:
        for method in spider_config[TAG_METHODS]:
            for ref_selector in _get_referenced_selectors_in_method(method):
                selectors_referenced.append(ref_selector)

            for ref_collector in _get_referenced_collectors_in_method(method):
                collectors_referenced.append(ref_collector)

            for ref_method in _get_referenced_methods(method):
                methods_referenced.append(ref_method)

    # collect referenced names in data collectors
    if TAG_COLLECTORS not in spider_config:
        logger.warning('no data collectors defined')
    else:
        for collector in spider_config[TAG_COLLECTORS]:
            for ref_selector in _get_referenced_selectors_in_collector(collector):
                selectors_referenced.append(ref_selector)

    # defined selector, method and data collector names
    selector_names = [sel[TAG_SELECTOR_NAME] for sel in spider_config[TAG_SELECTORS]]
    collector_names = [coll[TAG_COLLECTOR_NAME] for coll in spider_config[TAG_COLLECTORS]]
    method_names = [method[TAG_METHOD_NAME] for method in spider_config[TAG_METHODS]]

    # check for bad names
    _check_ids(selector_names, selectors_referenced, warns_errors, type_='selector')
    _check_ids(collector_names, collectors_referenced, warns_errors, type_='data collector')
    _check_ids(method_names, methods_referenced, warns_errors, type_='method')

    if warns_errors.errors > 0:
        logger.info('{} errors found'.format(warns_errors.errors))

    if warns_errors.warnings > 0:
        logger.info('{} warnings found'.format(warns_errors.warnings))

    return warns_errors.errors == 0
