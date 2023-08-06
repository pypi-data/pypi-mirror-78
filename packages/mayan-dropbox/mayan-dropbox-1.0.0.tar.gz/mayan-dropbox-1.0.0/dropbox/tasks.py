import logging

from django.apps import apps

from mayan.celery import app

logger = logging.getLogger(name=__name__)


@app.task(ignore_result=True)
def task_import_setup_populate(import_setup_id):
    ImportSetup = apps.get_model(
        app_label='dropbox', model_name='ImportSetup'
    )

    import_setup = ImportSetup.objects.get(pk=import_setup_id)
    import_setup.populate_items()


@app.task(ignore_result=True)
def task_import_setup_process_items(import_setup_id):
    ImportSetup = apps.get_model(
        app_label='dropbox', model_name='ImportSetup'
    )

    import_setup = ImportSetup.objects.get(pk=import_setup_id)
    import_setup.process_items()
