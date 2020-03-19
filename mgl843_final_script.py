from pydriller import RepositoryMining
from git import Repo
import shutil
import os
import sys
import subprocess
import io

sys.setrecursionlimit(10000)

repo_dir = 'C:/REPOS/MGL843/TEMP'
repo_file = 'repos.txt'

print(str.format("Opening Git repo text file {repoFile} in '{repoDir}'...", repoFile=repo_file, repoDir=repo_dir))
with open(repo_file) as f: 
    lines = [line.rstrip('\n') for line in f] 

c = 1

for gitURL in lines:
    newRepo = repo_dir + '/repo' + str(c)
    c = c + 1

    print(str.format("Cloning repo '{gitURL}' into '{newRepo}'...", gitURL=gitURL, newRepo=newRepo))
    Repo.clone_from(gitURL, newRepo)
    print("Repo cloned!")

    commitsCSVFilePath = newRepo + '_commits.csv'  
    print(str.format("'{commitsCSVFilePath}' file created.", commitsCSVFilePath=commitsCSVFilePath))
    
    commitsFile = io.open(commitsCSVFilePath,"w+", encoding="utf-8")
    
    print(str.format("Writing to '{commitsCSVFilePath}'...", commitsCSVFilePath=commitsCSVFilePath))
    for commit in RepositoryMining(newRepo).traverse_commits():
        commitsFile.write(commit.hash + ';' 
            + commit.author.name + ';' 
            + commit.author.email + ';' 
            + str(commit.author_date)
            + '\n') 
    commitsFile.close()
    print(str.format("'{commitsCSVFilePath}' completed and closed.", commitsCSVFilePath=commitsCSVFilePath))

    smellsCSVFilePath = newRepo + '_smells.csv'

    print("Running PMD...")
    subprocess.run(str.format("pmd.bat -d {repo} -R rulesets/java/design.xml -f csv -reportfile {file}", repo=newRepo, file=smellsCSVFilePath))
    print(str.format("PMD complete. Data saved to'{smellsCSVFilePath}'.", smellsCSVFilePath=smellsCSVFilePath))

#----------------------------------------------------------------------

    # for commit in RepositoryMining(newRepo).traverse_commits():    
    #     for mod in commit.modifications:       
    #         f.write(commit.hash + ';' 
    #             + commit.author.name + ';' 
    #             + str(commit.author_date) + ';' 
    #             + mod.filename + ';' 
    #             + str(mod.nloc) + ';' 
    #             + str(mod.complexity)
    #             + '\n')