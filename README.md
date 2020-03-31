# MGL843 - Final Project - README
## Author: Mario Morra

The following steps should be followed to run the script. First, some things need to be installed (if not done already).


## 1) Install Python 3.4+
> https://www.python.org/downloads/

Note: if on Windows, Python should be added to the PATH variable
Example: "C:\Users\Mario Morra\AppData\Local\Programs\Python\Python36-32\"


## 2) Install PMD
> https://pmd.github.io/

Note: if on Windows, PMD should be added to the PATH variable
Example: "C:\Program Files\PMD\pmd-bin-6.22.0\bin"


## 3) Install Git
> https://git-scm.com/downloads

Note: if on Windows, Git should be added to the PATH variable
Example: "C:\Program Files\Git\cmd"


## 4) Install necessary packages using pip (GitPython and PyDriller)
> pip install --upgrade pip
> pip install GitPython
> pip install PyDriller


## 5) Choose what projects to pull in the "github_repos.txt" file
To test the script, you might not want to actually download all 5 repos and generate all the CSV files. It can take many hours to complete. You can remove some of the projects by simply deleting lines in the "github_repos.txt" file. I recommend keeping only the following line:
> https://github.com/apache/commons-text
That project is fairly small and the execution of the whole script will be done in minutes.


## 6) Run the script
On Windows, go in the folder containing the script and open a new command prompt:
> python script.py


## Notes
- If desired, you can change the dump folder or GitHub repo text file. By default, the script will look in the local folder for a text file called "github_repos.txt" and a folder named "DUMP". If you wish to change this for whatever reason, you can do so by changing the 2 global variables at the beginning of the script. You can write the full path to the desired file / folder.
- The script is very verbose. If you wish to remove the comments, you must comment out each "print" line in the script. However, the PMD output is huge and unfortunately cannot be disabled.
- At the end of the script's execution, you should see a folder for each repo in the "github_repos.txt" file labeled with the project name. In each of these folders, you should find:
  - "ProjectName_repo": a folder containing the entire cloned repo
  - "ProjectName_all_files_in_repo.txt": a text file containing the list of all files in the repo
  - "ProjectName_commits.csv": a CSV file containing a list of all modifications (and commits) in the entire project
  - "ProjectName_git_blame_java_files.txt": a text file containing the combined output of all Git Blames executed on all Java files in the repo
  - "ProjectName_git_blame_java_files_fixed.txt": a CSV file containing a well formatted and cleaned list of the previous file's output
  - "ProjectName_nb_commits_per_author.csv": a CSV file containing the output of a Git shortlog command to get the number of commits per author in the project (note: this file is no longer used and the CSV separator is TABS)
  - "ProjectName_pmd_smells.csv": a CSV file containing the output of a PMD command run on the project with only the "design" ruleset