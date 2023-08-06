import os

from ..context import CompilerContext
from .utils.pattern_filter import PatternFilter
from .utils.processor_utils import ProcessorUtils


class Processor:
    """
    A base class for a processor. It provides some basic utils and the general interface.

    A processor processes a file in the input directory (e.g., "./content").
    The compiler iterates through all files and calls all processors in the given
    order until the first one returns True. If include/exclude is used, the processor
    will return automatically if the file does not match. Otherwise, the method 'match'
    is called.

    A very simple Processor that simply copies all .pdf files could look like this:
    ```
    class PdfCopyProcessor(Processor):
        def __init__(self):
            super().__init__()
            self.add_include(".*\\.pdf")  # only .pdf files

        def process(self, source, utils):
            utils.copy_file(source, source) # simply copy the file
            return True  # mark file as processed
    ```
    Note that for this case, the FileCopyProcessor could also be used.
    """

    def __init__(self, includes: list = None, excludes: list = None):
        """
        :param includes: List of patterns to include
        :param excludes: List of patterns to exclude
        """
        self._inclusion_pattern_checker = PatternFilter(includes=includes,
                                                        excludes=excludes)

    def add_include(self, pattern: str):
        """
        Add a pattern that is included even if it fits an exclude pattern.
        If there is no prior exclude pattern, a generic ".*" exclude is added (an include
        without an exclude is useless).
        Use before compiling.
        :param pattern: A regex pattern for `re.match`. See https://docs.python.org/3/library/re.html
        :return: Itself to allow concatenation
        """
        self._inclusion_pattern_checker.add_include_pattern(pattern)
        return self

    def add_exclude(self, pattern: str):
        """
        Add a pattern that is excluded pattern.
        Use before compiling.
        :param pattern: A regex pattern for `re.match`. See https://docs.python.org/3/library/re.html
        :return: Itself to allow concatenation
        """
        self._inclusion_pattern_checker.add_exclude_pattern(pattern)
        return self

    def __call__(self, source, context: CompilerContext):
        utils = ProcessorUtils(context, self)
        if self._inclusion_pattern_checker.is_included(source):
            if os.path.isdir(utils.get_full_source_path(source)):
                return self.process_folder(source, utils)
            else:
                return self.process_file(source, utils)
        return False

    def process_folder(self, path: str, utils: ProcessorUtils):
        """
        Overwrite this method in your custom folder (optionally).
        You can do the same as in process file but the source is a folder.
        If you return True, no file or folder in this folder will be processed.
        It is called before processing any of the folders content.
        :param path: Relative path of the folder (relative to input directory)
        :param utils: Utils for reading/writing/copying files.
        :return: True if folder is (completely) processed (including content).
        """
        return False

    def process_file(self, source: str, utils: ProcessorUtils):
        """
        Overwrite this method in your custom processor.
        :param source: Path in the input directory to the source
        :param utils: Utils for reading/writing/copying files
        :return: True if processed, False if not responsible.
        """
        raise NotImplementedError()

    def __repr__(self):
        return self.__class__.__name__+"("+str(self._inclusion_pattern_checker)+")"
