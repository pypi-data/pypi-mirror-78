from celery.utils.log import get_task_logger
from django_opstasks.common.sqlalchemy import retry_when_database_error
from django_opstasks.common.sqlalchemy import BaseDatabase

LOGGER = get_task_logger('django')


class TasksDatabase(BaseDatabase):
    """ database class based on BaseDatabase with tasks related operations
    """
    @retry_when_database_error
    def record_start_datetime(self, kwargs):
        """
        record the start datetime of the task
        kwargs = {
            "task_id": task_id, # models.CharField()
            "task_name": task_name, # models.CharField()
            "date_start": start_datetime # models.DateTimeField()
        }
        """
        with self.database_connection():
            LOGGER.info('record task start datetime. %s', kwargs)
            result_model = self._map_table('tasks_results')
            result = self.session.query(result_model).filter(
                result_model.task_id == kwargs['task_id'])
            if result.all():
                kwargs.pop('task_id')
                kwargs.pop('task_name')
                result.update(kwargs)
            else:
                kwargs.setdefault('status', 'PENDING')
                self.session.add(result_model(**kwargs))
            self.session.commit()
        LOGGER.info('record task start time has been completed')


from django_opstasks.models import TaskResult
def record_start_datetime(kwargs):
    TaskResult.objects.update_or_create(**kwargs)
