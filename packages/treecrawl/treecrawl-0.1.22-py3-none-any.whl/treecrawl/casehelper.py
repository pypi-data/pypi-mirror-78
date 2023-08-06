"""Helpers for using test data


"""
import os
from .utility import mkdir_p
from typing import List, Tuple  # noqa


class CaseHelper(object):
    """Test helper object representing the test and test case data

    It should log the relevant temp path locations

    Assumptions:
        - The project test resources are in a directory 'testdata'
        - Functions under test accept input and output (actual) locations

    CaseHelper represents test case and golden data for projects that transform
    files or directory contents

    golden(str): absolute path to a golden resource (file or directory) in the
    project tree. This is updated when pytest is run with the -update-golden
    flag. example: testdata/[TEST]/[CASE]/output.golden

    expected(str): absolute path to a copy of the golden resource in the
    tmp/test/case used for comparison. It can be useful to keep all of the
    relevant data for a test run in one place. example:
    [TMP_DIR]/[TEST]/[CASE]/

    input(str): absolute path to the transformation input data copied to . This
    should pr passed to the function under test as target data to be
    transformed. example: [TMP_DIR]/[TEST]/[CASE]/input

    actual(str): absolute path to the transformation output data. If this is
    the same as expected, a test would pass. example:
    [TMP]]/[TEST]/[CASE]/golden



    """

    def __init__(
        self, test_data, test_name, test_case, temp_dir, update_golden=False
    ):
        """init data. see class docstring for more details

        :param str test_data: project directory containing all test
        data. This is prepended to all the relevatn test case resource
        paths

        :param str test_name: test name from request.node.originalname

        :param str test_case: test case from parametrize

        :param str temp_dir: temporary directory for the test case

        if update_golden is  True
        """
        self.update_golden = update_golden
        self.test_name = test_name
        self.test_case = test_case
        self.golden = os.path.join(test_data, test_name, test_case, "golden")
        self.expected = os.path.join(
            temp_dir, test_name, test_case, "expected"
        )
        self.input = os.path.join(test_data, test_name, test_case, "input")
        self.actual = os.path.join(temp_dir, test_name, test_case, "actual")
        self.temp_case_dir = os.path.join(temp_dir, test_name, test_case)
        self.project_case_dir = os.path.join(test_data, test_name, test_case)
        # create the case path. populate will create the content subdirs
        mkdir_p(self.temp_case_dir)

        # if update_golden is  true, DO NOT populate temp until AFTER we use
        # the function under test to generate new golden contents
        if update_golden:
            self._delete_golden()
        else:
            self._populate_temp()

    def _populate_temp(self):
        """Copy test data to temp"""
        from distutils.dir_util import copy_tree

        if not os.path.isdir(self.golden):
            msg = (
                "Golden is missing: {}. Are you running with "
                "update_golden=True, but forgetting to create "
                "the new golden?".format(self.golden)
            )
            raise RuntimeError(msg)
        copy_tree(self.input, os.path.join(self.temp_case_dir, "input"))
        copy_tree(self.golden, self.expected)

    def _compare_use_filecmp(self):
        """use filecmp to compare actual and expected
        Return a result tuple":

        example


        :param str output_string: log string to process

        :rtype: bool, Tuple[str, str, str]
        """
        import filecmp
        from treecrawl.utility import compare_directories

        if os.path.isfile(self.input):
            res = filecmp.cmp(self.actual, self.expected, shallow=False)
            res = res, (self.input, self.actual, self.expected)
        elif os.path.isdir(self.input):
            succeeded = compare_directories(self.actual, self.expected)
            res = succeeded, (self.input, self.actual, self.expected)
        else:
            raise RuntimeError("Expected path to file or directory.")
        return res

    def _delete_golden(self):
        """



        :param str output_string: log string to process

        :rtype: List[Dict[str, str]]
        """
        from shutil import rmtree

        try:
            rmtree(self.golden)
        except FileNotFoundError:
            # don't care if it doesn;t exist
            pass

    def compare(self):
        """Run all comparisons

        If self.update_golden is True, golden needs to be updated externally
        by running the function under test and pointing its output to the
        golden path.  compare deals with this by conditionally run

        :param str output_string: log string to process

        :rtype: List[Dict[str, str]]
        """
        if self.update_golden:
            self._populate_temp()
        results = []
        results.append(self._compare_use_filecmp())
        return results
