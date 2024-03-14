from celery._state import _apps


class EnableCeleryTasks(object):
    def __enter__(*args, **kwargs):
        for app in _apps:
            app.conf._task_always_eager = app.conf.task_always_eager
            app.conf.task_always_eager = True

    def __exit__(*args, **kwargs):
        for app in _apps:
            app.conf.task_always_eager = app.conf._task_always_eager


def enable_celery_tasks():
    return EnableCeleryTasks()
