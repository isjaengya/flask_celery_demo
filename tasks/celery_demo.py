from extensions import celery


@celery.task
def celery_demo(id):
    from api.models.user import User
    user = User.find_by_id(id)
    print(user.to_json(), '111111111111111111111111111111111111111111')
