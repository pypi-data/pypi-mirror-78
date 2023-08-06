from django.conf.urls import url

from .views import (
    ImportSetupCreateView, ImportSetupDeleteView, ImportSetupEditView,
    ImportSetupItemsClearView, ImportSetupListView, ImportSetupPopulateView,
    ImportSetupProcessItemsView
)

urlpatterns = [
    url(
        regex=r'^import_setups/$', name='import_setup_list',
        view=ImportSetupListView.as_view()
    ),
    url(
        regex=r'^import_setups/create/$', name='import_setup_create',
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
        regex=r'^import_setups/(?P<import_setup_id>\d+)/items/clear/$',
        name='import_setup_items_clear',
        view=ImportSetupItemsClearView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<import_setup_id>\d+)/populate/$',
        name='import_setup_populate', view=ImportSetupPopulateView.as_view()
    ),
    url(
        regex=r'^import_setups/(?P<import_setup_id>\d+)/process/$',
        name='import_setup_process', view=ImportSetupProcessItemsView.as_view()
    ),
]
