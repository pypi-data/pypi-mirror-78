from logging import getLogger
from django_opstasks.common.datetime import current_datetime
from django_opstasks.common.sqlalchemy import retry_when_database_error
from django_opstasks.common.sqlalchemy import BaseDatabase

LOGGER = getLogger('django')


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

    def _make_task_dict(self, task):
        """
        return a task object, exclude 'celery.*'
        """
        data = {
            "name": task.name,
            "Request": task.Request,
            "Strategy": task.Strategy,
            "abstract": task.abstract,
            "acks_late": task.acks_late,
            "acks_on_failure_or_timeout": task.acks_on_failure_or_timeout,
            "app_main": task.app.main,
            "autoregister": task.autoregister,
            "backend_url": task.backend.url,
            "default_retry_delay": task.default_retry_delay,
            "ignore_result": task.ignore_result,
            "max_retries": task.max_retries,
            "priority": task.priority,
            "rate_limit": task.rate_limit,
            "reject_on_worker_lost": task.reject_on_worker_lost,
            "resultrepr_maxsize": task.resultrepr_maxsize,
            "send_events": task.send_events,
            "serializer": task.serializer,
            "soft_time_limit": task.soft_time_limit,
            "store_errors_even_if_ignored": task.store_errors_even_if_ignored,
            "throws": str(task.throws),
            "time_limit": task.time_limit,
            "track_started": task.track_started,
            "trail": task.trail,
            "typing": task.typing,
            "description": task.__doc__,
            "timestamp": current_datetime(),
            "status": 0
        }
        return data

    @retry_when_database_error
    def sync_to_database(self, app):
        """
        synchronize registered tasks and schedule to the database.
        """
        with self.database_connection():
            tasks_model = self._map_table('tasks_task')
            LOGGER.info(
                'begin syncing registered tasks to the database, '
                'set the status of all tasks to invalid.')
            task_names = [name for name in app.tasks if name.split('.')[0] != 'celery']
            self.session.query(tasks_model).filter().update({"status": 1})
            for name in task_names:
                task = self.session.query(tasks_model).filter(tasks_model.name == name)
                if task.all():
                    LOGGER.info('task "%s" already exists, set the status to normal', name)
                    _data = self._make_task_dict(app.tasks.get(name))
                    task.update(_data)
                else:
                    LOGGER.info('add new task "%s"', name)
                    self.session.add(tasks_model(**self._make_task_dict(app.tasks.get(name))))
            self.session.commit()
        LOGGER.info('synchronize the registered tasks to the database has been completed')
