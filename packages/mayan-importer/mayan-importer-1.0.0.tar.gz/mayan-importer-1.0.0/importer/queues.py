from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_medium

queue_importer = CeleryQueue(
    label=_('Importer'), name='importer', worker=worker_medium
)

queue_importer.add_task_type(
    label=_('Populate the items of an import setup'),
    dotted_path='mayan.apps.importer.tasks.task_import_setup_populate'
)
queue_importer.add_task_type(
    label=_('Download the items of an import setup'),
    dotted_path='mayan.apps.importer.tasks.task_import_setup_process_items'
)
