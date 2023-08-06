import os

from .base_processors import Processor
from .utils.processor_utils import ProcessorUtils


class DevNullProcessor(Processor):
    """
    This is a pseudo-processor that marks files and folders as processed without
    producing anything.
    Can especially be used to block specific files and folders to be processed by
    other processors.
    """
    def include_hidden_files_and_folders(self):
        """
        A common case
        :return:
        """
        self.add_include(".*/\..*")
        self.add_include("\.[/].*")
        return self

    def include_directory(self, path):
        self.add_include(os.path.normpath(path)+"/.*")
        return self

    def process_file(self, source: str, utils: ProcessorUtils):
        return True

    def process_folder(self, path: str, utils: ProcessorUtils):
        return True
