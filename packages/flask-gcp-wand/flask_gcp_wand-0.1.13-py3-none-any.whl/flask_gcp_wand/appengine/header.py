from flask import request


class AppEngineHeader:
    GAE_PREFIX = "X-Appengine-"

    @property
    def user_ip(self):
        return request.headers.get(self.GAE_PREFIX + "User-Ip")

    @property
    def city(self):
        return request.headers.get(self.GAE_PREFIX + "City")

    @property
    def city_latlong(self):
        return request.headers.get(self.GAE_PREFIX + "Citylatlong")

    @property
    def country(self):
        return request.headers.get(self.GAE_PREFIX + "Country")

    @property
    def cloudscheduler(self):
        return request.headers.get("X-Cloudscheduler")

    @property
    def tasks_queue_name(self):
        return request.headers.get(self.GAE_PREFIX + "Queuename")

    @property
    def tasks_execution_count(self):
        return int(
            request.headers.get(self.GAE_PREFIX + "TaskExecutionCount", -1)
        )

    @property
    def user_id(self):
        return request.headers.get(self.GAE_PREFIX + "User-Id")

    @property
    def user_email(self):
        return request.headers.get(self.GAE_PREFIX + "User-Email")

    @property
    def user_is_admin(self):
        return request.headers.get(self.GAE_PREFIX + "User-Is-Admin")

    def _is_internal_ip(self):
        return self.user_ip in ("0.1.0.1", "0.1.0.2",)

    def is_cloudscheduler_request(self, ip_check=True):
        if ip_check and not self._is_internal_ip():
            return False
        value = self.cloudscheduler
        if not isinstance(value, str):
            return False
        return str.lower() == "true"

    def is_tasks_request(self, ip_check=True):
        if ip_check and not self._is_internal_ip():
            return False
        return self.tasks_queue_name is not None


GaeHeader = AppEngineHeader()
