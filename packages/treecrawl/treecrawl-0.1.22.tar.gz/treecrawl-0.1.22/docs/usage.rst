==============
TestData Usage
==============

To use TestData in a project::

    from treecrawl import TestData

In this example, U2029remover crawls through a direcotry tree, removing the
u2029 character from files (using DirEdit). The project contains initial and
expected directories for every test case. The pytst uses parametriz to iterte
through case names.  Those names are used by TestData to copy initial and
expected data into a tmp location (using testData.copy_test_data_to_temp()).  
After the transformation is run against inital test case data,
TestData.files_to_compare() is used to get a list of all of the file  contents
in the initial and expected directories to compare

TestData works if the tests data is organized into a directory structure that
matches the pytest tests test cases. The tree below would work for the test at
the bottom. 

.. code-block:: bash

| .
| └── tests
|     ├── test_u2029remover.py
|     └── testdata
|         └── test_remove_u2029
|             ├── beginning_of_file
|             │   ├── initial
|             │   └── expected
|             ├── end_of_file
|             │   ├── initial
|             │   └── expected
|             ├── end_of_first_line
|             │   ├── initial
|             │   └── expected
|             └── beginning_of_second_line
|                 ├── initial
|                 └── expected





.. code-block:: python

    class Upperificator(DirEdit):
        """Convert file characters to upper case

        """

        def __init__(self, root_dir=None, dry_run=True):
            super().__init__(root_dir=root_dir, dry_run=dry_run)

        def transform_files(self, source_file, destination_file):
            from treecrawl.utility import file_to_string, string_to_file

            contents = file_to_string(source_file)
            contents = contents.upper()
            string_to_file(contents, destination_file)


    @pytest.mark.parametrize(
        "test_case", ["pets", "cities"],
    )
    def test_upperificator(test_case, tmp_path, request):
        """Run and compare results to expected

        """
        # Instantiate a TestData object with the name of the test (originalname)
        t = TestData(request.node.originalname, str(tmp_path))
        # copy iitial and expected test case data to temp path
        t.copy_test_data_to_temp(test_case)
        # Execute against initial data
        Upperificator(root_dir=t.initial, dry_run=False)
        # compare all modified target files in initial against the matching
        # file in expected
        for cmp in t.files_to_compare():
            assert cmp[0] == cmp[1]
