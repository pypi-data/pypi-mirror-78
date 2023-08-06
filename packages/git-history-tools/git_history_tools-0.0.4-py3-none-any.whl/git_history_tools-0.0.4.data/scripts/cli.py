#!python
"""cli.py

Description:
  Group GIT commits by user and show changes in a compact mode

Usage:
  cli.py [-b <name>] [-i <regex>] [-d <number>] [--since date] [--after date] <path>

Options:
  -h --help                     Show this screen.
  -b --branch <name>            GIT branch name [default: master]
  -i --issue <regex>            Regex pattern which correspond the issue ID. [default: ""]
  -d --deep <number>            change file deep [default: 1]
  --since <date>                Start date: format (%Y-%m-%d). Default is today -1
  --after <date>                End date: format (%Y-%m-%d). Default is today -2
  <path>                        GIT repository path.
"""
from datetime import datetime, timedelta
from typing import Dict, List

from tabulate import tabulate
from docopt import docopt
import re

from src.commit import Commit
from src.gitutils import GitUtils
from src.summary import Summary


def show(path, branch, pattern, deep, since, after):
    commits: List[Commit] = GitUtils.get_commits_between(path, branch, since, after)
    changes: Dict[str, Summary] = GitUtils.group_by_user(commits, pattern, deep)
    table = [
        [key, changes[key].show(), changes[key].msg(), changes[key].hashes()]
        for key in changes
    ]
    headers = ["Author", "Modules", "Issue", "GIT hash"]
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


if __name__ == '__main__':
    arguments = docopt(__doc__)
    _path = arguments['<path>']
    _branch = arguments['--branch']
    _issue_pattern = re.compile(arguments['--issue'])
    _deep = int(arguments['--deep'])
    _since = arguments['--since']
    _after = arguments['--after']
    if _since is None:
        _start_date = (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d 00:00:00')
    else:
        _start_date = datetime.strptime(_since, '%Y-%m-%d')
    if _after is None:
        _end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        _end_date = datetime.strptime(_after, '%Y-%m-%d')
    show(_path, _branch, _issue_pattern, _deep, _start_date, _end_date)
