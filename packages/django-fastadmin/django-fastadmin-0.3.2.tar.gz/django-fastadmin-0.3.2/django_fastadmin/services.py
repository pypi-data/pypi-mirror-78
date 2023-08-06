import datetime

from fastutils import randomutils

from django.urls import path
from django.utils import timezone
from django.db.models import Q

from django_apiview.views import apiview
from django_db_lock.client import DjangoDbLock


class SimpleTaskService(object):

    def __init__(self, model, lock_service):
        self.model = model
        self.lock_service = lock_service
        self.app_label = self.model._meta.app_label
        self.model_name = self.model._meta.model_name

    def getGetReadyTasksView(self):
        @apiview
        def getReadyTasks(worker, n: int=1):
            tasks = self.get_ready_tasks(worker, n)
            result = []
            for task in tasks:
                result.append(task.info())
            return result
        return getReadyTasks
    
    def getResetDeadTasksView(self):
        @apiview
        def resetDeadTasks():
            tasks = self.reset_dead_tasks()
            return len(tasks)
        return resetDeadTasks

    def getReportSuccessView(self):
        @apiview
        def reportSuccess(worker, id: int, result):
            self.model.get(pk=id).report_success(worker, result, save=True)
            return True
        return reportSuccess

    def getReportErrorView(self):
        @apiview
        def reportError(worker, id: int, error_code, error_message):
            self.model.get(pk=id).report_error(worker, error_code, error_message, save=True)
            return True
        return reportError

    def get_urls(self):
        return [
            path('getReadyTasks', self.getGetReadyTasksView(), name="{}.{}.{}".format(self.app_label, self.model_name, "getReadyTasks")),
            path('resetDeadTasks', self.getResetDeadTasksView(), name="{}.{}.{}".format(self.app_label, self.model_name, "resetDeadTasks")),
            path('reportSuccess', self.getReportSuccessView(), name="{}.{}.{}".format(self.app_label, self.model_name, "reportSuccess")),
            path('reportError', self.getReportErrorView(), name="{}.{}.{}".format(self.app_label, self.model_name, "reportError")),
        ]

    def get_ready_tasks(self, worker, n=1, reset_dead_task=True):
        # auto reset dead tasks
        if reset_dead_task:
            self.reset_dead_tasks()
        # get ready tasks
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        lock_name = self.model.GET_READY_TASKS_LOCK_NAME_TEMPLATE.format(app_label=app_label, model_name=model_name)
        timeout = self.model.GET_READY_TASKS_LOCK_TIMEOUT
        with DjangoDbLock(self.lock_service, lock_name, str(randomutils.uuid4()), timeout) as locked:
            if not locked:
                return []
            now = timezone.now()
            tasks = self.model.objects.filter(status=self.model.READY).filter(ready_time__lte=now).filter(Q(expire_time=None) | Q(expire_time__gte=now)).order_by("mod_time")[:n]
            for task in tasks:
                task.start(worker, save=True)
            return tasks

    def reset_dead_tasks(self):
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        lock_name = self.model.RESET_DEAD_TASKS_LOCK_NAME_TEMPLATE.format(app_label=app_label, model_name=model_name)
        timeout = self.model.RESET_DEAD_TASKS_LOCK_TIMEOUT
        with DjangoDbLock(self.lock_service, lock_name, str(randomutils.uuid4()), timeout) as locked:
            if not locked:
                return []
            dead_time_limit = timezone.now() - datetime.timedelta(seconds=self.model.TASK_DOING_TIMEOUT)
            tasks = self.model.objects.filter(status=self.model.DOING).filter(start_time__lte=dead_time_limit)
            for task in tasks:
                task.reset(save=True)
            return tasks

    def do_tasks(self, worker, n: int=100):
        done = 0
        failed = 0
        stime = datetime.datetime.now()
        for task in self.get_ready_tasks(worker, n):
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
