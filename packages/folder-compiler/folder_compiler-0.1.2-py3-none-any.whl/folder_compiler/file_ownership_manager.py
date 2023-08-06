import os


class FileOwnershipManager:
    """
    Manages ownership of created files. Can be used e.g., to clean up orphaned files
    or detect overwriting of files by other processors.
    """

    def __init__(self, root: str):
        self._file_owner = {}
        self._root = root

    def claim_ownership(self, file_path: str, owner: object):
        """
        Claim the ownership of a produced file.
        The same owner can claim ownership multiple times without a warning.
        :param file_path: Path to the file. Relative to root (or absolute).
        :param owner: Owner of the file. 'self' is usually the best option.
        :return: True if claim has been successful.
        """
        file_path = self._normalize_path(file_path)
        self._check_file_existence(file_path, owner)
        if file_path not in self._file_owner:
            self._file_owner[file_path] = owner
            return True
        else:
            return self._handle_claims_for_files_with_owner(file_path, owner)

    def _normalize_path(self, path):
        if os.path.isabs(path):
            path = os.path.relpath(path, self._root)
        return os.path.normpath(path)

    def _check_file_existence(self, file_path, owner):
        if not os.path.exists(os.path.join(self._root, file_path)):
            print(f"WARNING: {owner} claimed ownership for non existent {file_path}.")

    def _handle_claims_for_files_with_owner(self, file_path, owner):
        if self.get_owner(file_path) != owner:
            print(f"WARNING: {file_path} already has an owner "
                  f"{self.get_owner(file_path)}!"
                  f" {owner} tried to overwrite ownership.")
            return False
        else:
            return True

    def get_owner(self, file_path: str):
        """
        Return the owner of a file or None if there is none.
        :param file_path: Path to the file. Relative to root (or absolute).
        :return: Owner or None
        """
        file_path = self._normalize_path(file_path)
        return self._file_owner.get(file_path, None)

    def iterate_owned_files(self):
        """
        Return an iterable over all files with an owner.
        :return: Iterable with tuples (absolute path of file, owner)
        """
        for root, folders, files in os.walk(self._root):
            for file in files:
                path = os.path.join(root, file)
                owner = self.get_owner(os.path.relpath(path, self._root))
                if owner is not None:
                    yield os.path.abspath(path), owner

    def iterate_orphaned_files(self):
        """
        Return an iterable over all files without an owner.
        :return: Iterable with absolute paths of files.
        """
        for root, folders, files in os.walk(self._root):
            for file in files:
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, self._root)
                if self.get_owner(rel_path) is None:
                    yield os.path.abspath(path)
