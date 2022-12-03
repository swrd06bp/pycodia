import os
import re
import requests
from getpass import getpass
from pycodya import config
from pycodya.helpers import tools

class CodyaApi(object):
    def __init__(self, token_branch=""):
        self.token = self._extract_user_token()
        self.token_branch = token_branch if token_branch else self._extract_branch_token()
        self.base_url = "http://localhost:8080/api/v0"


    def _extract_user_token(self):
        if os.path.isfile(config.CREDS_GENERATED_FILE):
            with open(config.CREDS_GENERATED_FILE, 'r') as f:
                token = f.read()
            return token    
        else:
            return ""
    
    def _extract_branch_token(self):
        if os.path.isfile(config.BRANCH_TOKEN_FILE):
            with open(config.BRANCH_TOKEN_FILE, 'r') as f:
                branch_token = f.read()
            return branch_token    
        else:
            return ""


    def login(self):
        username = input("Username: ")
        password = getpass("Password: ")
        url = self.base_url + "/login"
        resp = requests.post(url, json={"username": username, "password": password})
        
        if resp.status_code == 200:    
            self.token = resp.json()["token"]
            
            if not os.path.isdir(config.DIR_GENERATED_ROOT):
                os.makedirs(config.DIR_GENERATED_ROOT)
            with open(config.CREDS_GENERATED_FILE, 'w') as f:
                f.write(self.token)
            print("login succesfull", username, password, self.token)
        else:
            print("Login unsuccessful", resp.text)

    def projects(self):
        token_branch = self._extract_branch_token()

        if not token_branch:
            print("No current project selected.. \n\n")
        else:
            url = self.base_url + "/branch-by-token"
            resp = requests.get(url, headers={'Authorization': 'bearer ' + token_branch})
            branch = resp.json()["branch"]
            project_id = branch["projectId"]
            url = self.base_url + "/project/" + project_id
            resp = requests.get(url, headers={'Authorization': 'bearer ' + self.token})
            if resp.status_code != 200:
                print("Please login first: pycodya login")
                return
            project = resp.json()["project"]
            print("You are currently on the project \033[1;3m{}\033[0m on branch \033[1;3m{}\033[0m\n\n".format(project["name"], branch["name"]))


        is_project_creation = input("What would you like to do:\n0 - Create a new project\n1 - Use an existing project\nPlease type 0 or 1: ")
        if is_project_creation != "0" and is_project_creation != "1":
            print("Wrong input: only 0 and 1 allowed") 
            return

        elif is_project_creation == "0":
            project_name = input("Please type the name of the project: ")
            if not bool(re.match("^[a-zA-Z0-9_]*$", project_name)): 
                print("Wrong input: no special characters please, only numbers letters and _ allowed" ) 
                return
            url = self.base_url + "/project"
            resp = requests.post(url, headers={'Authorization': 'bearer ' + self.token}, json={"name": project_name, "language": "pycodya"})
            if resp.status_code != 200:
                print("Please login first: pycodya login")
                return
            project_id = resp.json()["projectId"]
            url = self.base_url + "/project/" + project_id + "/branch"
            resp = requests.post(url, headers={'Authorization': 'bearer ' + self.token}, json={"name": "master"})
            branch_id = resp.json()["branchId"]
            url = self.base_url + "/branch/" + branch_id + "/token"
            resp = requests.get(url, headers={'Authorization': 'bearer ' + self.token})
            branch_token = resp.json()['token']
            with open(config.BRANCH_TOKEN_FILE, 'w') as f:
                f.write(branch_token)
            print("Project {} created with branch master. Please copy the token:\n{}".format(project_name, branch_token))
            return
        
        elif is_project_creation == "1":
            url = self.base_url + "/projects"
            resp = requests.get(url, headers={'Authorization': 'bearer ' + self.token})
            if resp.status_code != 200:
                print("Please login first: pycodya login")
                return
            all_projects = resp.json()["projects"]
            if not all_projects:
                print("No projects yet - please create one")
                return
            print("\nPlease see the list of all the projects:")
            for key, project in enumerate(all_projects):
                print("{} - {}".format(key, project["name"]))
            chosen_project = input("Please type a number to choose between the different projects: ")    
            if chosen_project.isnumeric() and int(chosen_project) >= 0 and int(chosen_project) < len(all_projects):
                project_id = all_projects[int(chosen_project)]["_id"]
                url = self.base_url + "/project/" + project_id + "/branches"
                resp = requests.get(url, headers={'Authorization': 'bearer ' + self.token})
                branches = resp.json()["branches"]
                chosen_branch = [b for b in branches if b["name"] == "master"] 
                chosen_branch_id = chosen_branch[0]["_id"]
                url = self.base_url + "/branch/" + chosen_branch_id + "/token"
                resp = requests.get(url, headers={'Authorization': 'bearer ' + self.token})
                branch_token = resp.json()['token']
                with open(config.BRANCH_TOKEN_FILE, 'w') as f:
                    f.write(branch_token)
                print("You chose the project {} on the branch master".format(all_projects[int(chosen_project)]["name"]))
                print(branch_token)
            else:    
                print("Wrong input, please type a number between 0 and {}".format(len(all_projects)))


            

    def logout(self):
        if os.path.isfile(config.CREDS_GENERATED_FILE):
            os.remove(config.CREDS_GENERATED_FILE)
        print("Logout successful")    

    def pull_data(self):
        url = self.base_url + '/branch/funcunittests'
        resp = requests.get(url, headers={'Authorization': 'bearer ' + self.token_branch})
        if resp.status_code != 200:
            print("No branch selected, please choose a project: pycodya projects")
            return
        data = resp.json()['unittestdata']
        print("Pulling from Codya")
        tools.create_unitestfiles(data)

    def _send_data(self, data):
        url = self.base_url + '/branch/funcunittest'
        print(data)
        requests.post(url, json=data, headers={'Authorization': 'bearer ' + self.token_branch})


