from typing import List, Dict, Any, Union

from git import Repo

from src.commit import Commit
from src.summary import Summary


class GitUtils:
    @staticmethod
    def get_commits_between(rep_path, branch, since, after) -> List[Commit]:
        _commits: List[Commit] = []
        _repo = Repo(rep_path)
        for _c in _repo.iter_commits(branch, max_count=300, since=since, after=after):
            _commit = Commit(_c.hexsha, _c.author, _c.committed_datetime, _c.message, _c.stats.files)
            _commits.append(_commit)
        return _commits

    @staticmethod
    def group_by_user(commits, pattern, deep) -> Dict[str, Summary]:
        _summaries_by_user: Dict[Any, Union[Summary, Any]] = {}
        for _commit in commits:
            if _commit.author in _summaries_by_user:
                _summary = _summaries_by_user[_commit.author]
            else:
                _summary = Summary(pattern, deep)
            _summary.add(_commit)
            _summaries_by_user[_commit.author] = _summary
        return _summaries_by_user
