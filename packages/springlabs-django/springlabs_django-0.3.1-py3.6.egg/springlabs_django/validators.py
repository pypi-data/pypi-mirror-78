import click
import os
import json

try:
    with open('springlabs_django.json') as file:
        data = json.load(file)
    versions = data["versions"]
    project_name = data["project_name"]
    versions_detail=data["versions_detail"]
except:
    message = "Command python_django should be executed in root project (springlabs_django.json)"
    raise click.BadParameter(message)

groups_api = ["options"]

def validate_manage():
    """
        Función que valida si se ejecuta comando en raiz de proyecto Django

        Función que valida si se ejecuta comando en la raiz del proyecto
        Django basandonos en el archivo manage.py
        Parámetros:
        Retorno:
            message,result      [Tuple] Mensaje de respuesta, Resultado booleano
        Excepciones:
            click.BadParameter  [Raise] Mensaje de parámetro incorrecto
    """
    list_dir = os.listdir()
    if not "manage.py" in list_dir:
        message = "Command python_django should be executed in root project (manage.py)"
        return message, False
    return "OK", True


def validate_version_version(ctx, param, value):
    """
        Función que valida versión de subcomando create-version

        Función que valida si versión recibida es de tipo entero
        (ej. 1,2,3,4,...,n) y no existe ya una versión creada con ese
        número

        Parámetros:
            ctx         [Click Object]  Contexto de click
            param       [Click Option]  Parametro recibido
            value       [String]        Valor recibido como parámetro
        Retorno:
            value       [String]        Valor recibido como parámetro
        Excepciones:
            click.BadParameter  [Raise] Mensaje de parámetro incorrecto
    """
    message, result = validate_manage()
    if result == False:
        raise click.BadParameter(message)

    if not value.isdigit():
        message = f"Incorrect version '{value}'. It should be a integer value"
        raise click.BadParameter(message)
    if str(value) in versions:
        message = f"Duplicate version '{value}'. It should be a unique value"
        raise click.BadParameter(message)
    return value

def validate_api_name(ctx, param, value):
    """
        Función que valida que nombre de api este en formato correcto

        Función que valida que el nombre de la api este con formato correcto,
        es decir que solo sea alfanumérico

        Parámetros:
            ctx         [Click Object]  Contexto de click
            param       [Click Option]  Parametro recibido
            value       [String]        Valor recibido como parámetro
        Retorno:
            value       [String]        Valor recibido como parámetro
        Excepciones:
            click.BadParameter  [Raise] Mensaje de parámetro incorrecto
    """
    if value.isalnum():
        if not len(value) > 3 and len(value) < 16: 
            message = "The api name must only contain letters and numbers (3-15 characters)"
            raise click.BadParameter(message)
    else:
        message = "The api name must only contain letters and numbers (3-15 characters)"
        raise click.BadParameter(message)
    return value

def validate_api_version(ctx, param, value):
    """
        Función que valida versión de subcomando create-api

        Función que valida los grupos disponibles para generar una nueva
        api y llenar lista de choices en campo group de nueva api

        Parámetros:
            ctx         [Click Object]  Contexto de click
            param       [Click Option]  Parametro recibido
            value       [String]        Valor recibido como parámetro
        Retorno:
            value       [String]        Valor recibido como parámetro
        Excepciones:
            click.BadParameter  [Raise] Mensaje de parámetro incorrecto
    """
    try:
        with open('springlabs_django.json') as file:
            data = json.load(file)
    except:
        message = "Ocurrió un problema interno al leer archivo (springlabs_django.json)"
        raise click.BadParameter(message)
    else:
        versions_detail = data['versions_detail']
        # Recorremos todas las versiones
        for versions in versions_detail:
            # Si la versión del ciclo es en donde vamos a insertar la api
            if versions['version'] == value:
                groups_api.remove("options")
                # Agregamos los grupos disponibles de esta version a la lista de grupos
                groups_api.extend(versions['groups'])
                return value
        message = "No existen grupos creados en esta version"
        raise click.BadParameter(message)
    

def validate_api_name_verb(ctx, param, value):
    """
        Función que valida nombre de subcomando create-api

        Función que valida que nombre de la api no se encuentre ya registrado
        en la misma versión y mismo HTTP VERB de la aplicación.

        Parámetros:
            ctx         [Click Object]  Contexto de click
            param       [Click Option]  Parametro recibido
            value       [String]        Valor recibido como parámetro
        Retorno:
            value       [String]        Valor recibido como parámetro
        Excepciones:
            click.BadParameter  [Raise] Mensaje de parámetro incorrecto
    """

    api_version = ctx.params['version']
    name_api = ctx.params['name']
    group_api = ctx.params['group']
    try:
        with open('springlabs_django.json') as file:
            data = json.load(file)
    except:
        message = "Ocurrió un problema interno al leer archivo (springlabs_django.json)"
        raise click.BadParameter(message)
    else:
        versions_detail = data['versions_detail']
        names_no_valid = []
        # Recorremos todas las versiones
        for versions in versions_detail:
            # Si la versión del ciclo es en donde vamos a insertar la api
            if versions['version'] == api_version:
                groups_detail = versions["groups_detail"]
                # Recorremos todos los grupos de esa versión
                for group_detail in groups_detail:
                    # Si el grupo del ciclo es en donde vamos a insertar la api
                    if group_api == group_detail['group']:
                        apis = group_detail['apis']
                        # Recorremos todas las apis de ese grupo
                        for api in apis:
                            verb = api["http_verb"]
                            name = api["api_name"]
                            name_verb = name.lower() + verb.upper()
                            # Agregamos a lista de names_no_valid los nombres de api no validos
                            names_no_valid.append(name_verb)
        find = name_api.lower() + value.upper()
        # Si el nombre de nuestra api ya se encuentra en el proyecto
        if find in names_no_valid:
            message = f"El nombre de la api '{name_api}' con el HTTP '{value}' ya se encuentra registrado en la aplicación"
            raise click.BadParameter(message)
        return value

def validate_api_url(ctx, param, value):
    """
        Función que valida url de subcomando create-api

        Función que valida que url de la api no se encuentre ya registrado
        en la misma versión.

        Parámetros:
            ctx         [Click Object]  Contexto de click
            param       [Click Option]  Parametro recibido
            value       [String]        Valor recibido como parámetro
        Retorno:
            value       [String]        Valor recibido como parámetro
        Excepciones:
            click.BadParameter  [Raise] Mensaje de parámetro incorrecto
    """

    api_version = ctx.params['version']
    # Validar que url no empiece en /
    if value.startswith("/") or value.endswith("/"):
        message = "La url no puede comenzar ni terminar con el caracter '/'"
        raise click.BadParameter(message)

    # Validar que parametros de url sean correctos
    urls = value.split("/")
    for url in urls:
        
        # Si empieza con parentesis se refiere a un argumento de la url
        if "(" in url:
            # Si NO empieza con (?P< y termina con ) es parámetro incorrecto
            if not url.startswith("(?P<") and url.endswith(")"):
                message = "Parámetro de url invalido"
                raise click.BadParameter(message)
            # Si la cantidad de parentesis de apertura '(' es diferente a los de cierre ')' es parámetro incorrecto
            if not url.count("(") == url.count(")"):
                message = "Parámetro de url invalido"
                raise click.BadParameter(message)
            # Si la cantidad de diplés de apertura '<' es diferente a los de cierre '>' es parámetro incorrecto
            if not url.count("<") == url.count(">"):
                message = "Parámetro de url invalido"
                raise click.BadParameter(message)
    try:
        with open('springlabs_django.json') as file:
            data = json.load(file)
    except:
        message = "Ocurrió un problema interno al leer archivo (springlabs_django.json)"
        raise click.BadParameter(message)
    else:
        versions_detail = data['versions_detail']
        names_no_valid = []
        for versions in versions_detail:
            if versions['version'] == api_version:
                groups_detail = versions["groups_detail"]
                for group_detail in groups_detail:
                    apis = group_detail['apis']
                    for api in apis:
                        url = api["url"]
                        names_no_valid.append(url)
        if value in names_no_valid:
            message = f"La url '{value}' ya se encuentra registrada en el proyecto"
            raise click.BadParameter(message)
        return value

def validate_graph_name(ctx, param, value):
    """
        Función que valida que nombre de graph este en formato correcto

        Función que valida que el nombre de graph este con formato correcto,
        es decir que solo sea alfanumérico

        Parámetros:
            ctx         [Click Object]  Contexto de click
            param       [Click Option]  Parametro recibido
            value       [String]        Valor recibido como parámetro
        Retorno:
            value       [String]        Valor recibido como parámetro
        Excepciones:
            click.BadParameter  [Raise] Mensaje de parámetro incorrecto
    """
    if value.isalnum():
        if not len(value) > 3 and len(value) < 16: 
            message = "The graph name must only contain letters and numbers (3-15 characters)"
            raise click.BadParameter(message)
    else:
        message = "The graph name must only contain letters and numbers (3-15 characters)"
        raise click.BadParameter(message)
    
    graph_version = ctx.params['version']
    group_graph = ctx.params['group']
    name_graph = value
    try:
        with open('springlabs_django.json') as file:
            data = json.load(file)
    except:
        message = "Ocurrió un problema interno al leer archivo (springlabs_django.json)"
        raise click.BadParameter(message)
    else:
        versions_detail = data['versions_detail']
        names_no_valid = []
        # Recorremos todas las versiones
        for versions in versions_detail:
            # Si la versión del ciclo es en donde vamos a insertar el graph
            if versions['version'] == graph_version:
                groups_detail = versions["groups_detail"]
                # Recorremos todos los grupos de esa versión
                for group_detail in groups_detail:
                    # Si el grupo del ciclo es en donde vamos a insertar el graph
                    if group_graph == group_detail['group']:
                        graphs = group_detail['graph']
                        # Recorremos todas las apis de ese grupo
                        for graph in graphs:
                            name = graph["graph_name"]
                            name_no_valid = name.lower()
                            # Agregamos a lista de names_no_valid los nombres de los graphs no validos
                            names_no_valid.append(name_no_valid)
        find = name_graph.lower()
        # Si el nombre de nuestro graph ya se encuentra en el proyecto
        if find in names_no_valid:
            message = f"El nombre del graph '{name_graph}' ya se encuentra registrado en la aplicación"
            raise click.BadParameter(message)
        return value
    return value

def validate_group_group(ctx, param, value):
    
    message, result = validate_manage()
    if result == False:
        raise click.BadParameter(message)
    insertversion=ctx.params["version"]

    for detail in versions_detail:
        if detail["version"]==insertversion:
            if value.upper() in (gr.upper() for gr in detail["groups"]):
                message = f"group '{value}' already exists in version '{insertversion}'"
                raise click.BadParameter(message)
    return value