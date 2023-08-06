from __future__ import absolute_import, unicode_literals
from json import loads
from pytz import timezone
from datetime import timedelta
from timezone_field import TimeZoneField
from celery import states
from celery import schedules
from django.db import models
from django.db.models import signals
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import MultipleObjectsReturned, ValidationError
from django_celery_beat.utils import make_aware, now
from django_celery_beat.clockedschedule import clocked
from django_celery_beat.tzcrontab import TzAwareCrontab
from django_celery_beat.validators import (
    minute_validator,
    hour_validator,
    day_of_month_validator,
    month_of_year_validator,
    day_of_week_validator
)
from django_opstasks import managers



# Create your validators here.
def validate_tasks_args(value):
    # 位置参数可读性比关键字参数差
    if value:
        raise ValidationError('请使用关键字参数')

def validate_tasks_kwargs(value):
    try:
        loads(value)
    except:
        raise ValidationError('Json格式错误, 请纠正')

DAYS = 'days'
HOURS = 'hours'
MINUTES = 'minutes'
SECONDS = 'seconds'
MICROSECONDS = 'microseconds'
PERIOD_CHOICES = (
    (DAYS, u'天'),
    (HOURS, u'小时'),
    (MINUTES, u'分钟'),
    (SECONDS, u'秒'),
    (MICROSECONDS, u'毫秒'),
)
SOLAR_SCHEDULES = [(x, x) for x in sorted(schedules.solar._all_events)]
ALL_STATES = sorted(states.ALL_STATES)
TASK_STATE_CHOICES = sorted(zip(ALL_STATES, ALL_STATES))


# Create your models here.
class Task(models.Model):
    name = models.CharField(
        primary_key=True, max_length=50, verbose_name=u'NAME',
        help_text=u'Name of the task.')
    Request = models.CharField(
        max_length=50, verbose_name=u'REQUEST', default=u'celery.worker.request:Request', null=True,
        help_text=u'Request class used, or the qualified name of one.')
    Strategy = models.CharField(
        max_length=50, verbose_name=u'STRATEGY',
        default=u'celery.worker.strategy:default', null=True,
        help_text=u'Execution strategy used, or the qualified name of one.')
    abstract = models.BooleanField(
        verbose_name=u'ABSTRACT', default=True, null=True,
        help_text=u'Deprecated attribute abstract here for compatibility.')
    acks_late = models.BooleanField(
        verbose_name=u'ACKS LATE', default=False, null=True,
        help_text=(
            u'When enabled messages for this task will be acknowledged '
            u'after the task has been executed, and not just before (the default behavior).'))
    acks_on_failure_or_timeout = models.BooleanField(
        verbose_name=u'ACKS FAILURE', default=True, null=True,
        help_text=(
            u'When enabled messages for this task will be acknowledged '
            u'even if it fails or times out.'))
    app_main = models.CharField(
        max_length=20, verbose_name=u'APP NAME', default='opstasks',
        null=True, help_text=u'Celery application.')
    autoregister = models.BooleanField(
        verbose_name=u'AUTO REGISTER', default=True, null=True,
        help_text=u'If disabled this task won’t be registered automatically.')
    backend_url = models.CharField(
        max_length=100, verbose_name=u'BACKEND URL', null=True,
        default='mysql://user:passwd@localhost/opstasks',
        help_text=u'The result store backend class, or the name of the backend class to use.')
    default_retry_delay = models.SmallIntegerField(
        verbose_name=u'DEFAULT RETRY DELAY', default=180, null=True,
        help_text=(
            u'Default time in seconds before a retry of the task should be executed. '
            u'3 minutes by default.'))
    # expires
    # from_config
    ignore_result = models.BooleanField(
        verbose_name=u'IGNORE RESULT', default=False, null=True,
        help_text=u'If enabled the worker won’t store task state and return values for this task.')
    max_retries = models.SmallIntegerField(
        verbose_name=u'MAX RETRIES', default=3, null=True,
        help_text=(
            u'Maximum number of retries before giving up. '
            u'If set to None, it will never stop retrying.'))
    priority = models.SmallIntegerField(
        verbose_name=u'PRIORITY', null=True,
        help_text='The task priority, a number between 0 and 9. .')
    rate_limit = models.CharField(
        max_length=10, verbose_name=u'RATE LIMIT', null=True,
        help_text=(
            u'None (no rate limit), "100/s" (hundred tasks a second),'
            u'"100/m" (hundred tasks a minute), "100/h" (hundred tasks an hour)'))
    reject_on_worker_lost = models.BooleanField(
        verbose_name=u'REJECT ON LOST', null=True,
        help_text=(
            u'Even if acks_late is enabled, the worker will acknowledge tasks '
            u'when the worker process executing them abruptly exits or is signaled '
            u'(e.g., KILL/INT, etc).\n'
            u'Setting this to true allows the message to be re-queued instead, '
            u'so that the task will execute again by the same worker, or another worker.\n'
            u'Warning: Enabling this can cause message loops; '
            u'make sure you know what you’re doing.'))
    # request
    resultrepr_maxsize = models.SmallIntegerField(
        verbose_name=u'RESULTREPR MAXSIZE', default=1024, null=True,
        help_text=u'Max length of result representation used in logs and events.')
    send_events = models.BooleanField(
        verbose_name=u'SEND EVENTS', default=False, null=True,
        help_text=(
            u'If enabled the worker will send monitoring events related to this task\n'
            u'but only if the worker is configured to send task related events'))
    serializer = models.CharField(
        max_length=10, verbose_name=u'SERIALIZER', default='json', null=True,
        help_text=u'The name of a serializer that are registered with kombu.serialization.registry')
    soft_time_limit = models.SmallIntegerField(
        verbose_name=u'SOFT TIME LIMIT', null=True,
        help_text=u'Soft time limit. Defaults to the task_soft_time_limit setting.')
    store_errors_even_if_ignored = models.BooleanField(
        verbose_name=u'STORE ERRORS', default=False, null=True,
        help_text=(
            u'When enabled errors will be stored '
            u'even if the task is otherwise configured to ignore results.'))
    throws = models.CharField(
        max_length=100, verbose_name=u'THROWS', default='()', null=True,
        help_text=u'Tuple of expected exceptions.')
    time_limit = models.SmallIntegerField(
        verbose_name=u'TIME LIMIT', null=True,
        help_text=u'Hard time limit. Defaults to the task_time_limit setting.')
    track_started = models.BooleanField(
        verbose_name=u'TRACK STARTED', default=False, null=True,
        help_text=(
            u'If enabled the task will report its status as ‘started’ '
            u'when the task is executed by a worker.'))
    trail = models.BooleanField(
        verbose_name=u'TRAIL', default=True, null=True,
        help_text=(
            u'If enabled the request will keep track of subtasks started by this task, '
            u'and this information will be sent with the result (result.children).'))
    typing = models.BooleanField(
        verbose_name=u'TYPING', default=True, null=True,
        help_text=(
            u'Enable argument checking. '
            u'You can set this to false if you don’t want the signature to be checked '
            u'when calling the task. Defaults to Celery.strict_typing.'))
    description = models.CharField(
        max_length=255, verbose_name=u'DESCRIPTION', unique=False, null=True)
    timestamp = models.DateTimeField(
        verbose_name=u'TIMESTAMP', auto_now=True,
        help_text=u'Last update time of the task')
    status_choices = ((0, u'NORMAL'), (1, u'INVALID'))
    status = models.IntegerField(
        verbose_name=u'STATUS', null=False, unique=False, default=0, choices=status_choices)

    class Meta:
        verbose_name = u'任务列表'
        verbose_name_plural = verbose_name
        db_table = "tasks_task"

    def __str__(self):
        return self.name


class SolarSchedule(models.Model):
    """Schedule following astronomical patterns.

    Example: to run every sunrise in New York City:
    event='sunrise', latitude=40.7128, longitude=74.0060
    """

    event = models.CharField(
        max_length=24, choices=SOLAR_SCHEDULES,
        verbose_name=u'Solar Event',
        help_text=u'The type of solar event when the job should run')
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name=u'纬度',
        help_text=u'Run the task when the event happens at this latitude',
        validators=[MinValueValidator(-90), MaxValueValidator(90)],)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name=u'经度',
        help_text=u'Run the task when the event happens at this longitude',
        validators=[MinValueValidator(-180), MaxValueValidator(180)],)

    class Meta:
        verbose_name = u'solar'
        verbose_name_plural = u'solars'
        ordering = ('event', 'latitude', 'longitude')
        unique_together = ('event', 'latitude', 'longitude')
        db_table = "tasks_solar_schedule"

    @property
    def schedule(self):
        return schedules.solar(
            self.event, self.latitude, self.longitude, nowfun=lambda: make_aware(now()))

    @classmethod
    def from_schedule(cls, schedule):
        spec = {
            'event': schedule.event,
            'latitude': schedule.lat,
            'longitude': schedule.lon}
        try:
            return cls.objects.get(**spec)
        except cls.DoesNotExist:
            return cls(**spec)
        except MultipleObjectsReturned:
            cls.objects.filter(**spec).delete()
            return cls(**spec)

    def __str__(self):
        return '{0} ({1}, {2})'.format(
            self.get_event_display(),
            self.latitude,
            self.longitude
        )


class IntervalSchedule(models.Model):
    """
    Schedule executing on a regular interval.

    Example: execute every 2 days
    every=2, period=DAYS
    """

    DAYS = DAYS
    HOURS = HOURS
    MINUTES = MINUTES
    SECONDS = SECONDS
    MICROSECONDS = MICROSECONDS

    PERIOD_CHOICES = PERIOD_CHOICES

    every = models.IntegerField(
        null=False, verbose_name=u'间隔时间', validators=[MinValueValidator(1)],
        help_text=u'再次运行任务之前要等待的间隔时间')
    period = models.CharField(
        max_length=24, choices=PERIOD_CHOICES, verbose_name=u'时间单位')

    class Meta:
        verbose_name = u'interval'
        verbose_name_plural = u'intervals'
        ordering = ['period', 'every']
        unique_together = (('period', 'every'),)
        db_table = "tasks_interval_schedule"

    @property
    def schedule(self):
        return schedules.schedule(
            timedelta(**{self.period: self.every}),
            nowfun=lambda: make_aware(now()))

    @classmethod
    def from_schedule(cls, schedule, period=SECONDS):
        every = max(schedule.run_every.total_seconds(), 0)
        try:
            return cls.objects.get(every=every, period=period)
        except cls.DoesNotExist:
            return cls(every=every, period=period)
        except MultipleObjectsReturned:
            cls.objects.filter(every=every, period=period).delete()
            return cls(every=every, period=period)

    def __str__(self):
        readable_period = None
        if self.every == 1:
            for period, _readable_period in PERIOD_CHOICES:
                if period == self.period:
                    readable_period = _readable_period.lower()
                    break
            return u'每 {} 执行一次'.format(readable_period)
        for period, _readable_period in PERIOD_CHOICES:
            if period == self.period:
                readable_period = _readable_period.lower()
                break
        return u'每 {} {} 执行一次'.format(self.every, readable_period)

    @property
    def period_singular(self):
        return self.period[:-1]


class ClockedSchedule(models.Model):
    """
    clocked schedule.
    """

    clocked_time = models.DateTimeField(
        verbose_name=u'Clock Time', help_text=u'在指定时间运行任务.')
    enabled = models.BooleanField(
        default=True, editable=False, verbose_name='ENABLED',
        help_text=u'设置为False后不进行任务调度.')

    class Meta:
        verbose_name = u'clocked'
        verbose_name_plural = u'clocked'
        ordering = ['clocked_time']
        db_table = "tasks_clocked_schedule"

    def __str__(self):
        _local_tz = timezone(settings.TIME_ZONE)
        return f'{self.clocked_time.astimezone(_local_tz)}'

    @property
    def schedule(self):
        _clocked = clocked(
            clocked_time=self.clocked_time, enabled=self.enabled, model=self)
        return _clocked

    @classmethod
    def from_schedule(cls, schedule):
        spec = {
            'clocked_time': schedule.clocked_time,
            'enabled': schedule.enabled,}
        try:
            return cls.objects.get(**spec)
        except cls.DoesNotExist:
            return cls(**spec)
        except MultipleObjectsReturned:
            cls.objects.filter(**spec).delete()
            return cls(**spec)


class CrontabSchedule(models.Model):
    """
    Timezone Aware Crontab-like schedule.

    Example:  Run every hour at 0 minutes for days of month 10-15
    minute="0", hour="*", day_of_week="*",
    day_of_month="10-15", month_of_year="*"
    """

    # The worst case scenario for day of month is a list of all 31 day numbers
    # '[1, 2, ..., 31]' which has a length of 115. Likewise, minute can be
    # 0..59 and hour can be 0..23. Ensure we can accomodate these by allowing
    # 4 chars for each value (what we save on 0-9 accomodates the []).
    # We leave the other fields at their historical length.

    minute = models.CharField(
        max_length=60 * 4, default='*', verbose_name=u'Minutes',
        validators=[minute_validator],)
    hour = models.CharField(
        max_length=24 * 4, default='*', verbose_name=u'Hours',
        validators=[hour_validator],)
    day_of_week = models.CharField(
        max_length=64, default='*', verbose_name=u'Days Of The Week',
        validators=[day_of_week_validator],)
    day_of_month = models.CharField(
        max_length=31 * 4, default='*', verbose_name=u'Days Of The Month',
        validators=[day_of_month_validator],)
    month_of_year = models.CharField(
        max_length=64, default='*', verbose_name=u'Months Of The Year',
        validators=[month_of_year_validator],)
    timezone = TimeZoneField(
        default='UTC', verbose_name='Timezone')

    class Meta:
        verbose_name = u'crontab'
        verbose_name_plural = u'crontabs'
        ordering = [
            'month_of_year', 'day_of_month', 'day_of_week', 'hour', 'minute', 'timezone']
        db_table = "tasks_crontab_schedule"

    def __str__(self):
        _data = {
            "m": self.cronexp(self.minute),
            "h": self.cronexp(self.hour),
            "dm": self.cronexp(self.day_of_month),
            "my": self.cronexp(self.month_of_year),
            "dw": self.cronexp(self.day_of_week)
        }
        return 'Crontab({m} {h} {dm} {my} {dw})'.format(**_data)

    def cronexp(self, field):
        """
        Representation of cron expression.
        """
        return field and str(field).replace(' ', '') or '*'

    @property
    def schedule(self):
        crontab = schedules.crontab(
            minute=self.minute,
            hour=self.hour,
            day_of_week=self.day_of_week,
            day_of_month=self.day_of_month,
            month_of_year=self.month_of_year,
        )
        if getattr(settings, 'DJANGO_CELERY_BEAT_TZ_AWARE', True):
            crontab = TzAwareCrontab(
                minute=self.minute,
                hour=self.hour,
                day_of_week=self.day_of_week,
                day_of_month=self.day_of_month,
                month_of_year=self.month_of_year,
                tz=self.timezone
            )
        return crontab

    @classmethod
    def from_schedule(cls, schedule):
        spec = {
            'minute': schedule._orig_minute,
            'hour': schedule._orig_hour,
            'day_of_week': schedule._orig_day_of_week,
            'day_of_month': schedule._orig_day_of_month,
            'month_of_year': schedule._orig_month_of_year,
            'timezone': schedule.tz}
        try:
            return cls.objects.get(**spec)
        except cls.DoesNotExist:
            return cls(**spec)
        except MultipleObjectsReturned:
            cls.objects.filter(**spec).delete()
            return cls(**spec)


class PeriodicTasks(models.Model):
    """
    Helper table for tracking updates to periodic tasks.

    This stores a single row with ident=1.  last_update is updated
    via django signals whenever anything is changed in the PeriodicTask model.
    Basically this acts like a DB data audit trigger.
    Doing this so we also track deletions, and not just insert/update.
    """

    ident = models.SmallIntegerField(default=1, primary_key=True, unique=True)
    last_update = models.DateTimeField(null=False)

    objects = managers.ExtendedManager()

    class Meta:
        db_table = "tasks_periodic_tasks"

    @classmethod
    def changed(cls, instance, **kwargs):
        if not instance.no_changes:
            cls.update_changed()
        del kwargs

    @classmethod
    def update_changed(cls, **kwargs):
        cls.objects.update_or_create(ident=1, defaults={'last_update': now()})
        del kwargs

    @classmethod
    def last_change(cls):
        try:
            return cls.objects.get(ident=1).last_update
        except cls.DoesNotExist:
            pass


class PeriodicTask(models.Model):
    """
    Model representing a periodic task.
    """
    name = models.CharField(max_length=200, unique=True, verbose_name=u'SHORT DESCRIPTION NAME')
    task = models.CharField(max_length=200, verbose_name=u'TASK')
    registered_task = models.ForeignKey(
        Task, on_delete=models.DO_NOTHING, to_field='name', verbose_name=u'已注册任务',
        null=True, blank=True, related_name='TASK')
    interval = models.ForeignKey(
        IntervalSchedule, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=u'Interval计划', help_text=u'注:仅能设置一种调度方式,请将其余计划留空.')
    crontab = models.ForeignKey(
        CrontabSchedule, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=u'Crontab计划', help_text=u'注:仅能设置一种调度方式,请将其余计划留空.')
    solar = models.ForeignKey(
        SolarSchedule, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=u'Solar计划', help_text=u'注:仅能设置一种调度方式,请将其余计划留空.')
    clocked = models.ForeignKey(
        ClockedSchedule, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=u'Clocked计划', help_text=u'注:仅能设置一种调度方式,请将其余计划留空.')
    args = models.TextField(
        blank=True, verbose_name=u'位置参数', validators=[validate_tasks_args],
        help_text=u'传递给任务的位置参数, Json格式')
    kwargs = models.TextField(
        blank=True, verbose_name=u'任务参数', validators=[validate_tasks_kwargs],
        help_text=u'传递给任务的关键字参数, Json格式')
    queue = models.CharField(
        max_length=200, blank=True, null=True, default=None, verbose_name=u'队列',
        help_text=u'选择CELERY_TASK_QUEUES中定义的队列, 留空将使用默认队列.')
    # you can use low-level AMQP routing options here,
    # but you almost certaily want to leave these as None
    # http://docs.celeryproject.org/en/latest/userguide/routing.html#exchanges-queues-and-routing-keys
    exchange = models.CharField(
        max_length=200, blank=True, null=True, default=None,
        verbose_name=u'Exchange', help_text=u'Override Exchange for low-level AMQP routing')
    routing_key = models.CharField(
        max_length=200, blank=True, null=True, default=None, verbose_name=u'Routing Key',
        help_text=u'Override Routing Key for low-level AMQP routing')
    headers = models.TextField(
        blank=True, default='{}', verbose_name=u'AMQP Message Headers',
        help_text=u'JSON encoded message headers for the AMQP message.')
    priority = models.PositiveIntegerField(
        default=None, validators=[MaxValueValidator(255)], blank=True, null=True,
        verbose_name=u'优先级',
        help_text=u'优先级数字介于0-255之间. 仅支持: RabbitMQ, Redis . 优先级相反, 0最高.')
    start_time = models.DateTimeField(
        blank=True, null=True, verbose_name=u'开始时间', help_text=u'计划的生效时间')
    expires = models.DateTimeField(
        blank=True, null=True, verbose_name='过期时间',
        help_text=u'超过该时间之后, 本计划将不再启动任务')
    expire_seconds = models.PositiveIntegerField(
        blank=True, null=True, verbose_name=u'Expires timedelta with seconds',
        help_text=(
            u'Timedelta with seconds which the schedule will no longer '
            u'trigger the task to run'))
    enabled = models.BooleanField(
        default=True, verbose_name=u'ENABLED', help_text=u'取消勾选将关闭计划任务')
    one_off = models.BooleanField(
        default=False, verbose_name=u'ONE_OFF', help_text=u'勾选后该计划仅执行一次')
    last_run_at = models.DateTimeField(
        auto_now=False, auto_now_add=False, editable=False, blank=True, null=True,
        verbose_name=u'Last Run Datetime')
    total_run_count = models.PositiveIntegerField(
        default=0, editable=False, verbose_name=u'Total Run Count',
        help_text=(
            u'Running count of how many times the schedule '
            u'has triggered the task'))
    date_changed = models.DateTimeField(
        auto_now=True, verbose_name=u'Last Modified',
        help_text=u'Datetime that this PeriodicTask was last modified')
    description = models.TextField(
        blank=True, verbose_name=u'DESCRIPTION',
        default=u'Detailed description about the details of this Periodic Task')
    objects = managers.PeriodicTaskManager()
    no_changes = False

    class Meta:
        verbose_name = u'定时任务'
        verbose_name_plural = verbose_name
        db_table = "tasks_periodic_task"

    def validate_unique(self, exclude=None):
        """
        Check unique constraints on the model and raise ValidationError if any failed.
        """
        super(PeriodicTask, self).validate_unique(exclude=exclude)
        schedule_types = ['interval', 'crontab', 'solar', 'clocked']
        selected_schedule_types = [
            s for s in schedule_types if getattr(self, s)]
        if len(selected_schedule_types) == 0:
            raise ValidationError({
                'interval': ['One of clocked, interval, crontab, or solar must be set.']})
        err_msg = 'Only one of clocked, interval, crontab, or solar must be set'
        if len(selected_schedule_types) > 1:
            error_info = {}
            for selected_schedule_type in selected_schedule_types:
                error_info[selected_schedule_type] = [err_msg]
            raise ValidationError(error_info)

        # clocked must be one off task
        if self.clocked and not self.one_off:
            err_msg = 'clocked must be one off, one_off must set True'
            raise ValidationError(err_msg)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """
        Save the current instance. Override this in a subclass if you want to
        control the saving process.

        The 'force_insert' and 'force_update' parameters can be used to insist
        that the "save" must be an SQL insert or update (or equivalent for
        non-SQL backends), respectively. Normally, they should not be set.
        """
        self.exchange = self.exchange or None
        self.routing_key = self.routing_key or None
        self.queue = self.queue or None
        self.headers = self.headers or None
        if not self.enabled:
            self.last_run_at = None
        self._clean_expires()
        self.validate_unique()
        super(PeriodicTask, self).save(
            force_insert=force_insert, force_update=force_update,
            using=using, update_fields=update_fields)

    def _clean_expires(self):
        if self.expire_seconds is not None and self.expires:
            raise ValidationError('Only one can be set, in expires and expire_seconds')

    @property
    def expires_(self):
        return self.expires or self.expire_seconds

    def __str__(self):
        fmt = '{0.name}: {{no schedule}}'
        if self.interval:
            fmt = '{0.name}: {0.interval}'
        if self.crontab:
            fmt = '{0.name}: {0.crontab}'
        if self.solar:
            fmt = '{0.name}: {0.solar}'
        if self.clocked:
            fmt = '{0.name}: {0.clocked}'
        return fmt.format(self)

    @property
    def schedule(self):
        if self.interval:
            return self.interval.schedule
        if self.crontab:
            return self.crontab.schedule
        if self.solar:
            return self.solar.schedule
        if self.clocked:
            return self.clocked.schedule


class TaskResult(models.Model):
    """
    Task result/status.
    """
    task_id = models.CharField(
        max_length=getattr(settings, 'DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH', 255),
        unique=True, db_index=True, verbose_name=u'Task ID')
    task_name = models.CharField(
        null=True, max_length=255, db_index=True, verbose_name=u'Task Name')
    task_args = models.TextField(
        null=True, verbose_name=u'Task Positional Arguments')
    task_kwargs = models.TextField(
        null=True, verbose_name=u'Task Named Arguments')
    status = models.CharField(
        max_length=50, default=states.PENDING, db_index=True,
        choices=TASK_STATE_CHOICES, verbose_name=u'Task State')
    worker = models.CharField(
        max_length=100, db_index=True, default=None, null=True, verbose_name=u'Worker')
    content_type = models.CharField(
        blank=True, null=True, max_length=128, verbose_name=u'Result Content Type')
    content_encoding = models.CharField(
        blank=True, null=True, max_length=64, verbose_name=u'Result Encoding')
    result = models.TextField(
        blank=True, null=True, default=None, editable=False, verbose_name=u'Result Data')
    date_start = models.DateTimeField(
        auto_now_add=True, blank=True, null=True, verbose_name=u'Started DateTime')
    date_created = models.DateTimeField(
        auto_now_add=True, blank=True, null=True, db_index=True,
        verbose_name=u'Created DateTime')
    date_done = models.DateTimeField(
        auto_now=True, blank=True, null=True, db_index=True,
        verbose_name=u'Completed DateTime')
    traceback = models.TextField(
        blank=True, null=True, verbose_name=u'Traceback')
    meta = models.TextField(
        null=True, default=None, editable=False, verbose_name=u'Task Meta Information')
    queue = models.CharField(max_length=155, blank=True, null=True, verbose_name=u'Queue')

    objects = managers.TaskResultManager()

    class Meta:
        verbose_name = u'执行记录'
        verbose_name_plural = verbose_name
        db_table = "tasks_results"


    def as_dict(self):
        return {
            'task_id': self.task_id,
            'task_name': self.task_name,
            'task_args': self.task_args,
            'task_kwargs': self.task_kwargs,
            'status': self.status,
            'result': self.result,
            'date_done': self.date_done,
            'traceback': self.traceback,
            'meta': self.meta,
            'worker': self.worker
        }

    def __str__(self):
        return '<Task: {0.task_id} ({0.status})>'.format(self)


signals.pre_delete.connect(PeriodicTasks.changed, sender=PeriodicTask)
signals.pre_save.connect(PeriodicTasks.changed, sender=PeriodicTask)
signals.pre_delete.connect(
    PeriodicTasks.update_changed, sender=IntervalSchedule)
signals.post_save.connect(
    PeriodicTasks.update_changed, sender=IntervalSchedule)
signals.post_delete.connect(
    PeriodicTasks.update_changed, sender=CrontabSchedule)
signals.post_save.connect(
    PeriodicTasks.update_changed, sender=CrontabSchedule)
signals.post_delete.connect(
    PeriodicTasks.update_changed, sender=SolarSchedule)
signals.post_save.connect(
    PeriodicTasks.update_changed, sender=SolarSchedule)
signals.post_delete.connect(
    PeriodicTasks.update_changed, sender=ClockedSchedule)
signals.post_save.connect(
    PeriodicTasks.update_changed, sender=ClockedSchedule)
