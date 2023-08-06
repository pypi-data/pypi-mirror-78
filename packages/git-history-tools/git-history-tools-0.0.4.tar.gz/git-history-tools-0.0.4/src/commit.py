import typing


class Commit:
    def __init__(self, commit_hash, author, commit_datetime, msg, files=[]):
        self._commit_hash = commit_hash
        self._author = author
        self._datetime = commit_datetime
        self._files = files
        self._msg = msg

    def __str__(self):
        return f"{self._datetime} {self._commit_hash} {self._author}"

    @property
    def hash(self) -> str:
        return self._commit_hash

    @property
    def author(self) -> str:
        return self._author

    @property
    def datetime(self) -> str:
        return self._datetime

    @property
    def msg(self) -> str:
        return self._msg

    @property
    def files(self) -> typing.List[str]:
        return self._files