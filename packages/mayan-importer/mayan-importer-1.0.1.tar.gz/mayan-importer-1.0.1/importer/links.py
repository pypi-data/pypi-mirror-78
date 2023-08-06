from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_cascade_condition

from .permissions import (
    permission_import_setup_create, permission_import_setup_delete,
    permission_import_setup_edit, permission_import_setup_use,
    permission_import_setup_view
)

link_import_setup_create = Link(
    icon_class_path='mayan.apps.importer.icons.icon_import_setup_create',
    permissions=(permission_import_setup_create,),
    text=_('Create import setup'), view='importer:import_setup_create'
)
link_import_setup_delete = Link(
    args='object.pk',
    icon_class_path='mayan.apps.importer.icons.icon_import_setup_delete',
    permissions=(permission_import_setup_delete,),
    tags='dangerous', text=_('Delete'), view='importer:import_setup_delete'
)
link_import_setup_edit = Link(
    args='object.pk',
    icon_class_path='mayan.apps.importer.icons.icon_import_setup_edit',
    permissions=(permission_import_setup_edit,), text=_('Edit'),
    view='importer:import_setup_edit'
)
link_import_setup_items_clear = Link(
    args='object.pk',
    icon_class_path='mayan.apps.importer.icons.icon_import_setup_items_clear',
    permissions=(permission_import_setup_use,), text=_('Clear items'),
    view='importer:import_setup_items_clear'
)
link_import_setup_list = Link(
    icon_class_path='mayan.apps.importer.icons.icon_import_setup_list',
    text=_('Import setup list'),
    view='importer:import_setup_list'
)
link_import_setup_populate = Link(
    args='object.pk',
    icon_class_path='mayan.apps.importer.icons.icon_import_setup_populate',
    permissions=(permission_import_setup_use,), text=_('Populate'),
    view='importer:import_setup_populate'
)
link_import_setup_process = Link(
    args='object.pk',
    icon_class_path='mayan.apps.importer.icons.icon_import_setup_process',
    permissions=(permission_import_setup_use,), text=_('Process'),
    view='importer:import_setup_process'
)
link_import_setup_setup = Link(
    condition=get_cascade_condition(
        app_label='importer', model_name='ImportSetup',
        object_permission=permission_import_setup_view,
        view_permission=permission_import_setup_create,
    ), icon_class_path='mayan.apps.importer.icons.icon_import_setup_list',
    text=_('Importer'),
    view='importer:import_setup_list'
)
