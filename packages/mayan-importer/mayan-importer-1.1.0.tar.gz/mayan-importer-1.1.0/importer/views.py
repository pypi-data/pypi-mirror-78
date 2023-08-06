import logging

from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.generics import (
    ConfirmView, FormView, SingleObjectDeleteView,
    SingleObjectDynamicFormCreateView, SingleObjectDynamicFormEditView,
    SingleObjectListView
)

from .classes import ImportSetupBackend
from .forms import (
    ImportSetupBackendSelectionForm, ImportSetupBackendDynamicForm
)
from .icons import icon_import_setup_list
from .links import link_import_setup_backend_selection
from .models import ImportSetup
from .permissions import (
    permission_import_setup_create, permission_import_setup_delete,
    permission_import_setup_edit, permission_import_setup_execute,
    permission_import_setup_view
)
from .tasks import task_import_setup_execute, task_import_setup_populate

logger = logging.getLogger(name=__name__)


class ImportSetupBackendSelectionView(FormView):
    extra_context = {
        'title': _('New import backend selection'),
    }
    form_class = ImportSetupBackendSelectionForm
    view_permission = permission_import_setup_create

    def form_valid(self, form):
        backend = form.cleaned_data['backend']
        return HttpResponseRedirect(
            redirect_to=reverse(
                viewname='importer:import_setup_create', kwargs={
                    'class_path': backend
                }
            )
        )


class ImportSetupCreateView(SingleObjectDynamicFormCreateView):
    form_class = ImportSetupBackendDynamicForm
    post_action_redirect = reverse_lazy(
        viewname='importer:import_setup_list'
    )
    view_permission = permission_import_setup_create

    def get_backend(self):
        try:
            return ImportSetupBackend.get(name=self.kwargs['class_path'])
        except KeyError:
            raise Http404(
                '{} class not found'.format(self.kwargs['class_path'])
            )

    def get_extra_context(self):
        return {
            'title': _(
                'Create a "%s" import setup'
            ) % self.get_backend().label,
        }

    def get_form_schema(self):
        backend = self.get_backend()
        result = {
            'fields': backend.fields,
            'widgets': getattr(backend, 'widgets', {})
        }
        if hasattr(backend, 'field_order'):
            result['field_order'] = backend.field_order

        return result

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'backend_path': self.kwargs['class_path']
        }


class ImportSetupDeleteView(SingleObjectDeleteView):
    model = ImportSetup
    object_permission = permission_import_setup_delete
    pk_url_kwarg = 'import_setup_id'
    post_action_redirect = reverse_lazy(viewname='importer:import_setup_list')

    def get_extra_context(self):
        return {
            'import_setup': None,
            'object': self.object,
            'title': _('Delete the import setup: %s?') % self.object,
        }


class ImportSetupEditView(SingleObjectDynamicFormEditView):
    form_class = ImportSetupBackendDynamicForm
    model = ImportSetup
    object_permission = permission_import_setup_edit
    pk_url_kwarg = 'import_setup_id'
    post_action_redirect = reverse_lazy(viewname='importer:import_setup_list')

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit import setup: %s') % self.object,
        }

    def get_form_schema(self):
        backend = self.object.get_backend()
        result = {
            'fields': backend.fields,
            'widgets': getattr(backend, 'widgets', {})
        }
        if hasattr(backend, 'field_order'):
            result['field_order'] = backend.field_order

        return result

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class ImportSetupExecuteView(ConfirmView):
    post_action_redirect = reverse_lazy(
        viewname='importer:import_setup_list'
    )

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Process items of import setup: %s') % self.get_object()
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_object(self):
        return get_object_or_404(
            klass=self.get_queryset(), pk=self.kwargs['import_setup_id']
        )

    def get_queryset(self):
        return AccessControlList.objects.restrict_queryset(
            permission=permission_import_setup_execute,
            queryset=ImportSetup.objects.all(), user=self.request.user
        )

    def view_action(self):
        task_import_setup_execute.apply_async(
            kwargs=dict(import_setup_id=self.get_object().pk)
        )

        messages.success(
            message=_('Import setup item processing queued.'),
            request=self.request
        )


class ImportSetupItemsClearView(ConfirmView):
    post_action_redirect = reverse_lazy(
        viewname='importer:import_setup_list'
    )

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Clear the items of import setup: %s') % self.get_object()
        }

    def get_object(self):
        return get_object_or_404(
            klass=self.get_queryset(), pk=self.kwargs['import_setup_id']
        )

    def get_queryset(self):
        return AccessControlList.objects.restrict_queryset(
            permission=permission_import_setup_execute,
            queryset=ImportSetup.objects.all(), user=self.request.user
        )

    def view_action(self):
        self.get_object().items_clear()

        messages.success(
            message=_('Import setup items cleared.'),
            request=self.request
        )


class ImportSetupListView(SingleObjectListView):
    model = ImportSetup
    object_permission = permission_import_setup_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_import_setup_list,
            'no_results_main_link': link_import_setup_backend_selection.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Import setups are configuration units that will retrieve '
                'files for external locations and create documents from '
                'them.'
            ),
            'no_results_title': _('No import setups available'),
            'title': _('Import setups'),
        }


class ImportSetupPopulateView(ConfirmView):
    post_action_redirect = reverse_lazy(
        viewname='importer:import_setup_list'
    )

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Populate import setup: %s') % self.get_object()
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_object(self):
        return get_object_or_404(
            klass=self.get_queryset(), pk=self.kwargs['import_setup_id']
        )

    def get_queryset(self):
        return AccessControlList.objects.restrict_queryset(
            permission=permission_import_setup_execute,
            queryset=ImportSetup.objects.all(), user=self.request.user
        )

    def view_action(self):
        task_import_setup_populate.apply_async(
            kwargs=dict(import_setup_id=self.get_object().pk)
        )

        messages.success(
            message=_('Import setup populate queued.'), request=self.request
        )
