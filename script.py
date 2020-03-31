# ================================================================================
# IMPORTS
# ================================================================================
from pydriller import RepositoryMining
from git import Repo
from pathlib import Path
import shutil
import os
import sys
import subprocess
import io
import re


# ================================================================================
# GLOBAL VARABLES
# ================================================================================
repo_dir = 'DUMP' # directory where all folder and files will be generated
repo_file = 'github_repos.txt' # text file with a list of GitHub repo URLs (one per line)


# ================================================================================
# FUNCTIONS
# ================================================================================
def openRepoFile():
    print(str.format("Reading Git repo text file '{repoFile}'...", repoFile=repo_file))
    with open(repo_file) as f: 
        return [line.rstrip('\n') for line in f] 

def cloneRepo(gitURL,downloadRepo):
    print(str.format("Cloning repo '{gitURL}' into '{downloadRepo}'...", gitURL=gitURL, downloadRepo=downloadRepo))
    Repo.clone_from(gitURL, downloadRepo)
    print("Repo cloned!")
    print("----------------------------------------------------------------------------------")

def generateCommitsCSVFile(newRepo,projectName,downloadRepo):
    commitsCSVFilePath = newRepo + '/' + projectName + '_commits.csv'
    commitsFile = io.open(commitsCSVFilePath,"w+", encoding="utf-8")
    print(str.format("'{commitsCSVFilePath}' file created.", commitsCSVFilePath=commitsCSVFilePath))
    
    print(str.format("Writing to '{commitsCSVFilePath}'...", commitsCSVFilePath=commitsCSVFilePath))
    commitsFile.write('"commit.hash","commit.author.name","commit.author.email","commit.author_date","mod.filename","mod.change_type","mod.nloc"\n') 
    commitsCounter = 0
    for commit in RepositoryMining(downloadRepo).traverse_commits():
        commitsCounter = commitsCounter + 1
        print(str.format("Analyzing commit #{currentCommit} ({hash})...", currentCommit=commitsCounter, hash=commit.hash))
        for mod in commit.modifications:    
            commitsFile.write('"' + commit.hash + '","' + commit.author.name + '","' + commit.author.email + '","' + str(commit.author_date) + '","' + mod.filename + '","' + str(mod.change_type) + '","' + str(mod.nloc) + '"\n') 

    commitsFile.close()
    print(str.format("'{commitsCSVFilePath}' completed and closed.", commitsCSVFilePath=commitsCSVFilePath))
    print(str.format("Analyzed {nbCommits} commits.", nbCommits=commitsCounter))
    print("----------------------------------------------------------------------------------")

def generatePMDOutputCSVFile(newRepo,projectName,downloadRepo):
    smellsCSVFilePath = newRepo + '/' + projectName + '_pmd_smells.csv'
    print("Running PMD...")
    pmdCacheFile = './pmdCacheFile'
    subprocess.run(str.format("pmd.bat -d {repo} -R rulesets/java/design.xml -f csv -reportfile {file} -cache {cache} -shortnames", repo=downloadRepo, file=smellsCSVFilePath, cache=pmdCacheFile))
    print(str.format("PMD complete. Data saved to '{smellsCSVFilePath}'.", smellsCSVFilePath=smellsCSVFilePath))
    print("----------------------------------------------------------------------------------")

def generateNbCommitsPerAuthorCSVFile(newRepo,projectName,downloadRepo):
    nbCommitsPerAuthorFile = newRepo + '/' + projectName + '_nb_commits_per_author.csv'
    print("Getting number of commits per author...")
    subprocess.run(str.format("git -C {dir} shortlog -s -n --all --no-merges > {outfile}", dir=downloadRepo, outfile=nbCommitsPerAuthorFile), shell=True)
    print(str.format("Data saved to '{file}'.", file=nbCommitsPerAuthorFile))
    print("----------------------------------------------------------------------------------")

def generateListOfAllFilesTextFile(newRepo,projectName,downloadRepo):
    allFilesInRepoPath = newRepo + '/' + projectName + '_all_files_in_repo.txt'
    print("Getting list of all Java files...")
    subprocess.run(str.format("git -C {dir} ls-tree --full-tree -r --name-only HEAD > {outfile}", dir=downloadRepo, outfile=allFilesInRepoPath), shell=True)
    print(str.format("All repo filenames saved to '{file}'.", file=allFilesInRepoPath))
    print("----------------------------------------------------------------------------------")
    return allFilesInRepoPath

def generateGitBlameOutputCSVFile(newRepo,projectName,downloadRepo,listOfFilesInRepo):
    # Generate raw text file
    gitBlameJavaFilesPath = newRepo + '/' + projectName + '_git_blame_java_files.txt'
    gitBlameFile = io.open(gitBlameJavaFilesPath,"w+", encoding="utf-8")
    gitBlameFile.close()
    print("Executing 'git blame' on each Java file in repo...")
    with open(listOfFilesInRepo) as gitFilenamesFile: 
        gitFilenames = [filename.rstrip('\n') for filename in gitFilenamesFile]
    nbFilesToCheck = len(gitFilenames)
    currentFileIndex = 0

    # Generate formatted CSV file
    for gitFilename in gitFilenames:
        currentFileIndex = currentFileIndex + 1
        print(str.format("Checking file {curr}/{tot} ...", curr=currentFileIndex, tot=nbFilesToCheck))
        if(gitFilename.endswith(".java")):
            subprocess.run(str.format("git -C {dir} blame {filename} >> {outfile}", dir=downloadRepo, filename=gitFilename, outfile=gitBlameJavaFilesPath), shell=True)
    print(str.format("Git blame results saved to '{file}'.", file=gitBlameJavaFilesPath))
    print("----------------------------------------------------------------------------------")
    with open(gitBlameJavaFilesPath, "r", encoding="utf-8") as gitBlameList: 
        blameLines = [line.rstrip('\n') for line in gitBlameList]
    fixedBlameLinesPath = newRepo + '/' + projectName + '_git_blame_java_files_fixed.csv'
    gitBlameFixedFile = io.open(fixedBlameLinesPath, "w+", encoding="utf-8")
    nbBlamesToCheck = len(blameLines)
    currentBlameIndex = 0
    firstLine = '"filename","author","date","line"'
    gitBlameFixedFile.write(firstLine + "\n")
    for blameLine in blameLines:
        currentBlameIndex = currentBlameIndex + 1
        print(str.format("Checking git blame line {curr}/{tot} ...", curr=currentBlameIndex, tot=nbBlamesToCheck))
        if(".java" in blameLine):
            removedHead = re.sub(r'^\w*\s', '', blameLine)
            removedTail = re.sub(r'\).*$', '', removedHead)
            removedOpenParen = re.sub(r'\s*\(', '","', removedTail)
            removedTimeZone = re.sub(r'\s(\+|\-)....\s*', '","', removedOpenParen)
            fixedDate = re.sub(r'\s*(\d\d\d\d\-\d\d\-\d\d\s\d\d\:\d\d\:\d\d)', r'","\1', removedTimeZone)
            finalString = '"'+fixedDate+'"' 
            gitBlameFixedFile.write(finalString + "\n")
    gitBlameFixedFile.close()


# ================================================================================
# READ REPOS TO ANALYZE IN TEXT FILE
# ================================================================================
print("----------------------------------------------------------------------------------")
lines = openRepoFile()
repositoryCounter = 0


# ================================================================================
# MAIN LOOP (LOOPS ON ALL REPOS IN FILE)
# ================================================================================
for gitURL in lines:
    
    repositoryCounter = repositoryCounter + 1

    # Get project name from URL
    p = Path(gitURL)
    projectName = p.parts[-1]

    # Setup directory names
    newRepo = repo_dir + '/' + projectName
    downloadRepo = newRepo + '/' + projectName + '_repo'  

    # Clone repo into directory
    cloneRepo(gitURL,downloadRepo)

    # Create CSV file for commits and write info into commit file
    generateCommitsCSVFile(newRepo,projectName,downloadRepo)

    # Run PMD and save results into CSV file
    generatePMDOutputCSVFile(newRepo,projectName,downloadRepo)

    # Get number of commits per author (CSV seperated by TABS)
    generateNbCommitsPerAuthorCSVFile(newRepo,projectName,downloadRepo)

    # Get a list of all files in repo (text file)
    listOfFilesInRepo = generateListOfAllFilesTextFile(newRepo,projectName,downloadRepo)

    # Get the raw output of Git Blame in a text file and then create new CSV file with Git Blame output
    generateGitBlameOutputCSVFile(newRepo,projectName,downloadRepo,listOfFilesInRepo)   


# ================================================================================
# END MESSAGES
# ================================================================================
print(str.format("All done! Check in '{repoDir}' directory.", repoDir=repo_dir))
print(str.format("Analyzed {nbRepos} repositories.", nbRepos=repositoryCounter))
