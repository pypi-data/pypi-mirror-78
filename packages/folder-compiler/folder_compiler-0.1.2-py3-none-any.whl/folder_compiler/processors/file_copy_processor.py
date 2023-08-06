from .base_processors import Processor
from .utils.processor_utils import ProcessorUtils


class FileCopyProcessor(Processor):
    """
    A very simple processor that simply copies the files. Good for images and stuff.
    Use with add_include or add_exclude to specialize it to specific files.
    """

    def __init__(self, skip_old=True):
        """
        :param skip_old: Skip if the source file is older than the target
        """
        super().__init__()
        self._skip_olds=skip_old

    def process_file(self, source: str, utils: ProcessorUtils):
        """
        Called by the compiler.
        """
        if self._skip_olds and not utils.is_target_outdated(source=source, target=source):
            print(source, "is up to date.")
            utils.add_file(source)  # claim ownership for old file but do not overwrite.
        else:
            utils.copy_file(source, source)
        return True
