from logging import getLogger
from django.contrib import admin, messages
from django.utils.html import format_html
from django.conf import settings
from django.template.defaultfilters import pluralize
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django_celery_beat.utils import is_database_scheduler
from .models import Task, TaskResult
from .models import (
    SolarSchedule, IntervalSchedule, CrontabSchedule,
    ClockedSchedule, PeriodicTask, PeriodicTasks
)

LOGGER = getLogger('django')

DISPLAY_NAME_FORMAT = '<div title="{}">{}</div>'
DISPLAY_STATUS_FORMAT = '<span title="{}" \
    class="el-tag el-tag--mini el-tag--light el-tag--{}">{}</span>'

# Register your models here.
class TaskResource(resources.ModelResource):
    class Meta:
        model = Task
        skip_unchanged = True
        report_skipped = True
@admin.register(Task)
class TaskAdmin(ImportExportModelAdmin):
    model = Task
    resource_class = TaskResource
    list_per_page = 20
    list_display = (
        'dis_name_description', 'description', 'dis_average_duration', 'dis_success_ratio',
        'dis_status')
    search_fields = ('name', 'description', 'status')
    list_filter = ('name', 'max_retries', 'priority', 'status')
    empty_value_display = '---'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def dis_average_duration(self, obj):
        duration_list = []
        for result in TaskResult.objects.filter(task_name=obj.name):
            try:
                duration = result.date_done - result.date_start
                duration_list.append(duration.seconds)
            except Exception:
                pass
        if duration_list:
            min_duration, max_duration = min(duration_list), max(duration_list)
            sum_duration = 0
            for duration in duration_list:
                sum_duration += duration
            avg_duration = round(sum_duration/len(duration_list), 2)
        else:
            min_duration, avg_duration, max_duration = 0, 0, 0
        return '%s / %s / %s' % (min_duration, avg_duration, max_duration)
    dis_average_duration.short_description = u'DURATION(MIN/AVG/MAX)'
    dis_average_duration.admin_order_field = 'id'

    def dis_success_ratio(self, obj):
        status_list = [result.status for result in TaskResult.objects.filter(task_name=obj.name)]
        successed = status_list.count('SUCCESS')
        return '%s / %s' % (successed, len(status_list))
    dis_success_ratio.short_description = u'SUCCESS/TOTAL'
    dis_success_ratio.admin_order_field = 'id'

    def dis_name_description(self, obj):
        return format_html(DISPLAY_NAME_FORMAT.format(obj.description, obj.name))
    dis_name_description.short_description = u'NAME'
    dis_name_description.admin_order_field = 'name'

    def dis_status(self, obj):
        timestamp = obj.timestamp.strftime('%Y-%m-%d %H:%M:%S') if obj.timestamp else obj.status
        if obj.status:
            return format_html(DISPLAY_STATUS_FORMAT.format(timestamp, 'danger', 'INVALID'))
        return format_html(DISPLAY_STATUS_FORMAT.format(timestamp, 'success', 'NORMAL'))
    dis_status.short_description = ' '
    dis_status.admin_order_field = 'status'


@admin.register(SolarSchedule)
class SolarScheduleAdmin(admin.ModelAdmin):

    def has_module_permission(self, request):
        return False

    class Meta:
        model = SolarSchedule


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(admin.ModelAdmin):
    fields = ('every', 'period',)

    def has_module_permission(self, request):
        return False

    class Meta:
        model = IntervalSchedule


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(admin.ModelAdmin):

    def has_module_permission(self, request):
        return False

    class Meta:
        model = CrontabSchedule


@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(admin.ModelAdmin):
    """
    Admin-interface for clocked schedules.
    """
    fields = ('clocked_time', 'enabled',)
    readonly_fields = ('enabled',)
    list_display = ('clocked_time', 'enabled',)

    def has_module_permission(self, request):
        return False

    class Meta:
        model = ClockedSchedule


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(admin.ModelAdmin):
    """
    Admin interface for periodic tasks.
    """
    model = PeriodicTask
    list_display = (
        'dis_name_description', 'task', 'dis_scheduler', 'dis_kwargs',
        'total_run_count', 'last_run_at', 'dis_enabled')
    search_fields = ('name',)
    list_filter = ['task', 'enabled', 'one_off']
    fieldsets = (
        (u'基础配置', {
            'fields': ('name', 'registered_task', 'enabled', 'one_off', 'description',),
            'classes': ('extrapretty',),}),
        (u'调度策略', {
            'fields': ('interval', 'crontab', 'solar', 'clocked',),
            'classes': ('extrapretty',),
            'description': '请在下列四种调度计划中选择其中一种.'}),
        (u'生效时间', {
            'fields': ('start_time', 'expires'),
            'classes': ('extrapretty',)}),
        (u'任务选项', {
            'fields': ('kwargs', 'queue', 'priority'),
            'classes': ('extrapretty', 'collapse', 'in'),}),)
    readonly_fields = ('last_run_at',)
    date_hierarchy = 'start_time'
    empty_value_display = '---'
    actions = ('enable_tasks', 'disable_tasks')

    def save_model(self, request, obj, form, change):
        if obj.registered_task.status == 0:
            obj.task = obj.registered_task.name
        if obj.task:
            super().save_model(request, obj, form, change)
        else:
            messages.set_level(request, messages.WARNING)
            messages.error(request, u'当前选择的任务无效, 请确认后重新选择')

    def dis_name_description(self, obj):
        return format_html(DISPLAY_NAME_FORMAT.format(obj.description, obj.name))
    dis_name_description.short_description = u'NAME'
    dis_name_description.admin_order_field = 'name'

    def dis_scheduler(self, obj):
        if obj.interval:
            return obj.interval
        if obj.crontab:
            return obj.crontab
        if obj.clocked:
            return obj.clocked
        if obj.solar:
            return obj.solar
        return 'no schedule'
    dis_scheduler.admin_order_field = 'name'
    dis_scheduler.short_description = u'SCHEDULER'

    def dis_kwargs(self, obj):
        if obj.kwargs and obj.kwargs != '{}':
            return obj.kwargs
        return '---'
    dis_kwargs.admin_order_field = 'kwargs'
    dis_kwargs.short_description = u'KWARGS'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        scheduler = getattr(settings, 'CELERY_BEAT_SCHEDULER', None)
        extra_context['wrong_scheduler'] = not is_database_scheduler(scheduler)
        return super(PeriodicTaskAdmin, self).changelist_view(
            request, extra_context)

    def get_queryset(self, request):
        qs = super(PeriodicTaskAdmin, self).get_queryset(request)
        return qs.select_related('interval', 'crontab', 'solar', 'clocked')

    def _message_user_about_update(self, request, rows_updated, verb):
        """ Send message about action to user.
        `verb` should shortly describe what have changed (e.g. 'enabled').
        """
        self.message_user(request, (
            f'{rows_updated} task{pluralize(rows_updated)} '
            f'{pluralize(rows_updated, "was,were")} successfully {verb}'))

    def dis_enabled(self, obj):
        if obj.enabled:
            return format_html(DISPLAY_STATUS_FORMAT.format(
                'ENABLED', 'success', 'ENABLED'))
        return format_html(DISPLAY_STATUS_FORMAT.format(
            'DISABLED', 'danger', 'DISABLED'))
    dis_enabled.short_description = u' '
    dis_enabled.admin_order_field = 'enabled'

    def enable_tasks(self, request, queryset):
        rows_updated = queryset.update(enabled=True)
        PeriodicTasks.update_changed()
        self._message_user_about_update(request, rows_updated, 'enabled')
    enable_tasks.short_description = u'开启'
    enable_tasks.type = 'success'
    enable_tasks.icon = 'el-icon-video-play'

    def disable_tasks(self, request, queryset):
        rows_updated = queryset.update(enabled=False)
        PeriodicTasks.update_changed()
        self._message_user_about_update(request, rows_updated, 'disabled')
    disable_tasks.short_description = u'关闭'
    disable_tasks.type = 'warning'
    disable_tasks.icon = 'el-icon-video-pause'
    disable_tasks.confirm = u'确定要停止任务调度吗?'

    class Meta:
        model = PeriodicTask


class TaskResultResource(resources.ModelResource):
    class Meta:
        model = TaskResult
        skip_unchanged = True
        report_skipped = True
@admin.register(TaskResult)
class TaskResultAdmin(ImportExportModelAdmin):
    fields = (
        'task_id', 'task_name', 'queue', 'worker', 'status',
        'date_start', 'date_created', 'date_done',
        'task_args', 'task_kwargs', 'traceback', 'result', 'meta')
    list_display = (
        'id', 'task_id', 'task_name', 'dis_kwargs', 'date_start',
        'queue', 'dis_duration', 'dis_colored_status')
    list_filter = ('task_name', 'worker', 'status', 'date_done')
    resource_class = TaskResultResource
    actions_selection_counter = True
    empty_value_display = '---'
    list_per_page = 100
    date_hierarchy = 'date_done'

    class Meta:
        model = TaskResult

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def history_view(self, request, object_id, extra_context=None):
        return False

    def dis_kwargs(self, obj):
        return obj.task_kwargs
    dis_kwargs.short_description = u'KWARGS'
    dis_kwargs.admin_order_field = 'kwargs'

    def dis_duration(self, obj):
        """calculate and display task execution time"""
        try:
            duration = obj.date_done - obj.date_start
            return duration.seconds
        except Exception as error:
            LOGGER.exception(error)
            return '---'
    dis_duration.short_description = u'DURATION'
    dis_duration.admin_order_field = 'date_done'

    def dis_colored_status(self, obj):
        """display: colored status of task record"""
        status_color = {
            'PENDING': 'info',
            'RECEIVED': 'warning',
            'REJECTED': 'warning',
            'IGNORED': 'warning',
            'REVOKED': 'warning',
            'STARTED': 'primary',
            'RETRY': 'warning',
            'SUCCESS': 'success',
            'FAILURE': 'danger',
            }
        date_done = obj.date_done.strftime('%Y-%m-%d %H:%M:%S') if obj.date_done else obj.status
        try:
            return format_html(DISPLAY_STATUS_FORMAT.format(
                date_done, status_color[obj.status], obj.status))
        except Exception as error:
            LOGGER.exception(error)
            return '---'
    dis_colored_status.short_description = u'STATUS'
    dis_colored_status.admin_order_field = 'status'
