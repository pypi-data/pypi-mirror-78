import os
import json

from .primary_functions import (
    appendContent,
    replaceContent,
    findNReplace,
    findNDelete,
    deleteContent,
    notRecursiveModify,
    recursiveModify,
    getRangeStr,
    getRangeEnds,
    generateBackup,
    reverseChanges,
    modifyFilesNewVersion,
    createDirectoriesNewVersion,
    modifyFilesNewAPI
)

def createVersion(version, project_name, old_versions):
    """
        Función encargada de crear nueva version en proyecto django

        Función encargada de crear nueva versión en proyecto django

        Parámetros:
            version         [String]    Nueva versión del proyecto
        Retorno:
            message,result  [Tuple]     Mensaje[String] y result[Boolean]
    """
    message, result = generateBackup(project_name=project_name)
    if result == False:
        message = "Ocurrió un error interno al crear respaldo"
        return message, False

    errors = []
    # Modifica archivos para nueva versión
    message, result = modifyFilesNewVersion(version=version,
        project_name=project_name,
        old_versions=old_versions)
    
    # Si falla al escribir archivos se agrega a arreglo
    if result == False:
        errors.append([message, True])
    
    # Crea directorios y archivos dentro para nueva versión
    message, result = createDirectoriesNewVersion(version=version,
        project_name=project_name,
        old_versions=old_versions)
    
    # Si falla al modificar directorios se agrega a arreglo
    if result == False:
        errors.append([message, True])
    try:
        with open('springlabs_django.json') as file:
            data = json.load(file)
    except:
        message = "Ocurrio un error interno al actualizar archivo springlabs_django.json"
        errors.append([message, True])
    else:
        objVersionDetail = {
            "version": version,
            "groups": ["users"]
        }
        data["versions"].append(version)
        data['versions_detail'].append(objVersionDetail)
        try:
            with open("springlabs_django.json", "w") as file:
                file.write(json.dumps(data))
        except:
            message = "Ocurrio un error interno al actualizar archivo springlabs_django.json"
            errors.append([message, True])

    for error in errors:
        if error[1] == True:
            message, result = reverseChanges(project_name=project_name)
            os.chdir("..")
            os.remove(project_name + ".zip")
            os.chdir(project_name)
            return error[0], False
    


    return "OK", True

def createAPI(version,group,name,http_verb,type_api,url,availability,project_name):
    """
        Función encargada de crear nueva api en proyecto django

        Función encargada de crear nueva api en proyecto django

        Parámetros:
            version         [String]    Versión donde se creará la API
            group           [String]    Grupo donde se creará la API
            name            [String]    Nombre de la API
            http_verb       [String]    HTTP Verb de la API (POST, PUT, DELETE)
            type_api        [String]    Tipo de la API (MODEL, OPEN)
            url             [String]    URL donde se podrá acceder a la API
            availability    [String]    Disponibilidad de la API (public, private)
            project_name    [String]    Nombre del proyecto
        Retorno:
            message,result  [Tuple]     Mensaje[String] y result[Boolean]
    """
    # Generar respaldo de proyecto
    message, result = generateBackup(project_name=project_name)
    if result == False:
        message = "Ocurrió un error interno al crear respaldo"
        return message, False

    errors = []

    # Modifica archivos para nueva api
    message, result = modifyFilesNewAPI(version=version,
        group=group,
        name=name,
        http_verb=http_verb,
        type_api=type_api,
        url=url,
        availability=availability,
        project_name=project_name)
    
    # Si falla al modificar directorios se agrega a arreglo
    if result == False:
        errors.append([message, True])


    try:
        with open('springlabs_django.json') as file:
            data = json.load(file)
    except:
        message = "Ocurrio un error interno al actualizar archivo springlabs_django.json"
        errors.append([message, True])
    else:
        objApis = {
            "api_name": name,
            "http_verb": http_verb,
            "api_type" : type_api,
            "url": url,
            "availability" : availability
        }
        versions_detail = data['versions_detail']
        # Recorremos todas las versiones
        for index_versions, versions in enumerate(versions_detail):
            # Si la versión del ciclo es en donde vamos a insertar la api
            if versions['version'] == version:
                groups_detail = versions["groups_detail"]
                # Recorremos todos los grupos de esa versión
                for index_groups, group_detail in enumerate(groups_detail):
                    # Si el grupo del ciclo es en donde vamos a insertar la api
                    if group == group_detail['group']:
                        data['versions_detail'][index_versions]['groups_detail'][index_groups]['apis'].append(objApis)
        try:
            with open("springlabs_django.json", "w") as file:
                file.write(json.dumps(data))
        except:
            message = "Ocurrio un error interno al actualizar archivo springlabs_django.json"
            errors.append([message, True])
    # Si algo sale mal revertir los cambios y eliminar respaldo
    for error in errors:
        if error[1] == True:
            message, result = reverseChanges(project_name=project_name)
            os.chdir("..")
            os.remove(project_name + ".zip")
            os.chdir(project_name)
            return error[0], False

    return "OK", True