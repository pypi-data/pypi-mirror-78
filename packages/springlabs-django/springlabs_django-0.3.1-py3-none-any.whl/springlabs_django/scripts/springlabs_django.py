import click
import time
import os
import re
from springlabs_django.utils import createVersion, createAPI, createGraph, getVersions, createGroup
from springlabs_django.validators import *
from springlabs_django import __version__ as version


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

@cli.command()
@click.option('-ve','--version',
	prompt='Inserta la versión',
	help='Version a la que se agregara el grupo',
	type=click.Choice(getVersions(), case_sensitive=False)
	)
@click.option('-gr','--group',
	prompt='Inserta el nombre del grupo' ,
	help='Nuevo grupo para la aplicación',
	callback=validate_group_group)
def create_group(group,version):
	""" Create a new group for django project """
	message, result = createGroup(version=version,
		group=group,
		project_name=project_name
		)
	if result == True:
		message = f"Se creó el grupo '{group}' correctamente"
		click.secho(message, fg='green')
	else:
		message = "Error: " + message
		click.secho(message, fg='red')


@cli.command()
@click.option('-ve', '--version',
    prompt='Versión a utilizar',
    type=click.Choice(versions, case_sensitive=False),
    help='Version to use',
    callback=validate_api_version)
@click.option('-g', '--group',
    prompt='Grupo a utilizar',
    type=click.Choice(groups_api, case_sensitive=False),
    help='Group to use')
@click.option('-n', '--name',
    prompt='Nombre de tu API',
    help='API name',
    callback=validate_api_name) 
@click.option('-http', '--http_verb',
    prompt='Verbo http a utilizar',
    default="POST",
    type=click.Choice(["POST","PUT","DELETE"], case_sensitive=False),
    show_default=True,
    help='HTTP Verb to use in api',
    callback=validate_api_name_verb)
@click.option('-t', '--type_api',
    prompt='Tipo de api a crear',
    default="open",
    type=click.Choice(["model","open"], case_sensitive=False),
    show_default=True,
    help='API type')
@click.option('-u', '--url',
    prompt='Inserta la url de la api',
    help='API url',
    callback=validate_api_url)
@click.option('-a', '--availability',
    prompt='Disponibilidad de tu API',
    default="public",
    type=click.Choice(["public","private"], case_sensitive=False),
    show_default=True,
    help='API availability')
def create_api(version,group,name,http_verb,type_api,url,availability):
    """ Create a new api for django project """
    message, result = createAPI(version=version,
        group=group,
        name=name,
        http_verb=http_verb,
        type_api=type_api,
        url=url,
        availability=availability,
        project_name=project_name)
    if result == True:
        message = f"Se creó api '{name}' correctamente"
        click.secho(message, fg='green')
    else:
        message = "Error: " + message
        click.secho(message, fg='red')

@cli.command()
@click.option('-ve', '--version',
    prompt='Versión a utilizar',
    type=click.Choice(versions, case_sensitive=False),
    help='Version to use',
    callback=validate_api_version)
@click.option('-g', '--group',
    prompt='Grupo a utilizar',
    type=click.Choice(groups_api, case_sensitive=False),
    help='Group to use')
@click.option('-n', '--name',
    prompt='Nombre de tu graph',
    help='GraphQL name',
    callback=validate_graph_name) 
@click.option('-t', '--type_graph',
    prompt='Tipo de graph a crear',
    default="open",
    type=click.Choice(["model","open"], case_sensitive=False),
    show_default=True,
    help='API type')
def create_graph(version, group, name,type_graph):
    """ Create a new graph for django project """
    message, result = createGraph(version=version,
        group=group,
        name=name,
        type_graph=type_graph,
        project_name=project_name)
    if result == True:
        message = f"Se creó graph '{name}' correctamente"
        click.secho(message, fg='green')
    else:
        message = "Error: " + message
        click.secho(message, fg='red')

if __name__ == '__main__':
	cli()
