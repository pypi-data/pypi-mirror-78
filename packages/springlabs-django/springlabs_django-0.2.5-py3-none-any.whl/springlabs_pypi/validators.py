import click
import os
import json

try:
    with open('springlabs_django.json') as file:
        data = json.load(file)
    versions = data["versions"]
    project_name = data["project_name"]
except:
    message = "Command python_django should be executed in root project (springlabs_django.json)"
    raise click.BadParameter(message)


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
