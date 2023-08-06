import os
import json
import re
import configparser

from .Utils import error

class Config:
    def __init__(self):
        self.branch_dict = self.get_repo_config()

        config = configparser.ConfigParser()
        config.read(os.environ['BITBUCKET_CLI_CREDENTIAL'])
        
        if 'CONFIG' not in config:
            return self.incorrect_config_setup()

        for required_key in [ 'user', 'password', 'workspace', 'repo_slug' ]:
            if required_key not in config['CONFIG']:
                return self.incorrect_config_setup()

        data = config['CONFIG']

        self.user = data['user']
        self.password = data['password']
        self.workspace = data['workspace']
        self.repo_slug = data['repo_slug']

        self.url = 'https://api.bitbucket.org/2.0/repositories'
        self.base_url = self.url + '/' + self.workspace + '/' + self.repo_slug

    def get_config(self):
        return {
            'user': self.user,
            'password': self.password,
            'workspace': self.workspace,
            'repo': self.repo_slug,
            'api': self.url
        }

    def get_repo_config(self):
        git_directory = os.getcwd() + '/.git'
        if not os.path.isdir(git_directory):
            error('Error: not a git repository (or any of the parent directories): .git')

        current_branch = None
        with open(git_directory + '/HEAD') as git_head_file:
            content = git_head_file.read()
            current_branch = re.search('heads/(.*)', content).group(1)

        available_remote_branches = [f for f in os.listdir(git_directory + '/refs/remotes/origin')]

        return {
            'my_branch': current_branch,
            'available_branch': available_remote_branches
        }

    def incorrect_config_setup(self):
        instruction = """
            Incorrect configuration
            
            Remember to set the environment variable for the config file
                export BITBUCKET_CLI_CREDENTIAL=/path/to/your/config

            The config file must have the following format:

            [CONFIG]
            user: <your username>
            password: <your password>
            workspace: <your workspace>
            repo_slug: <your repo slug>
        """
        error(instruction)
