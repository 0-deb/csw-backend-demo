from django.conf import settings
from .models import ErrorLogs


def SerializerErrorMessage(serializerError):
    return [str(serializerError[error][0]) for error in serializerError]


def ExceptionMessage(responseMessage, errorMessage=str()):
    if settings.DEBUG:
        responseMessage = f"{responseMessage}\nError:\n{errorMessage}"

    return responseMessage


def CreateLogs(appName, functionName, error, data=""):
    ErrorLogs.objects.create(
        Application = appName, 
        FunctionName = functionName, 
        Logs = error, 
        RequestData = data
    )