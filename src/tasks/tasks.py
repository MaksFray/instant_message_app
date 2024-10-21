from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379')


def get_message_template(username: str):
    content = f"Hello, {username}! You have unread message!"
    return content

@celery.task
def send_unread_message_report(username: str):
    '''
    Add here code for sending report about unread message via telegram
    :param username:
    :return:
    '''
    print(get_message_template(username))