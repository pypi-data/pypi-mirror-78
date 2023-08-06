import json

from django.conf import settings
from django.db import models, transaction
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.serialization import yaml_load
from mayan.apps.common.validators import YAMLValidator
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.events.classes import (
    EventManagerMethodAfter, EventManagerSave
)
from mayan.apps.events.decorators import method_event
from mayan.apps.metadata.models import MetadataType

from credentials.models import StoredCredential

from .classes import NullBackend
from .events import (
    event_import_setup_created, event_import_setup_edited,
    event_import_setup_executed
)
from .literals import (
    ITEM_STATE_CHOICES, ITEM_STATE_COMPLETE, ITEM_STATE_DOWNLOADED,
    ITEM_STATE_ERROR, ITEM_STATE_QUEUED, ITEM_STATE_NONE, DEFAULT_PROCESS_SIZE
)


class BackendModelMixin(models.Model):
    backend_path = models.CharField(
        max_length=128,
        help_text=_('The dotted Python path to the backend class.'),
        verbose_name=_('Backend path')
    )
    backend_data = models.TextField(
        blank=True, verbose_name=_('Backend data')
    )

    class Meta:
        abstract = True

    def get_backend(self):
        """
        Retrieves the backend by importing the module and the class.
        """
        try:
            return import_string(dotted_path=self.backend_path)
        except ImportError:
            return NullBackend

    def get_backend_label(self):
        """
        Return the label that the backend itself provides. The backend is
        loaded but not initialized. As such the label returned is a class
        property.
        """
        return self.get_backend().label

    get_backend_label.short_description = _('Backend')
    get_backend_label.help_text = _('The backend class for this entry.')

    def get_backend_data(self):
        return json.loads(s=self.backend_data or '{}')

    def set_backend_data(self, obj):
        self.backend_data = json.dumps(obj=obj)


class ImportSetup(BackendModelMixin, models.Model):
    label = models.CharField(
        help_text=_('Short description of this import setup.'), max_length=128,
        unique=True, verbose_name=_('Label')
    )
    credential = models.ForeignKey(
        on_delete=models.CASCADE, related_name='import_setups',
        to=StoredCredential, verbose_name=_('Credential')
    )
    document_type = models.ForeignKey(
        on_delete=models.CASCADE, related_name='import_setups',
        to=DocumentType, verbose_name=_('Document type')
    )
    process_size = models.PositiveIntegerField(
        default=DEFAULT_PROCESS_SIZE, help_text=_(
            'Number of items to process per execution.'
        ), verbose_name=_('Process size.')
    )
    metadata_map = models.TextField(
        blank=True, help_text=_(
            'A YAML encoded dictionary to save the content of the item '
            'properties as metadata values. The dictionary must consist of '
            'an import item property key matched to a metadata type name.'
        ), validators=[YAMLValidator()], verbose_name=_('Metadata map')
    )

    class Meta:
        ordering = ('label',)
        verbose_name = _('Import setup')
        verbose_name_plural = _('Import setups')

    def __str__(self):
        return self.label

    def create_document_from_item(self, item, shared_uploaded_file):
        """
        Create a document from a downloaded ImportSetupItem instance.
        """
        backend_class = self.get_backend()

        metadata_map = {}

        for key, metadata_name in yaml_load(stream=self.metadata_map or '{}').items():
            metadata_map[key] = MetadataType.objects.get(name=metadata_name)

        with transaction.atomic():
            try:
                with shared_uploaded_file.open() as file_object:
                    document = self.document_type.new_document(
                        file_object=file_object, label=item.get_metadata_key(
                            key=backend_class.item_label
                        )
                    )

                item.state = ITEM_STATE_COMPLETE
                item.state_data = ''
                item.save()
            except Exception as exception:
                document = None
                item.state = ITEM_STATE_ERROR
                item.state_data = str(exception)
                item.save()
                if settings.DEBUG:
                    raise

        if document:
            for key, metadata_type in metadata_map.items():
                document.metadata.create(
                    metadata_type=metadata_type,
                    value=item.get_metadata_key(key=key)
                )

    def execute(self):
        """
        Iterate of the ImportSetupItem instances downloading and creating
        documents from them.
        """
        queryset = self.items.filter(state=ITEM_STATE_NONE)[:self.process_size]

        for item in queryset.all():
            self.process_item(item=item)

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_import_setup_executed,
        target='self',
    )
    def get_backend_instance(self):
        return self.get_backend()(
            credential_class=self.credential.get_backend(),
            credential_data=self.credential.get_backend_data(),
            kwargs=self.get_backend_data()
        )

    def item_count_all(self):
        return self.items.count()

    item_count_all.short_description = _('Items')

    def item_count_complete(self):
        return self.items.filter(state=ITEM_STATE_COMPLETE).count()

    item_count_complete.short_description = _('Items complete')

    def item_count_percent(self):
        items_complete = self.item_count_complete()
        items_all = self.item_count_all()

        if items_all == 0:
            percent = 0
        else:
            percent = items_complete / items_all * 100.0

        return '{} of {} ({:.0f}%)'.format(items_complete, items_all, percent)

    item_count_percent.short_description = _('Progress')

    def items_clear(self):
        self.items.all().delete()

    def populate_items(self):
        backend = self.get_backend_instance()

        for item in backend.get_item_list():
            setup_item, created = self.items.get_or_create(
                identifier=item[backend.item_identifier]
            )
            if created:
                setup_item.set_metadata(
                    obj=item
                )
                setup_item.save()

    def process_item(self, item):
        """
        Download a ImportSetupItem instance.
        """
        with transaction.atomic():
            try:
                shared_uploaded_file = self.get_backend_instance().get_item(
                    item=item
                )

                item.state = ITEM_STATE_DOWNLOADED
                item.state_data = ''
                item.save()
            except Exception as exception:
                shared_uploaded_file = None
                item.state = ITEM_STATE_ERROR
                item.state_data = str(exception)
                item.save()
                if settings.DEBUG:
                    raise

        if shared_uploaded_file:
            self.create_document_from_item(
                item=item, shared_uploaded_file=shared_uploaded_file
            )

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_import_setup_created,
            'target': 'self',
        },
        edited={
            'event': event_import_setup_edited,
            'target': 'self',
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class ImportSetupItem(models.Model):
    import_setup = models.ForeignKey(
        on_delete=models.CASCADE, related_name='items',
        to=ImportSetup, verbose_name=_('Import setup')
    )
    identifier = models.CharField(
        db_index=True, max_length=64, verbose_name=_('Identifier')
    )
    metadata = models.TextField(blank=True, verbose_name=_('Metadata'))
    state = models.IntegerField(
        choices=ITEM_STATE_CHOICES, default=ITEM_STATE_NONE,
        verbose_name=_('State')
    )
    state_data = models.TextField(blank=True, verbose_name=_('State data'))

    class Meta:
        verbose_name = _('Import setup item')
        verbose_name_plural = _('Import setup items')

    def get_metadata(self):
        return json.loads(s=self.metadata or '{}')

    def get_metadata_key(self, key):
        return self.get_metadata().get(key, self.id)

    def set_metadata(self, obj):
        self.metadata = json.dumps(obj=obj)
