import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import (
    permission_acl_edit, permission_acl_view
)
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import (
    menu_list_facet, menu_object, menu_secondary, menu_setup
)
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list,
)
from mayan.apps.events.permissions import permission_events_view
from mayan.apps.navigation.classes import SourceColumn

from .events import event_import_setup_edited, event_import_setup_executed
from .links import (
    link_import_setup_create, link_import_setup_delete,
    link_import_setup_edit, link_import_setup_items_clear,
    link_import_setup_list, link_import_setup_populate,
    link_import_setup_process, link_import_setup_setup,
)
from .permissions import (
    permission_import_setup_delete, permission_import_setup_edit,
    permission_import_setup_use, permission_import_setup_view
)

logger = logging.getLogger(name=__name__)


class ImporterApp(MayanAppConfig):
    app_namespace = 'importer'
    app_url = 'importer'
    has_rest_api = False
    has_tests = True
    name = 'importer'
    verbose_name = _('Importer')

    def ready(self):
        super().ready()

        ImportSetup = self.get_model(model_name='ImportSetup')

        EventModelRegistry.register(model=ImportSetup)

        ModelEventType.register(
            model=ImportSetup, event_types=(
                event_import_setup_edited, event_import_setup_executed
            )
        )

        ModelPermission.register(
            model=ImportSetup, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_events_view, permission_import_setup_delete,
                permission_import_setup_edit, permission_import_setup_use,
                permission_import_setup_view
            )
        )
        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=ImportSetup
        )
        SourceColumn(
            attribute='item_count_percent', empty_value=_('0%'),
            include_label=True, source=ImportSetup
        )

        menu_list_facet.bind_links(
            links=(
                link_acl_list, link_events_for_object,
                link_object_event_types_user_subcriptions_list,
            ), sources=(ImportSetup,)
        )

        menu_object.bind_links(
            links=(
                link_import_setup_delete, link_import_setup_edit,
                link_import_setup_items_clear, link_import_setup_populate,
                link_import_setup_process
            ), sources=(ImportSetup,)
        )
        menu_secondary.bind_links(
            links=(link_import_setup_create, link_import_setup_list),
            sources=(
                ImportSetup, 'importer:import_setup_list',
                'importer:import_setup_create'
            )
        )
        menu_setup.bind_links(
            links=(link_import_setup_setup,)
        )
