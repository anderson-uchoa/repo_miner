from pydriller import RepositoryMining
from git import Repo
import shutil
import os
import sys
import subprocess
import io

#sys.setrecursionlimit(10000)

repo_dir = 'DUMP'
repo_file = 'repos.txt'

print(str.format("Reading Git repo text file '{repoFile}'...", repoFile=repo_file))
with open(repo_file) as f: 
    lines = [line.rstrip('\n') for line in f] 

repositoryCounter = 1

for gitURL in lines:
    newRepo = repo_dir + '/gitRepo' + str(repositoryCounter)
    downloadRepo = newRepo + '/repo'
    repositoryCounter = repositoryCounter + 1

    print(str.format("Cloning repo '{gitURL}' into '{downloadRepo}'...", gitURL=gitURL, downloadRepo=downloadRepo))
    Repo.clone_from(gitURL, downloadRepo)
    print("Repo cloned!")

    commitsCSVFilePath = newRepo + '/repo_commits.csv'
    print(str.format("'{commitsCSVFilePath}' file created.", commitsCSVFilePath=commitsCSVFilePath))
    
    commitsFile = io.open(commitsCSVFilePath,"w+", encoding="utf-8")
    
    print(str.format("Writing to '{commitsCSVFilePath}'...", commitsCSVFilePath=commitsCSVFilePath))
    for commit in RepositoryMining(downloadRepo).traverse_commits():
        commitsFile.write(commit.hash + ';' 
            + commit.author.name + ';' 
            + commit.author.email + ';' 
            + str(commit.author_date)
            + '\n') 
    commitsFile.close()
    print(str.format("'{commitsCSVFilePath}' completed and closed.", commitsCSVFilePath=commitsCSVFilePath))

    smellsCSVFilePath = newRepo + '/repo_pmd_smells.csv'

    print("Running PMD...")
    pmdCacheFile = './pmdCacheFile'
    subprocess.run(str.format("pmd.bat -d {repo} -R rulesets/java/design.xml -f csv -reportfile {file} -cache {cache}", repo=newRepo, file=smellsCSVFilePath, cache=pmdCacheFile))
    print(str.format("PMD complete. Data saved to '{smellsCSVFilePath}'.", smellsCSVFilePath=smellsCSVFilePath))

    #pmd.bat -d C:\REPOS\MGL843\Python_RepoDownloder\DUMP\repo1 -R rulesets/java/design.xml -f csv -reportfile C:\REPOS\MGL843\Python_RepoDownloder\DUMP\repo1_smells.csv -cache C:\REPOS\MGL843\Python_RepoDownloder\pmdCacheFile

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