#!/usr/bin/env python

"""Tests for `treecrawl` package."""
import os
import pytest
from treecrawl.utility import (
    find_path_to_subdirectory,
    mkdir_p,
    output_file_from_input_file,
    get_all_files,
    validate_path,
)
from treecrawl.casehelper import CaseHelper


def test_find_path_to_subdirectory(tmp_path):
    import os

    target_dir = os.path.join(
        str(tmp_path), *["some", "path", "to", "testdata"]
    )
    mkdir_p(target_dir)
    ff = find_path_to_subdirectory("testdata", search_path=str(tmp_path))
    assert ff[0].endswith("testdata")


@pytest.mark.parametrize(
    "test_case,file_count",
    [("happy_path", 3)],
)
def test_get_all_files(
    test_case, file_count, tmp_path, request, testdata, update_golden
):
    """This is a stupid redundant test but wtf

    c CaseHelper copies golden to tmp/expected and input to tmp/actual.
    file-count should match the total number of files that exist in tmp
    after this happens.

    """

    # Instantiate a TestData object with the name of the test (originalname)
    c = CaseHelper(
        testdata,
        request.node.originalname,
        test_case,
        str(tmp_path),
        update_golden=update_golden,
    )
    # Execute against initial data
    res = get_all_files(c.temp_case_dir)
    assert len(res) == file_count


def test_rel_pos_validate(tmp_path):
    d = tmp_path / "rel_exists"
    d.mkdir()

    orig_wd = os.getcwd()
    os.chdir(str(tmp_path))
    assert validate_path("rel_exists") == str(d)
    os.chdir(orig_wd)


def test_rel_neg_validate(tmp_path):
    d = tmp_path / "rel_exists"

    orig_wd = os.getcwd()
    os.chdir(str(tmp_path))
    with pytest.raises(RuntimeError, match="Invalid path: {}".format(str(d))):
        validate_path("rel_exists")
    os.chdir(orig_wd)


def test_none_pos_validate(tmp_path):
    orig_wd = os.getcwd()
    os.chdir(str(tmp_path))
    assert validate_path() == str(tmp_path)
    os.chdir(orig_wd)


def test_abs_pos_validate(tmp_path):
    d = tmp_path / "abs_exists"
    d.mkdir()
    assert validate_path(str(d)) == str(d)


def test_abs_neg_validate(tmp_path):
    d = tmp_path / "abs_exists"
    with pytest.raises(RuntimeError, match="Invalid path: {}".format(str(d))):
        validate_path(str(d))


# this was an interesting experiment using python magic
# to inspect filkes a litt=le closer. I've abandoned it because
# there's not enough value in the approach to account for adding
# an external dependency
@pytest.mark.skip
@pytest.mark.parametrize(
    "test_case,type",
    [
        ("a_directory", "dir"),
        ("ascii.txt", "ASCII text"),
        ("min_yaml.yml", "ASCII text"),
        ("utf8_unlabeled.txt", "UTF-8 Unicode text"),
        ("yaml.yml", "ASCII text"),
    ],
)
def test_path_type(test_case, type, request, testdata):
    """Run and compare results to expected"""
    # target = os.path.join(testdata, request.node.originalname, test_case)
    assert True
    # assert path_type(target) == type


def test_output_file_from_input_file():

    res = output_file_from_input_file(
        "/a/b/c/", "/d/f/g", "/a/b/c/x/y/z/file.txt"
    )
    assert res == "/d/f/g/x/y/z/file.txt"


def test_locate_subdir():
    from treecrawl.utility import locate_subdir

    res = locate_subdir("testdata")
    assert os.path.isdir(res)
