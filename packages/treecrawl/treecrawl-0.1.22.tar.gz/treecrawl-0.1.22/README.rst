=========
treecrawl
=========


.. image:: https://img.shields.io/pypi/v/treecrawl.svg
        :target: https://pypi.python.org/pypi/treecrawl

.. image:: https://img.shields.io/travis/natemarks/treecrawl.svg
        :target: https://travis-ci.com/natemarks/treecrawl

.. image:: https://readthedocs.org/projects/treecrawl/badge/?version=latest
        :target: https://treecrawl.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




libraries to make it easier to maniuplate files in a directory tree


* Free software: MIT license
* Documentation: https://treecrawl.readthedocs.io.


Usage
--------

This project makes it easier to edit directory trees and to test those edits.

** CAUTION!! **
treecrawl doesn't protect you from mistreating your files by, for example, corrupting a binary file because you transformed it like a text file. In fact, utility.file_to_string() encodes binary to utf-8 ignoring errors, so it will help you wreck your files.

I generally manage this with scalpel-like opt-in targeting  when I override Transformer.is_target().  I use extensions where it's adequate, but if I need something more robust, I might use python-magic.

Check out the example transformer in tests.test_casehelper.MakeUpper

The example Transformer sub-class (MakeUpper) is a trivial example for using the Transformer class. remember the following tips:
Always override Transformer.transform
Override Transformer.is_target to customize the target file selection
Almost always create and use an alternative to Transformer.write_string_to_output(). Treating everything like a string will cause SERIOUS problems with editing and testing with any unicode at all.

tests/test_casehelper.py::test_make_upper  is a good example of the boilerplate use of casehelper.  Also be sure to replicate the tests/conftest.py so you can capture the pytest --update_golden flag.

When you init CaseHelper with the update golden flag (by running pytest --update_golden), it deletes the golden directory and delays the copying of temp files until CaseHelper.compare() is run.  In between these events, use the funciton under test to generate new project golden data

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


Build Notes
------------

Setup dev venv

::

    python -m venv .treecrawl.venv
    source .treecrawl.venv/bin/activate
    pip install -r requirements-dev.txt


Tests
------------

 I use pyenv to provide multiple versions for nox python testing. in my case:

.. code-block::

    pyenv install 3.6.8
    pyenv install 3.7.8
    # in the project directory
    pyenv local 3.6.8 3.7.8
    make test

If other versions are flagged as missing or are skipped you can just pyenv instal them and add them to the project directory


run 'make test' to run all the tests. I use pyenv to install all of the supported python versions so nox can run the full matrix of tests for me


always run ' make lint'
