from api.app import create_app, celery

app = create_app()
app.app_context().push()
