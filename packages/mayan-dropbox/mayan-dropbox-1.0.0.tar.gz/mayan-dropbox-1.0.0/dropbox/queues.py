from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_medium

queue_dropbox = CeleryQueue(
    label=_('Dropbox'), name='dropbox', worker=worker_medium
)

queue_dropbox.add_task_type(
    label=_('Populate the items of an import setup'),
    dotted_path='mayan.apps.dropbox.tasks.task_import_setup_populate'
)
queue_dropbox.add_task_type(
    label=_('Download the items of an import setup'),
    dotted_path='mayan.apps.dropbox.tasks.task_import_setup_process_items'
)
