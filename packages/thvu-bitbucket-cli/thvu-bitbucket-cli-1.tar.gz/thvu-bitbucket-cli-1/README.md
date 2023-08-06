# Bitbucket-CLI

Inspired by [Github CLI](https://github.com/cli/cli), Bitbucket-CLI attempts to tackle the same goal for Bitbucket repositories i.e. an interactive tool to interact with your repository via CLI. It is built on [Bitbucket API](https://developer.atlassian.com/bitbucket/api/2/reference/resource/) - a REST api service developed by Atlassian. 

# Installation
## Using Pip
```bash
  $ pip install thvu-bitbucket-cli
```
## Manual
```bash
  $ https://github.com/thvu11/Bitbucket-CLI.git
  $ cd Bitbucket-CLI
  $ python setup.py install
```

## Configuration

```
export BITBUCKET_CLI_CREDENTIAL=/path/to/your/config
```

The config file must have the following format:
```
[CONFIG]
user: <your username>
password: <your password>
workspace: <your workspace>
repo_slug: <your repo slug>
```

# Usage
```bash
$ bb --help
$ bb pr --help    # available sub-commands for pull request command
$ bb issue --help # available sub-commands for issue command
```

# Development
Local development is done through a docker compose stack
Feel free to setup the environment variable `BITBUCKET_CLI_CREDENTIAL` to your mock config file
