#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2018-2019 releng-tool

import fnmatch
import os
import sys
import unittest

#: default verbosity for unit tests
DEFAULT_VERBOSITY = 2

def main():
    """
    process main for unit tests

    This method will prepare the test suite, load listed test classes and
    perform a run.
    """
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # discover unit tests
    test_base = os.path.dirname(os.path.realpath(__file__))
    tests_dir = os.path.join(test_base, 'unit-tests')
    unit_tests = loader.discover(tests_dir)

    # check if a unit test name was provided
    target_test_name_pattern = None
    for arg in sys.argv[1:]:
        if not arg.startswith('-'):
            target_test_name_pattern = arg
            break

    # register tests
    target_unit_tests = None
    if target_test_name_pattern:
        target_unit_tests, module_load_failure = find_tests(
            unit_tests, target_test_name_pattern)
        if target_unit_tests:
            print('running specific tests:')
            for test in target_unit_tests:
                print('    {}'.format(test.id()))
            sys.stdout.flush()
        else:
            print('ERROR: unable to find test with pattern: '
                '{}'.format(target_test_name_pattern))
            if not module_load_failure:
                sys.exit(1)

    if target_unit_tests:
        suite.addTests(target_unit_tests)
    else:
        suite.addTests(unit_tests)

    # invoke test suite
    runner = unittest.TextTestRunner(verbosity=DEFAULT_VERBOSITY)
    return 0 if runner.run(suite).wasSuccessful() else 1

def find_tests(entity, pattern):
    """
    search for a unit tests with a matching wildcard pattern

    Looks for the first 'unittest.case.TestCase' instance where its identifier
    matches the provided wildcard pattern.

    Args:
        entity: the unit test entity to search for a pattern on
        pattern: the pattern

    Returns:
        a 2-tuple (list of tests, flag if a module error is detected)
    """
    found = []
    module_load_failure = False

    if isinstance(entity, unittest.case.TestCase):
        if fnmatch.fnmatch(entity.id(), '*{}*'.format(pattern)):
            found.append(entity)
        elif 'ModuleImportFailure' in entity.id():
            module_load_failure = True
    elif isinstance(entity, unittest.TestSuite):
        for subentity in entity:
            tests, fail = find_tests(subentity, pattern)
            if tests:
                found.extend(tests)
            if fail:
                module_load_failure = True

    return found, module_load_failure

if __name__ == '__main__':
    sys.exit(main())
