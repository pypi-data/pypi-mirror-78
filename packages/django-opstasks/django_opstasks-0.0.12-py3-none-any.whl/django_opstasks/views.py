from json import loads
from celery.utils.log import get_task_logger
from django_opstasks.common.response import OpstasksResponse
from django_opstasks.common.response import AsyncResultResponse

LOGGER = get_task_logger('django')


# Create your views here.

def error_test(request):
    if request.method == "GET":
        from django_opstasks.tasks import error
        result = error.apply_async()
        if result.get():
            return AsyncResultResponse(result)
    return OpstasksResponse('Method Not Allowed', 405)


def args_test(request):
    if request.method == "POST":
        from django_opstasks.tasks import add
        data = loads(request.body)
        try:
            result = add.apply_async(**data)
            return AsyncResultResponse(result)
        except Exception as error:
            LOGGER.exception(error)
            return OpstasksResponse('Bad Request', 400)
    return OpstasksResponse('Method Not Allowed', 405)


def longtime_test(request):
    if request.method == "GET":
        from django_opstasks.tasks import longtime
        result = longtime.apply_async()
        return AsyncResultResponse(result)
    return OpstasksResponse('Method Not Allowed', 405)


def sync_task_to_database(request):
    if request.method == "GET":
        from django_opstasks.tasks import sync_task_to_database as task
        result = task.apply_async()
        return AsyncResultResponse(result)
    return OpstasksResponse('Method Not Allowed', 405)
