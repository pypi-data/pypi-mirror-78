import os
import typing

from .context import CompilerContext
from .file_ownership_manager import FileOwnershipManager
from .processors import Processor


class FolderCompiler:
    """
    Compile your files from the input folder to the output folder.
    The general concept is that every output file will be created from a single input
    file. For example compiling a markdown file to html. However, composing an output
    file from multiple input files is possible by multiple compilations (collect the
    information on the first run, create the output on the second). Still, for such
    things a more complex static site generator like Hyde might be better suited. This
    one is supposed to be as simple as possible.
    """

    def __init__(self, input: str = "./content", output: str = "./output",
                 followlinks=True):
        self._followlinks = followlinks
        fsm = FileOwnershipManager(output)
        self._context = CompilerContext(input=input, output=output,
                                        file_ownership_manager=fsm)

    def _process_path(self, source, processors):
        if os.path.exists(os.path.join(self._context.input, source)):
            print(f"Processing '{source}'")
            for processor in processors:
                if processor(source, self._context):
                    print(f"Applied '{processor.__class__.__name__}'.")
                    return True
        else:
            print(f"Skipping {source}. Probably bad link.")
            return True

    def compile(self, processors: typing.List[Processor]):
        """
        Walk through all the input files and try to process them with the first processor
        that accepts it.
        You can also compile multiple times in order to collect information.
        :param processors: List of processors.
        :return: Itself
        """
        input_path = self._context.input
        for root, folders, files in os.walk(input_path, topdown=True,
                                            followlinks=self._followlinks):
            relative_root = os.path.relpath(root, input_path)
            if self._process_path(relative_root, processors):
                # no further processing of folder and its content
                folders.clear()
                files.clear()
            for file in files:
                source = os.path.join(relative_root, file)
                self._process_path(source, processors)
        return self

    def _remove_empty_output_directories(self) -> None:
        for root, folders, files in os.walk(self._context.output):
            if len(folders) + len(files) == 0 and root != self._context.output:
                print("Remove empty directory:", root)
                os.rmdir(root)

    def remove_orphaned_files(self) -> None:
        """
        Remove files in the output directory for which no processor claimed ownership.
        :return: None
        """
        for file in self._context.file_ownership_manager.iterate_orphaned_files():
            print("Remove:", file)
            os.remove(file)
        self._remove_empty_output_directories()
