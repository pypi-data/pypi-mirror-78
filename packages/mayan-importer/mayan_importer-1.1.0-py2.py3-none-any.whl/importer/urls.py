from django.conf.urls import url

from .views import (
    ImportSetupBackendSelectionView, ImportSetupCreateView,
    ImportSetupDeleteView, ImportSetupEditView, ImportSetupExecuteView,
    ImportSetupItemsClearView, ImportSetupListView, ImportSetupPopulateView
)

urlpatterns = [
    url(
        regex=r'^import_setups/$', name='import_setup_list',
        view=ImportSetupListView.as_view()
    ),
    url(
        regex=r'^import_setups/backend/selection/$',
        name='import_setup_backend_selection',
        view=ImportSetupBackendSelectionView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<class_path>[a-zA-Z0-9_.]+)/create/$',
        name='import_setup_create',
        view=ImportSetupCreateView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<import_setup_id>\d+)/delete/$',
        name='import_setup_delete', view=ImportSetupDeleteView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<import_setup_id>\d+)/edit/$',
        name='import_setup_edit', view=ImportSetupEditView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<import_setup_id>\d+)/execute/$',
        name='import_setup_execute', view=ImportSetupExecuteView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<import_setup_id>\d+)/items/clear/$',
        name='import_setup_items_clear',
        view=ImportSetupItemsClearView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<import_setup_id>\d+)/populate/$',
        name='import_setup_populate', view=ImportSetupPopulateView.as_view()
    ),
]
