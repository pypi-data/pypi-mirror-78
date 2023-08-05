import datetime
import bizerror

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


from fastutils import sysutils
from fastutils import randomutils

from django_db_lock.client import DjangoDbLock

from . import settings
from .services import SimpleTaskServices


_("Simple Task Information")

class SimpleTask(models.Model):

    READY = 10
    DOING = 20
    DONE = 30
    FAILED = 40
    SET_TO_READY_ON_FIRST_SAVE = True

    GET_READY_TASKS_LOCK_NAME_TEMPLATE = "SimpleTask:{app_label}:{model_name}:getReadyTasks:Lock"
    GET_READY_TASKS_LOCK_TIMEOUT = 60

    RESET_DEAD_TASKS_LOCK_NAME_TEMPLATE = "SimpleTask:{app_label}:{model_name}:resetDeadTasks:Lock"
    RESET_DEAD_TASKS_LOCK_TIMEOUT = 60
    TASK_DOING_TIMEOUT = 60*5

    STATUS_CHOICES = [
        (READY, _("Task Ready")),
        (DOING, _("Task Doing")),
        (DONE, _("Task Done")),
        (FAILED, _("Task Failed")),
    ]

    add_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Add Time"))
    mod_time = models.DateTimeField(auto_now=True, verbose_name=_("Modify Time"))

    status = models.IntegerField(choices=STATUS_CHOICES, null=True, blank=True, verbose_name=_("Status"))
    worker = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Worker Name"))
    start_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Start Time"))
    done_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Done Time"))
    error_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Error Time"))
    result = models.TextField(null=True, blank=True, verbose_name=_("Result"))
    error_code = models.IntegerField(null=True, blank=True, verbose_name=_("Error Code"))
    error_message = models.TextField(null=True, blank=True, verbose_name=_("Error Message"))

    class Meta:
        abstract = True

    SIMPLE_TASK_FIELDS = [
        "status",
        "worker",
        "start_time",
        "done_time",
        "error_time",
        "result",
        "error_code",
        "error_message",
        "add_time",
        "mod_time",
    ]

    def save(self, *args, **kwargs):
        if (not self.pk) and (self.status is None):
            self.reset()
        super().save(*args, **kwargs)

    def do_task(self, worker):
        self.start(worker, save=True)
        try:
            result = self.do_task_main()
            self.report_success(worker, result, save=True)
            return True
        except Exception as error:
            error = bizerror.BizError(error)
            self.report_error(worker, error.code, error.message, save=True)
            return False

    def do_task_main(self):
        raise NotImplementedError()

    def reset(self, save=False):
        self.status = self.READY
        self.worker = None
        self.start_time = None
        self.done_time = None
        self.error_time = None
        self.result = None
        self.error_code = None
        self.error_message = None
        if save:
            self.save()

    def start(self, worker, save=False):
        if self.status != self.READY:
            return False
        self.status = self.DOING
        self.worker = worker
        self.start_time = timezone.now()
        if save:
            self.save()
        return True

    def report_success(self, worker, result, save=False):
        if self.worker != worker:
            return False
        if self.status != self.DOING:
            return False
        self.status = self.DONE
        self.result = result
        self.done_time = timezone.now()
        if save:
            self.save()
        return True

    def report_error(self, worker, error_code, error_message, save=False):
        if self.worker != worker:
            return False
        if self.status != self.DOING:
            return False
        self.status = self.FAILED
        self.error_code = error_code
        self.error_message = error_message
        self.error_time = timezone.now()
        if save:
            self.save()
        return True

    @classmethod
    def get_ready_tasks(cls, worker, n=1):
        app_label = cls._meta.app_label
        model_name = cls._meta.model_name
        lock_name = cls.GET_READY_TASKS_LOCK_NAME_TEMPLATE.format(app_label=app_label, model_name=model_name)
        timeout = cls.GET_READY_TASKS_LOCK_TIMEOUT
        with DjangoDbLock(lock_name, str(randomutils.uuid4()), timeout) as locked:
            if not locked:
                return []
            tasks = cls.objects.filter(status=cls.READY).order_by("mod_time")[:n]
            for task in tasks:
                task.start(worker, save=True)
            return tasks

    @classmethod
    def reset_dead_tasks(cls):
        app_label = cls._meta.app_label
        model_name = cls._meta.model_name
        lock_name = cls.RESET_DEAD_TASKS_LOCK_NAME_TEMPLATE.format(app_label=app_label, model_name=model_name)
        timeout = cls.RESET_DEAD_TASKS_LOCK_TIMEOUT
        with DjangoDbLock(lock_name, str(randomutils.uuid4()), timeout) as locked:
            if not locked:
                return []
            dead_time_limit = timezone.now() - datetime.timedelta(seconds=cls.TASK_DOING_TIMEOUT)
            tasks = cls.objects.filter(status=cls.DOING).filter(start_time__lte=dead_time_limit)
            for task in tasks:
                task.reset(save=True)
            return tasks

    @classmethod
    def get_services(cls):
        return SimpleTaskServices(cls)


    @classmethod
    def do_tasks(cls, worker, n: int=100):
        done = 0
        failed = 0
        stime = datetime.datetime.now()
        for task in cls.get_ready_tasks(worker, n):
            if task.do_task(worker):
                done += 1
            else:
                failed += 1
        total = done + failed
        etime= datetime.datetime.now()
        time_delta = etime - stime
        return {
            "total": done + failed,
            "done": done,
            "failed": failed,
            "stime": stime,
            "etime": etime,
            "totalTime": time_delta.total_seconds(),
            "taskTime":  total and time_delta.total_seconds()/total or None,
        }
