from django.http import JsonResponse

from django_opstasks.common.datetime import current_datetime


class OpstasksResponse(JsonResponse):
    """
    return django.http.JsonResponse, setdefault safe=False

      error status code:
      - 400 Bad Request
      - 401 Unauthorized
      - 403 Forbidden
      - 404 Not Found
      - 405 Method Not Allowed

    """
    def __init__(self, context, status_code=200, safe=False, **kwargs):
        super().__init__(data=context, safe=safe, **kwargs)
        self.status_code = status_code


class AsyncResultResponse(OpstasksResponse):
    def __init__(self, async_result):
        data = {
            "timestamp": current_datetime(utc=False),
            "id": async_result.id,
            "name": async_result.name,
            "status": async_result.state,
            "args": async_result.args,
            "kwargs": async_result.kwargs,
            "queue": async_result.queue,
            "worker": async_result.worker,
        }
        super().__init__(data)
