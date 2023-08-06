from flask import current_app


def retry(retry_count=3, give_up_exceptions=None):
    def _retry(func):
        def wrapper(*args, **kwargs):
            errors = []
            for i in range(retry_count):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if give_up_exceptions is not None and isinstance(
                        e, give_up_exceptions
                    ):
                        raise e
                    errors.append(e)
                    current_app.logger.warning(
                        f"Retrying by {e.__class__.__name__}: {e}"
                    )
            raise GaveUpRetryException.from_error_list(errors)

        return wrapper

    return _retry


class GaveUpRetryException(Exception):
    @staticmethod
    def from_error_list(errors):
        error_messages = [f"{e.__class__.__name__}: {str(e)}" for e in errors]
        return GaveUpRetryException("\n".join(error_messages))
