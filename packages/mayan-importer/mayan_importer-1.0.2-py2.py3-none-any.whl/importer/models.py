import json
import re
import shutil

import dropbox

from django.conf import settings
from django.core.files import File
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.models import SharedUploadedFile
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.events.classes import (
    EventManagerMethodAfter, EventManagerSave
)
from mayan.apps.events.decorators import method_event
from mayan.apps.metadata.models import MetadataType
from mayan.apps.storage.utils import NamedTemporaryFile

from credentials.models import StoredCredential

from .events import (
    event_import_setup_created, event_import_setup_edited,
    event_import_setup_executed
)

from .literals import (
    ITEM_STATE_CHOICES, ITEM_STATE_COMPLETE, ITEM_STATE_DOWNLOADED,
    ITEM_STATE_ERROR, ITEM_STATE_QUEUED, ITEM_STATE_NONE, DEFAULT_PROCESS_SIZE
)


class ImportSetup(models.Model):
    label = models.CharField(
        help_text=_('Short description of this import setup.'),
        max_length=128, verbose_name=_('Label')
    )
    credential = models.ForeignKey(
        on_delete=models.CASCADE, related_name='import_setups',
        to=StoredCredential, verbose_name=_('Credential')
    )
    document_type = models.ForeignKey(
        on_delete=models.CASCADE, related_name='import_setups',
        to=DocumentType, verbose_name=_('Document type')
    )
    folder_regex = models.CharField(
        blank=True, max_length=128, null=True, verbose_name=_(
            'Folder regular expression'
        )
    )
    filename_regex = models.CharField(
        blank=True, max_length=128, null=True, verbose_name=_(
            'Filename regular expression'
        )
    )
    process_size = models.PositiveIntegerField(
        default=DEFAULT_PROCESS_SIZE, help_text=_(
            'Number of items to process per execution.'
        ), verbose_name=_('Process size.')
    )

    class Meta:
        verbose_name = _('Import setup')
        verbose_name_plural = _('Import setups')

    def __str__(self):
        return self.label

    def create_document_from_item(self, item, shared_uploaded_file):
        """
        Create a document from a downloaded ImportSetupItem instance.
        """
        with transaction.atomic():
            try:
                with shared_uploaded_file.open() as file_object:
                    document = self.document_type.new_document(
                        file_object=file_object, label=item.get_metadata_key(
                            key='name'
                        )
                    )

                metadata_type = MetadataType.objects.get(name='dropbox_folder')
                document.metadata.create(
                    metadata_type=metadata_type,
                    value=item.get_metadata_key(key='path_lower')
                )

                item.state = ITEM_STATE_COMPLETE
                item.state_data = ''
                item.save()
            except Exception as exception:
                item.state = ITEM_STATE_ERROR
                item.state_data = str(exception)
                item.save()
                if settings.DEBUG:
                    raise

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_import_setup_executed,
        target='self',
    )
    def get_client(self):
        """
        Return an instance of the Dropbox API client.
        """
        self.credential._event_action_object = self
        return dropbox.Dropbox(
            self.credential.get_backend_data()['access_token']
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

    def match_filename(self, entry):
        """
        Perform a regular expression of and entry's filename.
        Returns True if there is a regular expression match or if there is no
        regular expression set.
        """
        if self.filename_regex:
            return re.match(pattern=self.filename_regex, string=entry.name)
        else:
            return True

    def match_folder(self, entry):
        """
        Perform a regular expression of and entry's path.
        Returns True if there is a regular expression match or if there is no
        regular expression set.
        """
        if self.folder_regex:
            return re.match(pattern=self.folder_regex, string=entry.path_lower)
        else:
            return True

    def populate_items(self):
        """
        Crawl the folders and add all the items that are actual files as
        ImportSetupItem instances for later processing.
        """
        client = self.get_client()
        response = client.files_list_folder(
            path='', include_non_downloadable_files=False, recursive=True
        )

        while True:
            for entry in response.entries:
                if isinstance(entry, dropbox.files.FileMetadata):
                    # Only add files not directories

                    if self.match_folder(entry=entry) and self.match_filename(entry=entry):
                        item, created = self.items.get_or_create(
                            identifier=entry.id
                        )
                        if created:
                            item.set_metadata(
                                obj={
                                    'name': entry.name,
                                    'size': entry.size,
                                    'path_lower': entry.path_lower,
                                    'content_hash': entry.content_hash,
                                }
                            )
                            item.save()

            if not response.has_more:
                break
            else:
                response = client.files_list_folder_continue(
                    cursor=response.cursor
                )

    def process_items(self):
        """
        Iterate of the ImportSetupItem instances downloading and creating
        documents from them.
        """
        queryset = self.items.filter(state=ITEM_STATE_NONE)[:self.process_size]

        for item in queryset.all():
            self.process_item(item=item)

    def process_item(self, item):
        """
        Download a ImportSetupItem instance.
        """
        client = self.get_client()

        entry_metadata, response = client.files_download(path=item.identifier)

        response.raise_for_status()

        # Copy the Dropbox file to a temporary location using streaming
        # download.
        # The create a shared upload instance from the temporary file.
        with NamedTemporaryFile() as file_object:
            shutil.copyfileobj(fsrc=response.raw, fdst=file_object)

            file_object.seek(0)

            with transaction.atomic():
                try:
                    shared_uploaded_file = SharedUploadedFile.objects.create(
                        file=File(file_object),
                    )

                    item.state = ITEM_STATE_DOWNLOADED
                    item.state_data = ''
                    item.save()
                except Exception as exception:
                    item.state = ITEM_STATE_ERROR
                    item.state_data = str(exception)
                    item.save()
                    if settings.DEBUG:
                        raise

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
