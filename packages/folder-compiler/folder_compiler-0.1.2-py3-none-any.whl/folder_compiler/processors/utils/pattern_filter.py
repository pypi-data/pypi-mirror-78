import re


class PatternFilter:
    """
    A util for checking if the source matches a filter for inclusion or exclusion.
    Per default it excepts everything.
    If you use add_include_pattern(".*\\.md") it would only accept files ending
     with ".md".
    """

    def __init__(self, includes: list = None, excludes: list = None):
        self._includes = includes if includes is not None else []
        self._excludes = excludes if excludes is not None else []
        if self._includes and not self._excludes:
            self.add_exclude_pattern(".*")

    def add_exclude_pattern(self, pattern: str):
        """
        Add a pattern to exclude
        :param pattern: The pattern for re.match
        :return: None
        """
        self._excludes.append(pattern)

    def add_include_pattern(self, pattern: str):
        """
        Add a pattern to include. If there are no excludes, everything else gets excluded
        on default.
        :param pattern: The pattern for re.match
        :return: None
        """
        if len(self._excludes) == 0:
            # if include is used, exclude everything by default.
            self.add_exclude_pattern(".*")
        self._includes.append(pattern)

    def _is_in_exclude(self, source):
        return any(re.match(pattern, source) for pattern in self._excludes)

    def _is_in_include(self, source):
        return any(re.match(pattern, source) for pattern in self._includes)

    def is_included(self, source: str):
        """
        Check if the source is to be included or if there are any rules against.
        :param source: Path of the source files (resp. input directory)
        :return: True if it should be processed, False otherwise.
        """
        return self._is_in_include(source) or not self._is_in_exclude(source)

    def __repr__(self):
        return self.__class__.__name__ + "(includes=" + str(
            self._includes) + ", excludes=" + str(self._excludes) + ")"
