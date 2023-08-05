# Django libraries
# 3rd Party libraries
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import (
    APIException,
    ValidationError,
    NotFound,
    Throttled,
)
# Standard/core python libraries
# Our custom libraries

header204 = 204, "Ocurrio un error de lógica de negocio"
header409 = 409, "Ocurrio un error inesperado",


def custom_exception_handler(exc, context):
    #exceptionInfo(exc, context)

    errors_list = []
    data = None

    if isinstance(exc, APIException):
        if 'message_dict' in exc.detail:
            exc = APIException(
                detail={exc.detail['code']: exc.detail['message_dict']})
        elif 'message' in exc.detail:
            exc = APIException(
                detail={exc.detail['code']: exc.detail['message']})
        elif 'messages' in exc.detail:
            for msg in exc.detail['messages']:
                exc = APIException(
                    detail={msg['message'].code: msg['message']})

        headerCode = validateAPIExc(exc)
        try:
            detalle = dict(exc.detail)
            for key in detalle.keys():
                if isinstance(exc, ValidationError):
                    objeto = {
                        key: detalle[key][0]
                    }
                else:
                    objeto = {
                        key: detalle[key]
                    }
                errors_list.append(objeto)

        except:
            key = dict(exc.detail.__dict__)
            key = key['code']
            value = str(exc)
            objeto = {
                key: value
            }
            errors_list.append(objeto)

    else:
        headerCode = header409
        key = str(type(exc)).split("'")[1]
        value = str(exc)
        objeto = {
            key: value
        }
        errors_list.append(objeto)

    data = response_maker_1(headerCode[0], errors_list, headerCode[1])
    return Response(data, 200)


def response_maker_1(mensaje, resultado, code, nombre_campo=None):
    if nombre_campo == None:
        resp = {
            "headerResponse": {
                "message": mensaje,
                "code": code
            },
            "payload": resultado
        }
    else:  # Se ejecutó una busqueda (find)
        resp = {
            "headerResponse": {
                "message": mensaje,
                "code": code
            },
            "payload": {
                nombre_campo: resultado
            }
        }
    return resp


def validateAPIExc(exc):
    if isinstance(exc, Throttled) or isinstance(exc, NotFound):
        return header409
    else:
        return header409


def exceptionInfo(exc, context):
    print('>>>>>> Exception: ', exc)
    print('>>>>>> Exception(Type): ', type(exc))
    #print('>>>>>>Context: ', context)
    #print('>>>>>>Standar Response: ', exception_handler(exc, context))
    print('--> ', exc.__dict__)
