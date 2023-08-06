import logging
import os
from .utility import string_to_log_level, validate_path
from treecrawl.utility import create_module_logger

module_name = str(__name__)
module_logger = create_module_logger(module_name)


class Transformer(object):
    """Transform a file or directory

    input and output should both be paths to files OR both be directories
    with the same structure

    """

    dry_run_prefix = "SKIPPING! (DRY RUN): "

    def __init__(
        self, input=None, output=None, log_level="INFO", dry_run=True
    ):
        import json

        if input is None:
            self._input = os.getcwd()
        else:
            self._input = validate_path(input)
        if output is None:
            self._output = self._input
        else:
            self.output = output
        self.logger = logging.getLogger(
            module_name + "." + self.__class__.__name__
        )
        self.log_level = string_to_log_level(log_level)
        self.logger.setLevel(self.log_level)
        self.dry_run = dry_run

        msg_dict = {
            "input": self.input,
            "output": self.output,
            "log_level": self.log_level,
            "dry_run": str(self.dry_run),
        }
        self.logger.info(json.dumps(msg_dict))

    def add_dry_run_prefix(self, mm):
        """if the dry_run flag is set prepend the message with skipping..

        :param str mm: message to prepend

        :rtype: str
        """
        if self.dry_run:
            return Transformer.dry_run_prefix + mm
        return mm

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, value):
        self._input = validate_path(value)
        return self._input

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value):
        self._output = value
        return self._output

    def in_place(self):
        """Return true if teh output will overwrite the input

        :rtype: bool
        """
        return self._input == self._output

    def source_dest_as_dict(self):
        """If the target us a directory, return dict of input:output files

        The logic for selecting targets can be customized by overriding this
        method.

        :rtype: Dict[str, str]
        """
        from treecrawl.utility import (
            get_all_files,
            output_file_from_input_file,
        )

        res = {}
        if os.path.isfile(self.input):
            return {self.input: self.output}

        input_files = get_all_files(self.input)
        for file in input_files:
            if self.is_target(file):
                # transform input file and write to destination
                # in the same relative path in the output dir
                res[file] = output_file_from_input_file(
                    self.input, self.output, file
                )

        return res

    def is_target(self, i_file):
        """Return True is the file meets criteria to be transformed

        This is used by filter_files to build a target list.  The base
        implementation edits all files. Override this method to customizing
        file targeting

        WARNING!! I use opt-in targeting because treecrawl functions do not
        protect your binary files from being manipulated like  text files

        :param str i_file: abs path to target candidate

        :rtype: bool
        """
        raise NotImplementedError

    def transform(self, source_file, destination_file):
        """Override this with transformation logic

        CRITICAL: transform must check the value of self.dry_run and do the
        right thing.  use Transformer.add_dry_run_prefix to make the
        conditional logging a little easier

        read the source_file, do whatever and write to destination_file

        writing files may need to be encoding aware. look at methods that help
        with that like write_string_to_output or write your own

        :param str source_file: read this file as input
        :param str destination_file: write transformed file here

        """
        raise NotImplementedError

    def run(self):
        for k, v in self.source_dest_as_dict().items():
            if v is None:
                v = k
            self.transform(k, v)

    @staticmethod
    def write_string_to_output(s, o):
        """writes a string to a an absolute file path

        also creates necessary directories along the way

        :param str output_string: log string to process

        :rtype: List[Dict[str, str]]
        """
        from treecrawl.utility import string_to_file, mkdir_p

        if type(s) != str:
            msg = "Expected string input. Got {}".format(str(type(s)))
            raise RuntimeError(msg)
        # ensure directory pah exists
        mkdir_p(o, is_file=True)
        string_to_file(s, o)
