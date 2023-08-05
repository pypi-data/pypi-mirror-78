import os


class AppEngineEnv:
    @property
    def gae_instance(self):
        return os.getenv("GAE_INSTANCE")

    @property
    def gae_runtime(self):
        return os.getenv("GAE_RUNTIME")

    @property
    def gae_service(self):
        return os.getenv("GAE_SERVICE")

    @property
    def gae_version(self):
        return os.getenv("GAE_VERSION")

    @property
    def gae_application(self):
        return os.getenv("GAE_APPLICATION")

    @property
    def gae_deployment_id(self):
        return os.getenv("GAE_DEPLOYMENT_ID")

    @property
    def gae_env(self):
        return os.getenv("GAE_ENV")

    @property
    def gae_memory(self):
        return os.getenv("GAE_MEMORY_MB")

    @property
    def gcp_project(self):
        return os.getenv("GOOGLE_CLOUD_PROJECT")

    @property
    def server_software(self):
        return os.getenv("SERVER_SOFTWARE")

    @property
    def lc_ctype(self):
        return os.getenv("LC_CTYPE")

    def is_gae(self):
        return self.gae_instance is not None


GaeEnv = AppEngineEnv()
