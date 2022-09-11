import requests
import csv
import sys
from bs4 import BeautifulSoup

repo = sys.argv[1]
#if repo is not a valid URL, exit the script
if not repo.startswith('https://github.com/') or repo.startswith('https://www.github.com/'):
    print('Invalid URL')
    sys.exit(1)


def getdependents(repo): 
    #make a request to the repo's dependents page
    if not '/network/dependents' in repo:
        r = requests.get(repo + '/network/dependents')
    else:
        r = requests.get(repo)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        #find all the links to the dependent repos
        links = soup.find_all('a', class_ = 'btn-link selected')
        #create a list that will hold the URLs of the dependent repos
        dependents = []
        #for each link, extract the URL and append it to the list
        for link in links:
            dependents.append(link['href'])
        return dependents
    else:
        print('Error: ' + str(r.status_code))
        print(repo)
        sys.exit(1)


def searchFile(expression):
    expression = sys.argv[2]
    dependentURLs = []
    #make a request to the repo's search page
    r = requests.get(repo + '/search?q=' + expression)
    #if the request is successful, parse the HTML
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        #find all the links to the files containing the expression
        links = soup.find_all('a', class_ = 'js-navigation-open')
        #create a list that will hold the URLs of the files containing the expression
        files = []
        #for each link, extract the URL and append it to the list
        for link in links:
            files.append(link['href'])
        for file in files:
            dependentURL = file.split('/blob/')[0]
            dependentURLs.append(dependentURL)
        return files
        return dependentURLs
    else:
        print('Error: ' + str(r.status_code))
        sys.exit(1)

def filters(tags, name):
    dependents = getdependents(repo)
    #if there is a -t or --tag option, filter the repos by tag. Arguments can be combined or used in any order, eg. -tr or -rt or depindutil.py -tr $1 $2 or depfindutil.py $1 $2 -rt ${tag} 
    if '-t' or '--tag' or '-tn' or '-n -t' or '-nt' or '-t -n' in sys.argv[1:6]: 
        for dependent in dependents:
        #make a request to the dependent's tags page
            r = requests.get(dependent + '/tags')
        #if the request is successful, parse the HTML
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
            #find all the tags
                tags = soup.find_all('a', class_ = 'tag')
            #create a list that will hold the tags
                tags = []
            #for each tag, extract the text and append it to the list
            for tag in tags:
                tags.append(tag.text)
            #if the tag is not in the list, remove the repo from the list
            if name not in tags:
                dependents.remove(dependent)
            elif '-n' or '--name' in sys.argv[1:6]:
                for dependent in dependents:
                    r = requests.get(dependent)
                    #if the request is successful, check if the URL contains the name. Regex must be supported
                    #we are looking for the name that is passed after the -n or --name option
                    targetname =  [sys.argv[sys.argv.index('-n') + 1] if '-n' in sys.argv else sys.argv[sys.argv.index('--name') + 1]]
                    if r.statuscode == 200:
                        if targetname not in dependent:
                            dependents.remove(dependent)

                     
    return dependents

#now we will create two functions, one to print the repos containing the file(s) (called with -r or --repos), and one to print the files containing the expression + a string "in repo" + the repo's URL (called with the -f or --full option)
def printRepos(repos):
    for repo in repos:
        print(repo)

def printFull(files, repos):
    for file in files:
        print(file + ' in repo ' + repos[files.index(file)])

#now we will create a function that will print the results in a CSV file (called with the -c or --csv option)
def printCSV(files, repos):
    #create a list that will hold the results
    results = []
    #for each file, append a list containing the file's URL and the repo's URL to the results list
    for file in files:
        results.append([file, repos[files.index(file)]])
    #create a CSV file
    with open('results.csv', 'w') as f:
        writer = csv.writer(f)
        #write the results to the CSV file
        writer.writerows(results)
    
#parse the arguments passed to the script
if not '-n' or '--name' or '-t' or '--tag' in sys.argv[1:6]:
    #if there is no -n or --name option, search for the expression in all the repos
    dependents = getdependents(repo)
    #create a list that will hold the files containing the expression
    files = []
    #iterate over the dependentURLs list, calling the searchFile function for each repo
    searchFile(sys.argv[2])
    #if there is no -r or --repos option, print the files containing the expression
    if '-r' or '--repos' not in sys.argv[1:6]:
        printFull(files, dependents)
    #if there is a -r or --repos option, print the repos containing the files
    elif '-r' or '--repos' in sys.argv[1:6]:
        printRepos(dependents)
    #if there is a -c or --csv option, print the results in a CSV file
    if '-c' or '--csv' in sys.argv[1:6]:
        printCSV(files, dependents)
    else:
        #use the filters function to filter the repos by tag and/or name and then search for the expression in the filtered repos and print the results
        print("Sorry, this option is not supported yet")

