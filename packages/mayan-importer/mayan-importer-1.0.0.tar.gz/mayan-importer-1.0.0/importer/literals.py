from django.utils.translation import ugettext_lazy as _

ITEM_STATE_NONE = 1
ITEM_STATE_ERROR = 2
ITEM_STATE_QUEUED = 3
ITEM_STATE_DOWNLOADED = 4
ITEM_STATE_COMPLETE = 5

ITEM_STATE_CHOICES = (
    (ITEM_STATE_NONE, _('None')),
    (ITEM_STATE_ERROR, _('Error')),
    (ITEM_STATE_QUEUED, _('Queued')),
    (ITEM_STATE_DOWNLOADED, _('Complete')),
    (ITEM_STATE_COMPLETE, _('Complete')),
)

DEFAULT_PROCESS_SIZE = 2
