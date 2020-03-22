from pydriller import RepositoryMining
from pydriller.metrics.process.contributors_experience import ContributorsExperience
from pydriller.metrics.process.contributors_count import ContributorsCount
from git import Repo
import shutil
import os
import sys
import subprocess
import io
from pathlib import Path



metric = ContributorsCount(path_to_repo='E:/REPOS/MGL843/Python_RepoMiner/DUMP/zookeeper/zookeeper_repo', from_commit='047d9258a4730791b85cc81b0e1435465a32acbf' to_commit='8148f966947d3ecf3db0b756d93c9ffa88174af9')

count = metric.count()
minor = metric.count_minor()
print('Number of contributors per file: {}'.format(count))
print('Number of "minor" contributors per file: {}'.format(minor))







# https://github.com/apache/spark
# https://github.com/apache/kafka
# https://github.com/apache/cassandra
# https://github.com/apache/hive