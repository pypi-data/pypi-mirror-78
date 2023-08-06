import os
from typing import Optional

import click

from paten.constants import TEMPLATE_APP, GITIGNORE, WELCOME_PROMPT
from paten.utils import validate_function_app_name
from .factory import CliFactory


@click.group(invoke_without_command=True)
@click.option('--function-app-dir')
@click.pass_context
def cmd(ctx, function_app_dir: str):
    """
    root command for the `paten`.
    Currently, the sub-command below is supported:
    
    * build
    * deploy
    * new-project
    * plan
    
    """
    if function_app_dir is None:
        function_app_dir = os.getcwd()
    if ctx.invoked_subcommand is None:
        click.echo('This is parent!')
    ctx.obj['function_app_dir'] = function_app_dir
    ctx.obj['factory'] = CliFactory(function_app_dir=function_app_dir)


@cmd.command("deploy")
@click.option("--function-app-name")
@click.pass_context
def deploy(ctx, function_app_name: Optional[str] = None):
    """
    Deploy your app to Azure Functions via `Azure Functions Core Tools`.
    
    """
    cli_factory: CliFactory = ctx.obj['factory']
    paten_app = cli_factory.load_paten_app()
    paten_app.export()

    _function_app_name = paten_app.function_app_name if function_app_name is None else function_app_name
    if not validate_function_app_name(function_app_name=_function_app_name):
        click.echo(f"{_function_app_name} is invalid. Can only consists of `A-Z`, `a-z`, `0-9` and , `-`")
        return

    cli_factory.deploy(prompter=click, function_app_name=_function_app_name)


@cmd.command("build")
@click.pass_context
def build(ctx):
    """
    Build your app at directory `./.paten`.
    
    """
    cli_factory: CliFactory = ctx.obj['factory']
    paten_app = cli_factory.load_paten_app()
    paten_app.export()

    output_list = paten_app.plan()
    for s in output_list:
        click.echo(s)

    click.echo("\nyour function app is successfully built to `./.paten/*`")


@cmd.command("local")
@click.option("--azure-web-jobs-storage", help="Value for the AzureWebJobsStorage.")
@click.option('--port', default=7071, type=click.INT)
@click.option('--use-https', is_flag=True)
@click.pass_context
def local(ctx, azure_web_jobs_storage: Optional[str], port=7071, use_https=False):
    """
    Debug on local

    Args:
        ctx: shared context on click
        azure_web_jobs_storage: value for the AzureWebJobsStorage
        port: listen port
        use_https: use https

    """
    cli_factory: CliFactory = ctx.obj['factory']
    paten_app = cli_factory.load_paten_app()
    paten_app.export(azure_web_jobs_storage=azure_web_jobs_storage)

    cli_factory.local(prompter=click, port=port, use_https=use_https)


@cmd.command("plan")
@click.pass_context
def plan(ctx):
    """
    Display the function to deploy based script `app.py`.
    
    """
    cli_factory: CliFactory = ctx.obj['factory']
    paten_app = cli_factory.load_paten_app()
    output_list = paten_app.plan()
    for s in output_list:
        click.echo(s)

    click.echo("\ntype `paten build` to generate files to `./.paten/*`")


def _create_new_project_skeleton(function_app_name: str):
    """
    Create new function app at `./function_app_name` with sample script.
    
    """
    paten_dir = os.path.join(function_app_name, '.paten')
    os.makedirs(paten_dir)
    with open(os.path.join(function_app_name, 'requirements.txt'), 'w'):
        pass
    with open(os.path.join(function_app_name, 'app.py'), 'w') as f:
        f.write(TEMPLATE_APP % function_app_name)
    with open(os.path.join(function_app_name, '.gitignore'), 'w') as f:
        f.write(GITIGNORE)


@cmd.command("new-app")
@click.argument('function-app-name')
def new_app(function_app_name: str):
    """
    Create new Function App with sample python script.
    
    """
    if not validate_function_app_name(function_app_name=function_app_name):
        click.echo(f"{function_app_name} is invalid. Can only consists of `A-Z`, `a-z`, `0-9` and , `-`")
        return
    click.echo(WELCOME_PROMPT % function_app_name)
    _create_new_project_skeleton(function_app_name=function_app_name)


def main():
    cmd(obj={})
