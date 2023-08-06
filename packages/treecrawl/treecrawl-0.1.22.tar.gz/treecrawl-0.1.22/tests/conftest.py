import pytest
from treecrawl.utility import locate_subdir


def pytest_addoption(parser):
    parser.addoption(
        "--update_golden",
        action="store_true",
        help="Update golden files before running tests",
    )


@pytest.fixture
def update_golden(request):
    return request.config.getoption("--update_golden")


@pytest.fixture(scope="session", autouse=True)
def testdata():
    return locate_subdir("testdata")
