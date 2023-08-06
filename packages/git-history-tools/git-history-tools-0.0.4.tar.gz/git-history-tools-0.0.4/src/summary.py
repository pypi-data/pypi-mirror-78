from typing import Set, Any, Union


class Summary:
    def __init__(self, pattern, deep):
        self._commits = []
        self._pattern = pattern
        self._deep = deep

    def add(self, commit):
        self._commits.append(commit)

    def show(self) -> str:
        _paths = set()
        for _c in self._commits:
            for _f in _c.files:
                count = _f.count('/')
                if count < 3:
                    _path = _f[0:_f.index('/')]
                else:
                    _path = '/'.join(_f.split("/", self._deep)[0:self._deep])
                _paths.add(_path)
        return '\n'.join(_paths)

    def msg(self) -> str:
        _messages: Set[Union[str, Any]] = set()
        for _c in self._commits:
            match = self._pattern.search(_c.msg)
            if match:
                _short_msg = match.group(0)
            else:
                _short_msg = "NOT FOUND"
            _messages.add(_short_msg)
        return '\n'.join(_messages)

    def hashes(self) -> str:
        _hashes = set()
        for _c in self._commits:
            _hashes.add(_c.hash)
        return '\n'.join(_hashes)
