from ..models import ImportSetup

from .literals import (
    TEST_IMPORT_SETUP_LABEL, TEST_IMPORT_SETUP_LABEL_EDITED,
    TEST_IMPORT_SETUP_PROCESS_SIZE
)


class ImportSetupTestMixin(object):
    def _create_test_import_setup(self):
        self.test_import_setup = ImportSetup.objects.create(
            label=TEST_IMPORT_SETUP_LABEL, credential=self.test_credential,
            document_type=self.test_document_type
        )


class ImportSetupViewTestMixin(object):
    def _request_test_import_setup_create_view(self):
        return self.post(
            viewname='importer:import_setup_create', data={
                'label': TEST_IMPORT_SETUP_LABEL,
                'credential': self.test_credential.pk,
                'document_type': self.test_document_type.pk,
                'process_size': TEST_IMPORT_SETUP_PROCESS_SIZE
            }
        )

    def _request_test_import_setup_delete_view(self):
        return self.post(
            viewname='importer:import_setup_delete', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }
        )

    def _request_test_import_setup_edit_view(self):
        return self.post(
            viewname='importer:import_setup_edit', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }, data={
                'label': TEST_IMPORT_SETUP_LABEL_EDITED,
                'credential': self.test_credential.pk,
                'document_type': self.test_document_type.pk,
                'process_size': TEST_IMPORT_SETUP_PROCESS_SIZE
            }
        )

    def _request_test_import_setup_list_view(self):
        return self.get(viewname='importer:import_setup_list')
