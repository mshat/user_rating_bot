import time
from celery import shared_task
from user_rating.services.update_reactions import update_reactions


@shared_task(name="repeat_order_make")
def repeat_order_make():
    res = update_reactions()
    print(res)


@shared_task
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True

