import os
import shutil

from ...context import CompilerContext


class ProcessorUtils:
    """
    Simple utils for reading, writing, and moving files. It automatically adapts the path
    for input and output and provides some notification. Prefer the utils over manual
    implementations.
    """

    def __init__(self, context: CompilerContext, owner: object):
        self._context = context
        self._owner = owner

    def add_file(self, target):
        """
        Notify that you created a file and claim ownership of it.
        If another processor claims ownership, a warning is issued.
        Files without an owner might be deleted or overwritten without a warning.
        :param target: Path to the target file, relative to output directory.
        :return: None
        """
        self._context.file_ownership_manager.claim_ownership(target, self._owner)

    def get_full_source_path(self, source: str):
        """
        Returns the absolute path to a source file.
        This can be used to call command line tools or similar for creation.
        :param source: Path to source file (relative to input directory)
        :return: Absolute path to source
        """
        path = os.path.join(self._context.input, source)
        path = os.path.normpath(path)
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} does not exist. Make sure the path is "
                                    f"relative to the input directory.")
        return os.path.abspath(path)

    def get_full_target_path(self, target: str):
        """
        Return the full path to a target and adds it to the created files.
        This can be used to call command line tools or similar for creation.
        Subfolders are automatically created.
        Don't forget to use add_file to claim ownership as otherwise the file might be
        overwritten without a warning or deleted!
        :param target: Target path (relative to output directory)
        :return: Absolute path to target
        """
        path = os.path.join(self._context.output, target)
        path = os.path.normpath(path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return os.path.abspath(path)

    def is_target_outdated(self, source, target):
        """
        Returns true if the target file does not exists or is older than the source file.
        :param source: Path to source file (relative to input directory)
        :param target: Path to target file (relative to output directory)
        :return: True if target is outdated, otherwise False
        """
        if not os.path.exists(self.get_full_target_path(target)):
            return True
        date_source = os.path.getmtime(self.get_full_source_path(source))
        date_target = os.path.getmtime(self.get_full_target_path(target))
        return date_source > date_target

    def read_source_content(self, source: str) -> str:
        """
        Read the content of the source file.
        You can also use 'get_full_source_path' for using the file directly.
        :param source: Path within the input directory
        :return: Content of the source file
        """
        with open(self.get_full_source_path(source), "r") as input_file:
            return input_file.read()

    def write_target_content(self, target: str, content: str) -> None:
        """
        Writes content to a target file. Automatically creates necessary subfolders.
        You can also use 'get_full_target_path' for using the file directly.
        :param target: Path within the target directory
        :param content: String with the content to be written.
        :return: None
        """
        path = self.get_full_target_path(target)
        print("Write:", path)
        with open(path, "w") as output_file:
            output_file.write(content)
        self.add_file(target)

    def copy_file(self, source: str, target: str):
        """
        Copies a file from the input to the output directory.
        :param source: Path in input directory
        :param target: Path in output directory
        :return: None
        """
        source_path = self.get_full_source_path(source)
        target_path = self.get_full_target_path(target)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        print("Copy:", source_path, "->", target_path)
        shutil.copyfile(source_path, target_path)
        self.add_file(target)
