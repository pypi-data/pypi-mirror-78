import click
import time
import os
import re
from springlabs_pypi.utils import createVersion
from springlabs_pypi.validators import *
from springlabs_pypi import __version__ as version


@click.group(invoke_without_command=False)
@click.version_option(version=version, prog_name="Springlabs Django Manager", message="%(prog)s, v%(version)s")
@click.pass_context
def cli(ctx):
    """Springlabs Django Manager."""
    ctx.invoked_subcommand


@cli.command()
@click.option('-ve', '--version',
              prompt='Inserta tu versión',
              help='Nueva version para la aplicación',
              callback=validate_version_version)
def create_version(version):
    """ Create a new version for django project """
    message, result = createVersion(version=version,
                                    project_name=project_name,
                                    old_versions=versions)
    if result == True:
        message = f"Se creó version '{version}' correctamente"
        click.secho(message, fg='green')
    else:
        message = "Error: " + message
        click.secho(message, fg='red')


if __name__ == '__main__':
    cli()
