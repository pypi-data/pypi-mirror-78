from .file_ownership_manager import FileOwnershipManager


class CompilerContext:
    """
    Some data to share with the processors.
    """

    def __init__(self, input: str, output: str,
                 file_ownership_manager: FileOwnershipManager):
        self.input = input
        self.output = output
        self.file_ownership_manager = file_ownership_manager
