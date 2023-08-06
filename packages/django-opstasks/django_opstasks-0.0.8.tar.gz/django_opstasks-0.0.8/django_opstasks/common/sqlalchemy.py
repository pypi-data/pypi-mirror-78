from contextlib import contextmanager
from vine.utils import wraps
from django.conf import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import DatabaseError, InvalidRequestError
from sqlalchemy.orm.exc import StaleDataError
from celery.utils.log import get_task_logger

LOGGER = get_task_logger('django')


def retry_when_database_error(fun):
    """
    decorator:
        retry three times when the database operation fails.
        default max_retries = 3
    """
    @wraps(fun)
    def _inner(*args, **kwargs):
        max_retries = kwargs.pop('max_retries', 3)
        for retries in range(max_retries):
            try:
                return fun(*args, **kwargs)
            except (DatabaseError, InvalidRequestError, StaleDataError):
                LOGGER.warning(
                    'failed operation %s.  retrying %s more times.',
                    fun.__name__, max_retries - retries - 1,
                    exc_info=True)
                if retries + 1 >= max_retries:
                    raise
    return _inner


class BaseDatabase(object):
    """ basic database class with context manager
    """
    def __init__(self, dburi=None):
        self.dburi = dburi if dburi else settings.DB_URI
        self.engine = None
        self.session = None

    def _create_session(self):
        try:
            self.engine = create_engine(self.dburi, echo=False, encoding='utf-8')
            self.session = sessionmaker(bind=self.engine)()
            return self.engine, self.session
        except Exception as error:
            LOGGER.error('can not create database session. {"error": %s}', error)

    def _map_table(self, table):
        '''mapping model and data table, return a model'''
        try:
            base = automap_base()
            base.prepare(self.engine, reflect=True)
            return base.classes[table]
        except Exception as error:
            LOGGER.error('failed to map model and data table. {"error": %s}', error)
            raise

    @contextmanager
    def database_connection(self):
        """ a context manager
        """
        try:
            self.engine, self.session = self._create_session()
            yield
        except Exception as error:
            self.session.rollback()
            LOGGER.error('database operation failed, has been rolled back. {"error": %s}', error)
            raise
        finally:
            self.session.close()
