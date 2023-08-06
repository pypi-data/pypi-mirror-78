from django.conf.urls import url

from .views import (
    StoredCredentialBackendSelectionView, StoredCredentialCreateView,
    StoredCredentialDeleteView, StoredCredentialEditView,
    StoredCredentialListView
)


urlpatterns = [
    url(
        regex=r'^stored_credentials/backend/selection/$',
        name='stored_credential_backend_selection',
        view=StoredCredentialBackendSelectionView.as_view()
    ),
    url(
        regex=r'^stored_credentials/(?P<class_path>[a-zA-Z0-9_.]+)/create/$',
        name='stored_credential_create',
        view=StoredCredentialCreateView.as_view()
    ),
    url(
        regex=r'^credentials/(?P<stored_credential_id>\d+)/delete/$',
        name='stored_credential_delete',
        view=StoredCredentialDeleteView.as_view()
    ),
    url(
        regex=r'^credentials/(?P<stored_credential_id>\d+)/edit/$',
        name='stored_credential_edit', view=StoredCredentialEditView.as_view()
    ),
    url(
        regex=r'^stored_credentials/$', name='stored_credential_list',
        view=StoredCredentialListView.as_view()
    )
]
