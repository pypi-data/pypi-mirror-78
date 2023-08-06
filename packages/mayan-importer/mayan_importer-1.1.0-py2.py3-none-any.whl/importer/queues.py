from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_medium

queue_importer = CeleryQueue(
    label=_('Importer'), name='importer', worker=worker_medium
)

queue_importer.add_task_type(
    label=_('Execute an import setup'),
    dotted_path='importer.tasks.task_import_setup_execute'
)
queue_importer.add_task_type(
    label=_('Populate the items of an import setup'),
    dotted_path='importer.tasks.task_import_setup_populate'
)
