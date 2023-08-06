import click
import os
from .bitbucketCLI.CmdIssue import CmdIssue
from .bitbucketCLI.CmdPullRequest import CmdPullRequest
from .bitbucketCLI.Utils import error
from .bitbucketCLI.Config import Config

class Repo:
    def __init__(self, home=None, debug=False):
        self.home = os.path.abspath(home or '.')
        self.debug = debug
        self.config = Config()

pass_repo = click.make_pass_decorator(Repo)


@click.group()
@click.option('--repo-home', envvar='REPO_HOME', default='.repo')
@click.option('--debug/--no-debug', default=False, envvar='REPO_DEBUG')
@click.pass_context
def cli(ctx, repo_home, debug):
    ctx.obj = Repo(repo_home, debug)


@cli.command()
@click.argument(
    'action',
    nargs=1,
    type=click.Choice(['view', 'create', 'status', 'close', 'list'], case_sensitive=False),
)
@click.option('--id', required=False, help='Target issue ID')
@click.option('--title', required=False, help='Title for the new issue')
@click.option('--content', required=False, help='Description for the new issue')
@pass_repo
def issue(repo, action, id, title, content):
    issue_obj = CmdIssue(repo.config)

    arg = None
    if action == 'create':
        if title is not None and content is not None:
            arg = { 'title': title, 'content': content }
        else:
            error("Title and description is required to create an issue")
    elif action != 'list':
        if id is None:
            error("ID is required to {} an issue".format(action))
        else:
            arg = id

    issue_hash = {
        'create': issue_obj.create,
        'status': issue_obj.status,
        'view': issue_obj.view,
        'close': issue_obj.close,
        'list': issue_obj.list
    }

    issue_hash[ action ](arg)


@cli.command()
@click.argument(
    'action',
    nargs=1,
    type=click.Choice(['view', 'create', 'status', 'close', 'list'], case_sensitive=False),
)
@click.option('--id', required=False, help='Target pull request ID')
@click.option('--title', required=False, help='Title for the new pull request')
@click.option('--content', required=False, help='Description for the new pull request')
@click.option('--branch', required=False, help='Specify the branch the new pull request wants to merge into')
@pass_repo
def pr(repo, action, id, title, content, branch):
    pr_object = CmdPullRequest(repo.config)

    arg = None
    if action == 'create':
        if title is not None and content is not None:
            arg = { 'title': title, 'description': content }

            if branch is not None:
                arg['branch'] = branch
        else:
            error("Title and description is required to create a pull request")
    elif action != 'list':
        if id is None:
            error("ID is required to {} a pull request".format(action))
        else:
            arg = id

    pr_hash = {
        'create': pr_object.create,
        'status': pr_object.status,
        'view': pr_object.view,
        'close': pr_object.close,
        'list': pr_object.list
    }
    pr_hash[ action ](arg)

