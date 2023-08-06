from time import sleep
from celery import current_app
from celery.utils.log import get_task_logger
from django_opstasks.database import TasksDatabase

LOGGER = get_task_logger('django')


@current_app.task(bind=True, priority=8, name='opstasks.sync_task_to_database')
def sync_task_to_database(self):
    """将已注册的任务同步到数据库"""
    TasksDatabase().sync_to_database(current_app)


# Execute this task once when starting worker and beat and first importing task from opstasks.tasks
sync_task_to_database.delay()


# 以下为测试任务
@current_app.task(bind=True, priority=1, name='opstasks.test.add')
def add(self, inta, intb):
    """测试带参数任务"""
    return int(inta) + int(intb)


@current_app.task(bind=True, priority=1, name='opstasks.test.error')
def error(self):
    """测试错误任务"""
    raise TypeError(self.__doc__)


@current_app.task(bind=True, priority=1, name='opstasks.test.longtime')
def longtime(self):
    """测试长时间任务"""
    sleep(10)
    return True
