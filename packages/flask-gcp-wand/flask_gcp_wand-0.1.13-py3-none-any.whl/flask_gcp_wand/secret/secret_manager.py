from google.cloud import secretmanager
from ..appengine.env import GaeEnv


class SecretHolder:
    def __init__(self):
        self.project = GaeEnv.gcp_project
        self._cache = {}
        self.client = None

    def set_gcp_project(self, gcp_project):
        self.project = gcp_project

    def get_secret(self, secret_name, version="latest", gcp_project=None):
        if gcp_project is None:
            gcp_project = self.project
        if (
            self._cache.get(gcp_project)
            and self._cache.get(gcp_project).get(secret_name)
            and self._cache.get(gcp_project).get(secret_name).get(version)
        ):
            return self._cache.get(gcp_project).get(secret_name).get(version)

        if self.client is None:
            self.client = secretmanager.SecretManagerServiceClient()

        resource_name = self.client.secret_version_path(
            gcp_project, secret_name, version
        )
        res = self.client.access_secret_version(resource_name)
        secret_string = res.payload.data.decode("utf-8")

        if self._cache.get(gcp_project) is None:
            self._cache[gcp_project] = {secret_name: {version: secret_string}}
        elif self._cache.get(gcp_project).get(secret_name) is None:
            self._cache[gcp_project][secret_name] = {version: secret_string}
        else:
            self._cache[gcp_project][secret_name][version] = secret_string

        return self._cache.get(gcp_project).get(secret_name).get(version)

    def clear_cache(self):
        self._cache = {}


Secret = SecretHolder()
