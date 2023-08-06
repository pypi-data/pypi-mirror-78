from mlflow.store.tracking.rest_store import RestStore
from mlflow.utils.rest_utils import MlflowHostCreds
from infinstor_mlflow_plugin.tokenfile import get_token
from os.path import expanduser
from os.path import sep as separator

class CognitoAuthenticatedRestStore(RestStore):
    def cognito_host_creds(self):
        tokfile = expanduser("~") + separator + '.infinstor' + separator + 'token'
        token, service = get_token(tokfile, False)
        return MlflowHostCreds('https://mlflow.' + service + '.com:443/', token=token)

    def get_service(self):
        tokfile = expanduser("~") + separator + '.infinstor' + separator + 'token'
        token, service = get_token(tokfile, False)
        return service

    def get_token_string(self):
        tokfile = expanduser("~") + separator + '.infinstor' + separator + 'token'
        token, service = get_token(tokfile, False)
        return token

    def __init__(self, store_uri=None, artifact_uri=None):
        super().__init__(self.cognito_host_creds)

