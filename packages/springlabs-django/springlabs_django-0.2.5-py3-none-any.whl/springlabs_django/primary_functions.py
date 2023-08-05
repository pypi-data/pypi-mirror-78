import os
import re
from zipfile import ZipFile
import shutil
import pkgutil


def appendContent(path, content, find=None, recursive=False):
    '''
    Agrega contenido al final del archivo especificado, si existe un valor en "find", agregará el contenido despues de la coincidencia.

    Atributos:
            path            [String]            Ruta de archivo a editar
            content         [String]            Nuevo contenido a agregar
            find            [String]            cadena a buscar, si es nulo el contenido se agregara al final
            recursive       [Boolean]           Indica si la operación será recursiva
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al crear el archivo
            OSError                             Error al escribir el contenido
    '''
    if not os.path.exists(path):
        return f'El archivo {path} no existe', False
    if find == None:
        try:
            """ if not os.path.exists(path):
                    open(path, "x")
            with open(f'{path}.bak', "w") as f:
                    f.write(open(path).read()) """
            with open(path, "a") as f:
                newContent = f'\n{content}'
                f.write(newContent)
            return f'Se actualizó correctamente el archivo: {path}', True
        except Exception as exc:
            return f'Error al escribir el contenido:{exc}', False
    else:
        if recursive == False:
            return notRecursiveModify(path, content, find, 'append')
        elif recursive == True:
            return recursiveModify(path, content, find, 'append')

        return f'Valor no válido para el parametro recursive', False


def replaceContent(path, content, start, end='--end', recursive=False):
    '''
    Remplaza cierto contenido del archivo especificado.

    Atributos:
            path            [String]            Ruta de archivo a editar
            content         [String]            Nuevo contenido a agregar
            start           [String]            Parametro a partir del cual se iniciará el remplazo hasta encontrar el parametro "end"
            recursive       [Boolean]           Indica si la operación será recursiva
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    if not os.path.exists(path):
        return f'El archivo {path} no existe', False

    starts = getRangeStr(path, start)
    ends = getRangeEnds(path, end)
    if ends == None or len(ends) == 0:
        return f'Tu archivo no cuenta con delimitadores de fin: "{end}"', False
    if starts == None or len(starts) == 0:
        return f'Tu archivo no cuenta con delimitadores de inicio: "{start}"', False
    textsReplace = []
    for idx, _ in enumerate(ends):
        if len(starts) <= idx or starts[idx][1] > ends[idx][0]:
            break
        textsReplace.append([starts[idx][1] + 1,  ends[idx][0] - 1])
    file = open(path).read()
    if len(textsReplace) == 0:
        return f'Tu archivo tiene mal los delimitadores de inicio "{start}" y/o los deliminatores de fin "{end}" , favor de verificar.', False
    if recursive == False:
        return notRecursiveModify(path, content, file[textsReplace[0][0]:textsReplace[0][1]], 'replace')
    elif recursive == True:
        try:
            for text in textsReplace:
                recursiveModify(
                    path, content, file[text[0]:text[1]], 'replace')
            return f'Se actualizó correctamente el archivo: {path}', True
        except Exception as exc:
            return f'Error al escribir el contenido: {exc}', False

    return f'Valor no válido para el parametro recursive', False


def findNReplace(path, content, find, recursive=False):
    '''
    Remplaza cierto contenido del archivo especificado.

    Atributos:
            path            [String]            Ruta de archivo a editar
            content         [String]            Nuevo contenido a agregar
            find            [String]            Se hará un "search & replace de la valor dado
            recursive       [Boolean]           Indica si la operación será recursiva
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    if not os.path.exists(path):
        return f'El archivo {path} no existe', False
    if recursive == False:
        return notRecursiveModify(path, content, find, 'replace')
    elif recursive == True:
        return recursiveModify(path, content, find, 'replace')

    return f'Valor no válido para el parametro recursive', False


def findNDelete(path, find, recursive=False):
    '''
    Elimina cierto contenido del archivo especificado.

    Atributos:
            path            [String]            Ruta de archivo a editar
            find            [String]            Se hará un "search & replace de la valor dado
            recursive       [Boolean]           Indica si la operación será recursiva
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    if not os.path.exists(path):
        return f'El archivo {path} no existe', False
    if recursive == False:
        return findNReplace(path, '', find)
    elif recursive == True:
        return findNReplace(path, '', find, recursive=True)

    return f'Valor no válido para el parametro recursive', False


def deleteContent(path, start, end='--end', recursive=False):
    '''
    Elimina cierto contenido del archivo especificado.

    Atributos:
            path            [String]            Ruta de archivo a editar
            start           [String]            Parametro a partir del cual se iniciará el remplazo hasta encontrar el parametro "end"
            recursive       [Boolean]           Indica si la operación será recursiva
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    if not os.path.exists(path):
        return f'El archivo no existe', False
    if recursive == False:
        return replaceContent(path, '', start, end)
    elif recursive == True:
        return replaceContent(path, '', start, end, recursive=True)

    return f'Valor no válido para el parametro recursive', False


def notRecursiveModify(path, content, find, type):
    '''
    Modifica un archivo dado, en la coincidencia "find" con el contenido de "content" (solo primera coincidencia).

    Atributos:
            path            [String]            Ruta de archivo a editar
            content         [String]            Nuevo contenido a agregar
            find            [String]            Se hará un "search & replace de la valor dado
            type	        [String]            Indica el tipo de operación
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    file = open(path).read()
    matchFound = False
    find = find.replace("(", r'\(')
    find = find.replace(")", r'\)')
    find = find.replace("{", r'\{')
    find = find.replace("}", r'\}')
    find = find.replace("[", r'\[')
    find = find.replace("]", r'\]')
    find = find.replace("+", r'\+')
    find = find.replace("<", r'\<')
    find = find.replace("-", r'\-')
    find = find.replace("!", r'\!')
    find = find.replace("*", r'\*')
    find = find.replace("~", r'\~')
    find = find.replace("¬", r'\¬')
    find = find.replace(",", r'\,')
    find = find.replace(":", r'\:')
    find = find.replace(".", r'\.')

    matches = re.finditer(find, file)
    for m in matches:
        matchFound = True
        break
    if matchFound == False:
        return f'No se encontraron coincidencias de "{find}"', False
    if type == 'append':
        newContent = f'{file[: m.end()]}  \n{content} \n{file[m.end() + 1:]}'
    elif type == 'replace':
        newContent = f'{file[: m.start()]}{content}{file[m.end():]}'
    else:
        return f'Tipo de remplazo no válido', False
    try:
        '''with open(f'{path}.bak', "w") as f:
                f.write(open(path).read())'''
        with open(path, "w") as f:
            f.write(newContent)
        return f'Se actualizó correctamente el archivo: {path}', True
    except Exception as exc:
        return f'Error al escribir el contenido: {exc}', False


def recursiveModify(path, content, find, type):
    '''
    Modifica un archivo dado, en la coincidencia "find" con el contenido de "content" de manera recursiva.

    Atributos:
            path            [String]            Ruta de archivo a editar
            content         [String]            Nuevo contenido a agregar
            find            [String]            Se hará un "search & replace de la valor dado
            type	        [String]            Indica el tipo de operación
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    if type == 'append':
        newContent = f'{find} \n{content}\n'
    elif type == 'replace':
        newContent = content
    else:
        return f'Tipo de remplazo no válido', False
    try:
        file = open(path).read()
        '''with open(f'{path}.bak', "w") as f:
			f.write(open(path).read())'''
        with open(path, "w") as f:
            f.write(file.replace(find, newContent))
        return f'Se actualizó correctamente el archivo: {path}', True
    except Exception as exc:
        return f'Error al escribir el contenido: {exc}', False


def getRangeStr(path, find):
    '''
    Obtiene los indices del primer y ultimo caracter del valor de "find".

    Atributos:
            path            [String]            Ruta de archivo a editar
            find            [String]            Se hará un search de la valor dado
    Retorno:
            arr          	[Lista]            Indices
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    arr = []
    file = open(path).read()
    find = find.replace("(", r'\(')
    find = find.replace(")", r'\)')
    find = find.replace("{", r'\{')
    find = find.replace("}", r'\}')
    find = find.replace("[", r'\[')
    find = find.replace("]", r'\]')
    find = find.replace("+", r'\+')
    find = find.replace("<", r'\<')
    find = find.replace("-", r'\-')
    find = find.replace("!", r'\!')
    find = find.replace("*", r'\*')
    find = find.replace("~", r'\~')
    find = find.replace("¬", r'\¬')
    find = find.replace(",", r'\,')
    find = find.replace(":", r'\:')
    find = find.replace(".", r'\.')

    matches = re.finditer(find, file)
    for m in matches:
        arr.append([m.start(), m.end()])
    return arr


def getRangeEnds(path, find):
    '''
    Obtiene los indices del primer y ultimo caracter de la linea donde se encuentre el valor de "find".

    Atributos:
            path            [String]            Ruta de archivo a editar
            find            [String]            Se hará un "search & replace de la valor dado
    Retorno:
            arr          	[Lista]            Indices
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    with open(path) as file:
        for line in file:
            if find in line:
                return getRangeStr(path, line)


def generateBackup(project_name, path=os.getcwd()):
    oldPath = path
    os.chdir("..")
    # TEST LOCAL
    #shutil.make_archive(project_name, 'zip', base_dir="springlabs-django-cli")
    # PRODUCTIVE
    shutil.make_archive(project_name, 'zip', base_dir=project_name)
    os.chdir(oldPath)
    return "OK", True
    


def reverseChanges(project_name, path=os.getcwd()):
    try:
        oldPath = path
        os.chdir("..")
        shutil.rmtree(project_name)
        botZip = f'{project_name}.zip'
        with ZipFile(botZip, 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())
        os.chdir(oldPath)
        return "OK", True
    except Exception as e:
        return str(e), False


def modifyFilesNewVersion(version, project_name, old_versions):
    """
        Función que modifica archivos para agregar nueva versión

        Función que modifica los archivos de Django en los que se tiene
        que agregar la nueva versión (No contempla nuevas carpetas)

    Args:
        version (String): Nueva versión del proyecto
        project_name (String): Nombre del proyecto
        old_versions (List): Lista de versiones existentes en proyecto
    Returns:
        message,result (Tuple): Mensaje[String] y result[Boolean]
    Exceptions:
        exception ([type]): [description]
    """

    errors = []
    # Crear version en project_name/urls.py
    # Importar public versions de nueva versión
    path = f"{project_name}/urls.py"
    find = "# PUBLIC VERSIONS URLS (Managed by SPRINGLABS_DJANGO)"
    content = f"from api.v{version}.public_urls import public_urls as public_urls_v{version}"
    message, result = appendContent(path=path,
        content=content,
        find=find)
    if result == False:
        errors.append([message, True])

    # Agregar nueva version a urls_versions
    find = "urls_versions ="
    for index, old_version in enumerate(old_versions):
        if index == 0:
            public_urls = f" public_urls_v{old_version}"
        else:
            public_urls = f" + public_urls_v{old_version}"
        find = find + public_urls
    content = find + f" + public_urls_v{version}"

    message, result = findNReplace(path=path,
        content=content,
        find=find)
    if result == False:
        errors.append([message, True])
    
    # Crear version en api/urls.py
    # Agregar nueva version a url_patterns
    path = "api/urls.py"
    find = "# VERSIONS URLS (Managed by SPRINGLABS_DJANGO)"
    content = f"""
    url(r'^v{version}/', include('api.v{version}.urls', namespace='v{version}')),"""
    message, result = appendContent(path=path,
        content=content,
        find=find)
    if result == False:
        errors.append([message, True])
    
    # Crear version en core/documentation.py
    # Crear variables urls de version
    path = "core/documentation.py"
    find = "# DOC STRING VERSIONS (Managed by SPRINGLABS_DJANGO)"
    content = f"""
# VERSION {version}.0
title_v{version}_0 = "{project_name} v{version}.0"
description_v{version}_0 = "Descripción del proyecto (v{version})"
namespace_v{version}_0 = "api-docs-v{version}-0"
urls_v{version}_0 = "api.v{version}.urls"
# END VERSION {version}.0"""
    message, result = appendContent(path=path,
        content=content,
        find=find)
    
    if result == False:
        errors.append([message, True])
    
    # Crear version en graphql_api/urls.py
    # Agregar nueva version a url_patterns
    path = "graphql_api/urls.py"
    find = "# VERSIONS URLS (Managed by SPRINGLABS_DJANGO)"
    content = f"""
    url(r'^v{version}/', include('graphql_api.v{version}.urls', namespace='v{version}')),"""
    message, result = appendContent(path=path,
        content=content,
        find=find)
    if result == False:
        errors.append([message, True])
    

    for error in errors:
        if error[1] == True:
            return error[0], False
    
    return "OK", True

def createDirectoriesNewVersion(version, project_name, old_versions):
    """
        Función que modifica directorios para agregar nueva versión

        Función que modifica los directorios de Django y sus archivos dentro 
        en los que se tiene que agregar la nueva versión

    Args:
        version (String): Nueva versión del proyecto
        project_name (String): Nombre del proyecto
        old_versions (List): Lista de versiones existentes en proyecto
    Returns:
        message,result (Tuple): Mensaje[String] y result[Boolean]
    Exceptions:
        exception ([type]): [description]
    """

    errors = []
    
    # Crear carpeta API nueva versión con archivos
    primary_package = "springlabs_django"
    os.chdir("api")
    new_version = f"v{version}"
    os.mkdir(new_version)
    base_urls_py = "/core/new_version/api/baseUrls.py"
    base_public_urls_py = "/core/new_version/api/basePublicUrls.py"
    base_private_urls_py = "/core/new_version/api/basePrivateUrls.py"
    base_serializers_py = "/core/new_version/api/baseSerializers.py"
    base_views_py = "/core/new_version/api/baseViews.py"

    # Obtiene contenido de core/new_version/api/baseUrls.py
    try:
        template_urls_py = pkgutil.get_data(primary_package, base_urls_py).decode('utf-8')
        template_urls_py = template_urls_py.replace("name_version", new_version)
    except:
        message = f"Ocurrió un error interno en core/{new_version}/api/baseUrls.py"
        errors.append([message, True])

    # Obtiene contenido de core/new_version/api/basePublicUrls.py
    try:
        template_public_urls_py = pkgutil.get_data(primary_package, base_public_urls_py).decode('utf-8')
        template_public_urls_py = template_public_urls_py.replace("name_version", new_version)
    except:
        message = f"Ocurrió un error interno en core/{new_version}/api/basePublicUrls.py"
        errors.append([message, True])

    # Obtiene contenido de core/new_version/api/basePrivateUrls.py
    try:
        template_private_urls_py = pkgutil.get_data(primary_package, base_private_urls_py).decode('utf-8')
        template_private_urls_py = template_private_urls_py.replace("name_version", new_version)
    except:
        message = f"Ocurrió un error interno en core/{new_version}/api/basePrivateUrls.py"
        errors.append([message, True])

    # Obtiene contenido de core/new_version/api/baseSerializers.py
    try:
        template_serializers_py = pkgutil.get_data(primary_package, base_serializers_py).decode('utf-8')
    except:
        message = f"Ocurrió un error interno en core/{new_version}/api/baseSerializers.py"
        errors.append([message, True])

    # Obtiene contenido de core/new_version/api/baseViews.py
    try:
        template_views_py = pkgutil.get_data(primary_package, base_views_py).decode('utf-8')
    except:
        message = f"Ocurrió un error interno en core/{new_version}/api/baseViews.py"
        errors.append([message, True])

    # Escribe contenido base en archivo api/new_version/urls.py
    with open(f"{new_version}/urls.py", "w") as file:
        file. write(template_urls_py)
    
    # Escribe contenido base en archivo api/new_version/public_urls.py
    with open(f"{new_version}/public_urls.py", "w") as file:
        file. write(template_public_urls_py)
    
    # Escribe contenido base en archivo api/new_version/private_urls.py
    with open(f"{new_version}/private_urls.py", "w") as file:
        file. write(template_private_urls_py)
    os.mkdir(f"{new_version}/users")
    
    # Escribe contenido base en archivo api/new_version/users/serializers.py
    with open(f"{new_version}/users/serializers.py", "w") as file:
        file. write(template_serializers_py)
    
    # Escribe contenido base en archivo api/new_version/users/views.py
    with open(f"{new_version}/users/views.py", "w") as file:
        file. write(template_views_py)
    os.chdir("..")
    
    # Crear carpeta GRAPHQL_API nueva versión con archivos
    os.chdir("graphql_api")
    new_version = f"v{version}"
    os.mkdir(new_version)
    base_urls_py = "/core/new_version/graphql_api/baseUrls.py"
    base_api_py = "/core/new_version/graphql_api/baseApi.py"
    base_schema_py = "/core/new_version/graphql_api/baseSchema.py"
    base_types_py = "/core/new_version/graphql_api/baseTypes.py"

    # Obtiene contenido de core/new_version/graphql_api/baseUrls.py
    try:
        template_urls_py = pkgutil.get_data(primary_package, base_urls_py).decode('utf-8')
        template_urls_py = template_urls_py.replace("name_version", new_version)
    except:
        message = f"Ocurrió un error interno en core/{new_version}/graphql_api/baseUrls.py"
        errors.append([message, True])

    # Obtiene contenido de core/new_version/graphql_api/baseApi.py
    try:
        template_api_py = pkgutil.get_data(primary_package, base_api_py).decode('utf-8')
    except:
        message = f"Ocurrió un error interno en core/{new_version}/graphql_api/baseApi.py"
        errors.append([message, True])


    # Obtiene contenido de core/new_version/graphql_api/baseSchema.py
    try:
        template_schema_py = pkgutil.get_data(primary_package, base_schema_py).decode('utf-8')
    except:
        message = f"Ocurrió un error interno en core/{new_version}/graphql_api/baseSchema.py"
        errors.append([message, True])

    # Obtiene contenido de core/new_version/graphql_api/baseTypes.py
    try:
        template_types_py = pkgutil.get_data(primary_package, base_types_py).decode('utf-8')
    except:
        message = f"Ocurrió un error interno en core/{new_version}/graphql_api/baseTypes.py"
        errors.append([message, True])

    # Escribe contenido base en archivo graphql_api/new_version/urls.py
    with open(f"{new_version}/urls.py", "w") as file:
        file. write(template_urls_py)
    
    # Escribe contenido base en archivo graphql_api/new_version/api.py
    with open(f"{new_version}/api.py", "w") as file:
        file. write(template_api_py)
    os.mkdir(f"{new_version}/users")
    
    # Escribe contenido base en archivo graphql_api/new_version/users/schema.py
    with open(f"{new_version}/users/schema.py", "w") as file:
        file. write(template_schema_py)
    
    # Escribe contenido base en archivo graphql_api/new_version/users/types.py
    with open(f"{new_version}/users/types.py", "w") as file:
        file. write(template_types_py)
    os.chdir("..")

    # Crear carpeta TESTS nueva versión con archivos
    os.chdir("tests")
    new_version = f"v{version}"
    os.mkdir(new_version)
    os.mkdir(f"{new_version}/integration_tests")
    os.mkdir(f"{new_version}/integration_tests/utils")
    os.mkdir(f"{new_version}/unit_tests")


    base_test_apis_py = "/core/new_version/tests/baseTestApis.py"
    base_test_functions1_py = "/core/new_version/tests/baseTestFunctions1.py"
    base_test_serializers_py = "/core/new_version/tests/baseTestSerializers.py"
    base_test_functions_py = "/core/new_version/tests/baseTestFunctions.py"

    # Obtiene contenido de core/new_version/tests/baseTestApis.py
    try:
        template_test_apis_py = pkgutil.get_data(primary_package, base_test_apis_py).decode('utf-8')
    except:
        message = f"Ocurrió un error interno en core/{new_version}/tests/baseTestApis.py"
        errors.append([message, True])
    
    # Obtiene contenido de core/new_version/tests/baseTestFunctions1.py
    try:
        template_test_functions1_py = pkgutil.get_data(primary_package, base_test_functions1_py).decode('utf-8')
    except:
        message = f"Ocurrió un error interno en core/{new_version}/tests/baseTestFunctions1.py"
        errors.append([message, True])
    
    # Obtiene contenido de core/new_version/tests/baseTestSerializers.py
    try:
        template_test_serializers_py = pkgutil.get_data(primary_package, base_test_serializers_py).decode('utf-8')
    except:
        message = f"Ocurrió un error interno en core/{new_version}/tests/baseTestSerializers.py"
        errors.append([message, True])
    
    # Obtiene contenido de core/new_version/tests/baseTestFunctions.py
    try:
        template_test_functions_py = pkgutil.get_data(primary_package, base_test_functions_py).decode('utf-8')
    except:
        message = f"Ocurrió un error interno en core/{new_version}/tests/baseTestFunctions.py"
        errors.append([message, True])
    

    # Escribe contenido base en archivo tests/new_version/integration_tests/test_apis.py
    with open(f"{new_version}/integration_tests/test_apis.py", "w") as file:
        file. write(template_test_apis_py)
    
    # Escribe contenido base en archivo tests/new_version/integration_tests/test_functions1.py
    with open(f"{new_version}/integration_tests/test_functions1.py", "w") as file:
        file. write(template_test_functions1_py)
    
    # Escribe contenido base en archivo tests/new_version/integration_tests/test_serializers.py
    with open(f"{new_version}/integration_tests/test_serializers.py", "w") as file:
        file. write(template_test_serializers_py)
    
    # Escribe contenido base en archivo tests/new_version/unit_tests/test_functions.py
    with open(f"{new_version}/unit_tests/test_functions.py", "w") as file:
        file. write(template_test_functions_py)
    os.chdir("..")
    
    for error in errors:
        if error[1] == True:
            return error[0], False
    
    return "OK", True

def modifyFilesNewAPI(version,group,name,http_verb,type_api,url,availability,project_name):
    """
        Función encargada de modificar archivos para nueva api en django

        Función encargada de modificar los archivos necesarios para crear una nueva api
        en el proyecto django.

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
    errors = []
    primary_package = "springlabs_django"
    
    # Obtener variables dependientes del HTTP_VERB
    if http_verb == "POST":
        base_views = "post_views_"
        base_serializers = "post_serializers_"
    elif http_verb == "PUT":
        base_views = "put_views_"
        base_serializers = "put_serializers_"
    elif http_verb == "DELETE":
        base_views = "delete_views_"
        base_serializers = "delete_serializers_"
    
    # Obtener variables dependientes del TYPE_API
    if type_api=="open":
        base_views = base_views+"open.py"
        base_serializers = base_serializers+"open.py"
    elif type_api=="model":
        base_views = base_views+"model.py"
        base_serializers = base_serializers+"model.py"
    
    # Obtener variables dependientes del AVAILABILITY
    if availability=="public":
        general_urls = "public_urls.py"
    elif availability=="private":
        general_urls = "private_urls.py"
    
    base_views_py = f"/core/new_api/api/{base_views}"
    base_serializers_py = f"/core/new_api/api/{base_serializers}"
    # Obtiene contenido de /core/new_api/api/{base_views}
    try:
        template_views_py = pkgutil.get_data(primary_package, base_views_py).decode('utf-8')
        template_views_py = template_views_py.replace("API_NAME", name.capitalize())
    except:
        message = f"Ocurrió un error interno en /core/new_api/api/{base_views}"
        errors.append([message, True])
    
    # Obtiene contenido de /core/new_api/api/{base_serializers}
    try:
        template_serializers_py = pkgutil.get_data(primary_package, base_serializers_py).decode('utf-8')
        template_serializers_py = template_serializers_py.replace("API_NAME", name.capitalize())
    except:
        message = f"Ocurrió un error interno en /core/new_api/api/{base_serializers}"
        errors.append([message, True])
    
    # Escribe en archivo views.py
    path = f"api/v{version}/{group}/views.py"
    message, result = appendContent(path=path,
        content=template_views_py)
    if result == False:
        errors.append([message, True])

    # Escribe en archivo serializers.py
    path = f"api/v{version}/{group}/serializers.py"
    message, result = appendContent(path=path,
        content=template_serializers_py)
    if result == False:
        errors.append([message, True])

    # Escribe en urls public/private
    views_name = f"{name.capitalize()}{http_verb.capitalize()}"
    path = f"api/v{version}/{general_urls}"
    find = f"# {group.upper()} URLS (Managed by SPRINGLABS_DJANGO)"
    content = f"    url(r'^{url}/$', {group.lower()}_views.{views_name}),"
    message, result = appendContent(path=path,
        content=content,
        find=find)
    if result == False:
        errors.append([message, True])

    for error in errors:
        if error[1] == True:
            return error[0], False

    return "OK", True