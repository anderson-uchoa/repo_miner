from pydriller import RepositoryMining
from git import Repo
import shutil
import os
import sys
import subprocess
import io
from pathlib import Path


# pmd.bat -d C:\REPOS\MGL843\Python_RepoDownloder\DUMP\repo1 -R rulesets/java/design.xml -f csv -reportfile C:\REPOS\MGL843\Python_RepoDownloder\DUMP\repo1_smells.csv -cache C:\REPOS\MGL843\Python_RepoDownloder\pmdCacheFile

# for commit in RepositoryMining(newRepo).traverse_commits():    
#     for mod in commit.modifications:       
#         f.write(commit.hash + ';' 
#             + commit.author.name + ';' 
#             + str(commit.author_date) + ';' 
#             + mod.filename + ';' 
#             + str(mod.nloc) + ';' 
#             + str(mod.complexity)
#             + '\n')

# https://github.com/apache/spark
# https://github.com/apache/kafka
# https://github.com/apache/cassandra
# https://github.com/apache/zookeeper
# https://github.com/apache/hive


# git shortlog -s -n --all --no-merges > spark_nb_commits_per_author.csv
