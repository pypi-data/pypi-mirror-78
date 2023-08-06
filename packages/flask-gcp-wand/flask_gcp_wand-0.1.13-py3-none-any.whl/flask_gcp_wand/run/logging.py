import logging
import os
import json
from datetime import datetime, timezone, timedelta

from flask import request


class CloudRunLogRecord(logging.LogRecord):
    def __init__(self, name, level, pathname, lineno,
                 msg, args, exc_info, func=None, sinfo=None, **kwargs):
        super().__init__(name, level, pathname, lineno,
                         msg, args, exc_info, func, sinfo, **kwargs)
        self.tz = timezone(timedelta(hours=int(os.getenv('WAND_TD_HOUR', 0))))

    def getMessage(self):
        msg = super().getMessage()
        global_log_fields = {}

        try:
            project = os.getenv('WAND_GCP_PROJECT')
            trace_header = request.headers.get('X-Cloud-Trace-Context')
            if trace_header and project:
                trace = trace_header.split('/')
                global_log_fields['logging.googleapis.com/trace'] = (
                    f"projects/{project}/traces/{trace[0]}")
        except Exception:
            pass

        now = datetime.now(self.tz).isoformat()

        entry = dict(severity=self.levelname,
                     message=msg,
                     time=now,
                     **global_log_fields)

        return json.dumps(entry)


def setup_logging_cloudrun(log_set_level=None):
    if log_set_level is None:
        log_set_level = logging.DEBUG
    logging.basicConfig(format="%(message)s")
    logging.setLogRecordFactory(CloudRunLogRecord)
    logging.getLogger().setLevel(log_set_level)
