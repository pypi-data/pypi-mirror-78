import json

TEST_CREDENTIAL_BACKEND_PATH = 'mayan.apps.credentials.credentials.OAuthAccessToken'
TEST_CREDENTIAL_BACKEND_DATA_FIELDS = {'access_token': 'access_token_data'}
TEST_CREDENTIAL_BACKEND_DATA = json.dumps(
    obj=TEST_CREDENTIAL_BACKEND_DATA_FIELDS
)
TEST_CREDENTIAL_LABEL = 'test credential'
TEST_CREDENTIAL_LABEL_EDITED = 'test credential edited'
