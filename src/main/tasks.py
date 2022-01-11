from core.celery import app


# def work_with_task(task_id):
#     task = Task.objects.get(id=task_id)
#     task.status = TaskStatus.objects.get(id=2)
#     task.save()
#
#     return task
from main.modules import parser_starter


@app.task
def start_parse(task_id):
    # task = work_with_task(task_id)
    #
    # items = list(task.data.values())[0]
    #
    # starter = (task)
    parser_starter
