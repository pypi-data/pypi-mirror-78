import re
import shutil

import dropbox

from django.core.files import File
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.models import SharedUploadedFile
from mayan.apps.storage.utils import NamedTemporaryFile

from credentials.credentials import OAuthAccessToken

from .classes import ImportSetupBackend


class ImporterDropbox(ImportSetupBackend):
    class_fields = ('filename_regex', 'folder_regex')
    field_order = ('filename_regex', 'folder_regex')
    fields = {
        'filename_regex': {
            'label': _('Filename regular expression'),
            'class': 'django.forms.CharField', 'default': '',
            'help_text': _(
                'An optional regular expression used to filter which files '
                'to import. The regular expression will be matched against '
                'the filename.'
            ),
            'kwargs': {
                'max_length': 248
            }, 'required': False
        },
        'folder_regex': {
            'label': _('Folder regular expression'),
            'class': 'django.forms.CharField', 'default': '',
            'help_text': _(
                'An optional regular expression used to filter which files '
                'to import. The regular expression will be matched against '
                'the file folder path.'
            ),
            'kwargs': {
                'max_length': 248
            }, 'required': False
        },
    }
    label = _('Dropbox')
    item_identifier = 'id'  # Dropbox file unique indentifier
    item_label = 'name'  # Dropbox file field corresponding to the filename

    def __init__(self, credential_class, credential_data, kwargs):
        self.credential_class = credential_class
        self.credential_data = credential_data
        self.kwargs = kwargs

    def get_client(self):
        """
        Return an instance of the Dropbox API client.
        """
        if issubclass(self.credential_class, OAuthAccessToken):
            kwargs = {
                'oauth2_access_token': self.credential_data['access_token']
            }
        else:
            raise ImproperlyConfigured(
                'Unknown credential class `{}`.'.format(
                    self.credential_class.label
                )
            )

        return dropbox.Dropbox(**kwargs)

    def get_item(self, item):
        client = self.get_client()

        entry_metadata, response = client.files_download(path=item.identifier)

        response.raise_for_status()

        # Copy the Dropbox file to a temporary location using streaming
        # download.
        # The create a shared upload instance from the temporary file.
        with NamedTemporaryFile() as file_object:
            shutil.copyfileobj(fsrc=response.raw, fdst=file_object)

            file_object.seek(0)

            return SharedUploadedFile.objects.create(
                file=File(file_object),
            )

    def get_item_list(self):
        """
        Crawl the folders and add all the items that are actual files as
        ImportSetupItem instances for later processing.
        """
        client = self.get_client()
        response = client.files_list_folder(
            path='', include_non_downloadable_files=False, recursive=True
        )

        match_filename = self.match_filename_factory()
        match_folder = self.match_folder_factory()

        while True:
            for entry in response.entries:
                if isinstance(entry, dropbox.files.FileMetadata):
                    # Only add files not directories

                    if match_folder(entry=entry) and match_filename(entry=entry):
                        yield {
                            'id': entry.id,
                            'name': entry.name,
                            'size': entry.size,
                            'path_lower': entry.path_lower,
                            'content_hash': entry.content_hash,
                        }

            if not response.has_more:
                break
            else:
                response = client.files_list_folder_continue(
                    cursor=response.cursor
                )

    def match_filename_factory(self):
        """
        Perform a regular expression of and entry's filename.
        Returns True if there is a regular expression match or if there is no
        regular expression set.
        """
        pattern = self.kwargs['filename_regex']
        if pattern:
            regex = re.compile(pattern=pattern)

            def match_function(entry):
                return regex.match(string=entry.name)
        else:
            def match_function(entry):
                return True

        return match_function

    def match_folder_factory(self):
        """
        Perform a regular expression of and entry's path.
        Returns True if there is a regular expression match or if there is no
        regular expression set.
        """
        pattern = self.kwargs['folder_regex']
        if pattern:
            regex = re.compile(pattern=pattern)

            def match_function(entry):
                return regex.match(string=entry.path_lower)
        else:
            def match_function(entry):
                return True

        return match_function
