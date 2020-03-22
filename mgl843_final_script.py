from pydriller import RepositoryMining
from git import Repo
import shutil
import os
import sys
import subprocess
import io
from pathlib import Path

#sys.setrecursionlimit(10000)

repo_dir = 'DUMP'
repo_file = 'repos.txt'

# Open repo file and read Git repos
print(str.format("Reading Git repo text file '{repoFile}'...", repoFile=repo_file))
with open(repo_file) as f: 
    lines = [line.rstrip('\n') for line in f] 
repositoryCounter = 0
("----------------------------------------------------------------------------------")

# Loop on all repos in file
for gitURL in lines:
    
    repositoryCounter = repositoryCounter + 1

    # Get project name from URL
    p = Path(gitURL)
    projectName = p.parts[-1]

    # Setup directory names
    newRepo = repo_dir + '/' + projectName
    downloadRepo = newRepo + '/' + projectName + '_repo'  

    # Clone repo into directory
    print(str.format("Cloning repo '{gitURL}' into '{downloadRepo}'...", gitURL=gitURL, downloadRepo=downloadRepo))
    Repo.clone_from(gitURL, downloadRepo)
    print("Repo cloned!")
    print("----------------------------------------------------------------------------------")

    # Create CSV file for commits
    commitsCSVFilePath = newRepo + '/' + projectName + '_commits.csv'
    commitsFile = io.open(commitsCSVFilePath,"w+", encoding="utf-8")
    print(str.format("'{commitsCSVFilePath}' file created.", commitsCSVFilePath=commitsCSVFilePath))
    
    # Write info into commit file
    print(str.format("Writing to '{commitsCSVFilePath}'...", commitsCSVFilePath=commitsCSVFilePath))
    commitsFile.write('"commit.hash","commit.author.name","commit.author.email","commit.author_date","mod.filename","mod.change_type","mod.nloc"\n') 
    commitsCounter = 0
    for commit in RepositoryMining(downloadRepo).traverse_commits():
        commitsCounter = commitsCounter + 1
        print(str.format("Analyzing commit #{currentCommit} ({hash})...", currentCommit=commitsCounter, hash=commit.hash))
        for mod in commit.modifications:    
            commitsFile.write('"' + commit.hash + '","' + commit.author.name + '","' + commit.author.email + '","' + str(commit.author_date) + '","' + mod.filename + '","' + str(mod.change_type) + '","' + str(mod.nloc) + '"\n') 

    # Close commit file
    commitsFile.close()
    print(str.format("'{commitsCSVFilePath}' completed and closed.", commitsCSVFilePath=commitsCSVFilePath))
    print(str.format("Analyzed {nbCommits} commits.", nbCommits=commitsCounter))
    print("----------------------------------------------------------------------------------")

    # Run PMD and save results into CSV file
    smellsCSVFilePath = newRepo + '/' + projectName + '_pmd_smells.csv'
    print("Running PMD...")
    pmdCacheFile = './pmdCacheFile'
    subprocess.run(str.format("pmd.bat -d {repo} -R rulesets/java/design.xml -f csv -reportfile {file} -cache {cache} -shortnames", repo=downloadRepo, file=smellsCSVFilePath, cache=pmdCacheFile))
    print(str.format("PMD complete. Data saved to '{smellsCSVFilePath}'.", smellsCSVFilePath=smellsCSVFilePath))
    print("----------------------------------------------------------------------------------")

    # Get number of commits per author (careful: CSV seperated by TABS)
    nbCommitsPerAuthorFile = newRepo + '/' + projectName + '_nb_commits_per_author.csv'
    print("Getting number of commits per author...")
    subprocess.run(str.format("git -C {dir} shortlog -s -n --all --no-merges > {outfile}", dir=downloadRepo, outfile=nbCommitsPerAuthorFile), shell=True)
    print(str.format("Data saved to '{nbCommitsFile}'.", nbCommitsFile=nbCommitsPerAuthorFile))
    print("----------------------------------------------------------------------------------")

print(str.format("All done! Check in '{repoDir}' directory.", repoDir=repo_dir))
print(str.format("Analyzed {nbRepos} repositories.", nbRepos=repositoryCounter))
