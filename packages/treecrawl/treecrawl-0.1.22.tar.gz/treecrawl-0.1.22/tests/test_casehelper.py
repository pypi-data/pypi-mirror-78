#!/usr/bin/env python

"""Tests for `treecrawl` package."""
import os
import pytest
from treecrawl.transformer import Transformer
from treecrawl.casehelper import CaseHelper


class MakeUpper(Transformer):
    """Convert non-ASCII files to ASCII"""

    def __init__(self, input, output, dry_run=False):
        super().__init__(input=input, output=output, dry_run=dry_run)

    def is_target(self, i_file):
        included_extensions = [".txt"]

        # if it's not a file, right?
        if not os.path.isfile(i_file):
            return False

        # Regardless of extension if the file is in a .git directory
        # exclude it
        if ".git" in i_file.split(os.path.sep):
            return False

        # now target only files ending in ".txt
        # i could use
        _, ext = os.path.splitext(i_file)
        if ext in included_extensions:
            return True

        return False

    def transform(self, source_file, destination_file):
        from treecrawl.utility import file_to_string

        contents = file_to_string(source_file)
        contents = contents.upper()
        self.write_string_to_output(contents, destination_file)


@pytest.mark.parametrize(
    "test_case",
    ["pets", "cities"],
)
def test_populate_temp(test_case, tmp_path, request, testdata, update_golden):
    """Run and compare results to expected"""
    import os
    from treecrawl.utility import compare_directories

    # Instantiate a CaseHelper object with the name of the test (originalname)
    c = CaseHelper(
        testdata, request.node.originalname, test_case, str(tmp_path)
    )
    assert compare_directories(c.golden, c.expected)
    assert compare_directories(
        os.path.join(c.temp_case_dir, "input"),
        os.path.join(c.project_case_dir, "input"),
    )


@pytest.mark.parametrize(
    "test_case",
    ["pets", "cities"],
)
def test_make_upper(test_case, tmp_path, request, testdata, update_golden):
    c = CaseHelper(
        testdata,
        request.node.originalname,
        test_case,
        str(tmp_path),
        update_golden=update_golden,
    )

    """when update golden is set by running pytest --update_golden,
    the project golden files are deleted. This step generates new ones from
    the the function under test """
    if update_golden:
        _ = MakeUpper(c.input, c.golden)

    m = MakeUpper(c.input, c.actual)
    m.run()
    for r in c.compare():
        succeeded, compared = r
        assert succeeded
        if not succeeded:
            print("input: {}\nactual: {}\nexpected: {}".format(*compared))
