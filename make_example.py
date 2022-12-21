"""
git checkout --orphan <new-branch>

No need, can leave as chain.

iso8601: 2006-07-03 17:18:43 +0200
"""


from git import Repo
import git
import math

from datetime import datetime, timedelta, timezone
import random
from collections import defaultdict

import pathlib as p
import tempfile

pairs = ["USD-SGD", "USD-GBP", "GBP-EUR"]

def make_dates(delta = timedelta(hours = 1)):
  end = datetime.now(tz=timezone.utc)
  return [end - i * delta for i in range(31 * 24)][::-1]

def prep_data(time, dir):
  dir = dir / "data" / "binance"
  dir.mkdir(parents=True, exist_ok=True)
  for pair in pairs:
    rate = math.exp(random.gauss(0, 1))
    fp = dir / pair
    fp.write_text(f"exchange rate for {pair} at {time} is {rate:.5}\n")
    yield str(fp)

def base_repo(base_dir):
  repo = Repo.init(base_dir, bare=False)
  work = p.Path(repo.working_tree_dir)
  times = list(make_dates())
  commits = {}
  days = lambda: defaultdict(list)
  months = defaultdict(days)

  for time in times:
    files = list(prep_data(time, work))
    repo.index.add(files)
    print(time, str(time))
    c = repo.index.commit("More data", author_date=time, commit_date=time)
    commits[time] = c

if __name__=='__main__':
  base_repo(p.Path("example_repo"))
