from django.urls import path
from django_apiview.views import apiview


class SimpleTaskServices(object):
    def __init__(self, model):
        self.model = model
        self.app_label = self.model._meta.app_label
        self.model_name = self.model._meta.model_name

    def get_ready_tasks(self):
        @apiview
        def getReadyTasks(worker, n: int=1):
            tasks = self.model.get_ready_tasks(worker, n)
            result = []
            for task in tasks:
                result.append(task.info())
            return result
        return getReadyTasks
    
    def reset_dead_tasks(self):
        @apiview
        def resetDeadTasks():
            tasks = self.model.reset_dead_tasks()
            return len(tasks)
        return resetDeadTasks

    def report_success(self):
        @apiview
        def reportSuccess(worker, id: int, result):
            self.model.get(pk=id).report_success(worker, result, save=True)
            return True
        return reportSuccess

    def report_error(self):
        @apiview
        def reportError(worker, id: int, error_code, error_message):
            self.model.get(pk=id).report_error(worker, error_code, error_message, save=True)
            return True
        return reportError

    def get_urls(self):
        return [
            path('getReadyTasks', self.get_ready_tasks, name="{}.{}.{}".format(self.app_label, self.model_name, "getReadyTasks")),
            path('resetDeadTasks', self.reset_dead_tasks, name="{}.{}.{}".format(self.app_label, self.model_name, "resetDeadTasks")),
            path('reportSuccess', self.report_success, name="{}.{}.{}".format(self.app_label, self.model_name, "reportSuccess")),
            path('reportError', self.report_error, name="{}.{}.{}".format(self.app_label, self.model_name, "reportError")),
        ]
