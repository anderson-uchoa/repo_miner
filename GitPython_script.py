import git
from git import Repo

repo_dir = 'C:/REPOS/MGL843/TEMP'


with open('repos.txt') as f: 
    lines = [line.rstrip('\n') for line in f] 

c = 1

for gitURL in lines:
    newRepo = repo_dir + '/repo' + str(c)
    c = c + 1
    Repo.clone_from(gitURL, newRepo)


