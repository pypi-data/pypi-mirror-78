from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Importer'), name='importer')

permission_import_setup_create = namespace.add_permission(
    label=_('Create import setups'), name='import_setup_create'
)
permission_import_setup_delete = namespace.add_permission(
    label=_('Delete import setups'), name='import_setup_delete'
)
permission_import_setup_edit = namespace.add_permission(
    label=_('Edit import setups'), name='import_setup_edit'
)
permission_import_setup_execute = namespace.add_permission(
    label=_('Execute import setups'), name='import_setup_execute'
)
permission_import_setup_view = namespace.add_permission(
    label=_('View import setups'), name='import_setup_view'
)
