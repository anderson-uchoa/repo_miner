from pydriller import RepositoryMining

with open('repos.txt') as f: 
    lines = [line.rstrip('\n') for line in f] 

for gitURL in lines:
    for commit in RepositoryMining(gitURL).traverse_commits():
        print(commit.hash)
        print(commit.author.name)
        print(commit.author_date)
print('------------------------------------')
        #for mod in commit.modifications:
        #    print(mod.filename)