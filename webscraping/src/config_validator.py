import logging
from tags import *

ENABLED_DEFAULT_VALUE = True

logger = logging.getLogger(__name__)


def __get_referenced_collectors_in_method(method):
    if TAG_CALL_COLLECTORS in method:
        data_collectors = method[TAG_CALL_COLLECTORS]
        for collector in data_collectors:
            yield collector


def __get_referenced_methods(method):
    if TAG_FOLLOW_LINKS in method:
        called_methods = method[TAG_FOLLOW_LINKS]
        for link in called_methods:
            yield link[TAG_CALL_METHOD]


class ErrorCounter:
    def __init__(self):
        self.errors = 0
        self.warnings = 0


def __check_ids(possible_ids, referenced_ids, warns_errors, type_='id'):
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


def __get_spider_name(spider_config):
    if TAG_SPIDER_NAME not in spider_config:
        return None
    return spider_config[TAG_SPIDER_NAME]


def __is_enabled(spider_config):
    if TAG_ENABLED in spider_config:
        return spider_config[TAG_ENABLED]
    else:
        return ENABLED_DEFAULT_VALUE


def validate_spider_configuration(spider_config):
    logger.info('validating spider config')

    warns_errors = ErrorCounter()

    # must have a 'name'
    spider_name = __get_spider_name(spider_config)
    if not spider_name:
        logger.error('no name defined, exiting')
        return False

    enabled = __is_enabled(spider_config)

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
            for ref_collector in __get_referenced_collectors_in_method(method):
                collectors_referenced.append(ref_collector)

            for ref_method in __get_referenced_methods(method):
                methods_referenced.append(ref_method)

    # defined selector, method and data collector names
    collector_names = [coll[TAG_COLLECTOR_NAME] for coll in spider_config[TAG_COLLECTORS]]
    method_names = [method[TAG_METHOD_NAME] for method in spider_config[TAG_METHODS]]

    # check for bad names
    __check_ids(collector_names, collectors_referenced, warns_errors, type_='data collector')
    __check_ids(method_names, methods_referenced, warns_errors, type_='method')

    if warns_errors.errors > 0:
        logger.info('{} errors found'.format(warns_errors.errors))

    if warns_errors.warnings > 0:
        logger.info('{} warnings found'.format(warns_errors.warnings))

    return warns_errors.errors == 0
