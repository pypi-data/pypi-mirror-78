
from ..models import StoredCredential

from .literals import (
    TEST_CREDENTIAL_BACKEND_DATA_FIELDS, TEST_CREDENTIAL_BACKEND_DATA,
    TEST_CREDENTIAL_BACKEND_PATH, TEST_CREDENTIAL_LABEL,
    TEST_CREDENTIAL_LABEL_EDITED
)


class CredentialTestMixin(object):
    def _create_test_credential(self):
        self.test_credential = StoredCredential.objects.create(
            label=TEST_CREDENTIAL_LABEL,
            backend_path=TEST_CREDENTIAL_BACKEND_PATH,
            backend_data=TEST_CREDENTIAL_BACKEND_DATA
        )


class CredentialViewTestMixin(object):
    def _request_test_credential_backend_selection_view(self):
        return self.post(
            viewname='credentials:stored_credential_backend_selection', data={
                'backend': TEST_CREDENTIAL_BACKEND_PATH,
            }
        )

    def _request_test_credential_create_view(self):
        data = {'label': TEST_CREDENTIAL_LABEL}
        data.update(TEST_CREDENTIAL_BACKEND_DATA_FIELDS)

        return self.post(
            viewname='credentials:stored_credential_create', kwargs={
                'class_path': TEST_CREDENTIAL_BACKEND_PATH,
            }, data=data
        )

    def _request_test_credential_delete_view(self):
        return self.post(
            viewname='credentials:stored_credential_delete', kwargs={
                'stored_credential_id': self.test_credential.pk
            }
        )

    def _request_test_credential_edit_view(self):
        data = {'label': TEST_CREDENTIAL_LABEL_EDITED}
        data.update(TEST_CREDENTIAL_BACKEND_DATA_FIELDS)

        return self.post(
            viewname='credentials:stored_credential_edit', kwargs={
                'stored_credential_id': self.test_credential.pk
            }, data=data
        )

    def _request_test_credential_list_view(self):
        return self.get(viewname='credentials:stored_credential_list')
