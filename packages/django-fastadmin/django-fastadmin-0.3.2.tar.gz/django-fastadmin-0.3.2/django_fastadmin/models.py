import datetime
import bizerror

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


from fastutils import sysutils
from fastutils import randomutils

from django_db_lock.client import DjangoDbLock

from . import settings


_("Simple Task Information")

class SimpleTask(models.Model):
    """
    """
    NEW = 0
    READY = 10
    DOING = 20
    DONE = 30
    FAILED = 40

    GET_READY_TASKS_LOCK_NAME_TEMPLATE = "SimpleTask:{app_label}:{model_name}:getReadyTasks:Lock"
    GET_READY_TASKS_LOCK_TIMEOUT = 60

    RESET_DEAD_TASKS_LOCK_NAME_TEMPLATE = "SimpleTask:{app_label}:{model_name}:resetDeadTasks:Lock"
    RESET_DEAD_TASKS_LOCK_TIMEOUT = 60
    TASK_DOING_TIMEOUT = 60*5

    STATUS_CHOICES = [
        (NEW, _("Task New")),
        (READY, _("Task Ready")),
        (DOING, _("Task Doing")),
        (DONE, _("Task Done")),
        (FAILED, _("Task Failed")),
    ]


    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW, null=True, blank=True, verbose_name=_("Status"), help_text=_("Task has New, Ready, Doing, Done and Failed status."))
    active = models.NullBooleanField(verbose_name=_("Active"), help_text=_("The task is to be runned or is running..."))
    worker = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Worker ID"))

    success = models.NullBooleanField(verbose_name=_("Success"), help_text=_("Task success or not."))
    result = models.TextField(null=True, blank=True, verbose_name=_("Result"))
    error_code = models.IntegerField(null=True, blank=True, verbose_name=_("Error Code"))
    error_message = models.TextField(null=True, blank=True, verbose_name=_("Error Message"))

    add_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Add Time"), help_text=_("Task add time is the time when the task created."))
    mod_time = models.DateTimeField(auto_now=True, verbose_name=_("Modify Time"), help_text=_("Task modify time is the time when the task modified."))
    ready_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Ready Time"), help_text=_("Task ready time is the time when the task set ready. Task can only start after READY."))
    start_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Start Time"), help_text=_("Task start time is the time when the task start to run."))
    expire_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Expire Time"), help_text=_("Task expire time is the time when the task deactived. A task is expired, it will never be runned, even it is not runned yet."))
    done_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Done Time"), help_text=_("Task done time is the time when the task finished ."))

    auto_ready = True

    class Meta:
        abstract = True

    SIMPLE_TASK_FIELDS = [
        "status",
        "active",
        "worker",

        "success",
        "result",
        "error_code",
        "error_message",

        "add_time",
        "ready_time",
        "start_time",
        "expire_time",
        "done_time",
        "mod_time",
    ]

    def get_active_status(self):
        if self.status in [self.DONE, self.FAILED]:
            return False
        if self.expire_time and self.expire_time < timezone.now():
            return False
        return True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.reset()
        self.active = self.get_active_status()
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

    def reset(self, ready_time=None, ready_timeout=None, expire_time=None, save=False):
        self.status = self.NEW
        self.active = False
        self.worker = None
        self.ready_time = None
        self.start_time = None
        self.expire_time = None
        self.done_time = None
        self.success = None
        self.result = None
        self.error_code = None
        self.error_message = None
        if self.auto_ready:
            self.ready(ready_time=ready_time, ready_timeout=ready_timeout, expire_time=expire_time, save=False)
        if save:
            self.save()

    def ready(self, ready_time=None, ready_timeout=None, expire_time=None, save=False):
        if self.status != self.NEW:
            return False
        self.status = self.READY
        self.active = True
        self.ready_time = ready_time or timezone.now()
        if expire_time:
            self.expire_time = expire_time
        elif ready_timeout:
            self.expire_time = self.ready_time + datetime.timedelta(seconds=ready_timeout)
        if save:
            self.save()
        return True

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
        self.active = False
        self.success = True
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
        self.active = False
        self.success = False
        self.error_code = error_code
        self.error_message = error_message
        self.done_time = timezone.now()
        if save:
            self.save()
        return True

