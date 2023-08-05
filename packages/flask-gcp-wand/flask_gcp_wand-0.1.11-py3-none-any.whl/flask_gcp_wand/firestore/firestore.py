from google.cloud import firestore


_db_client = None


def get_db_client():
    """
    :return: google.cloud.firestore_v1.client.Client
    """
    global _db_client
    if not _db_client:
        _db_client = firestore.Client()
    return _db_client


def get_collection_reference(collection_path):
    """
    :param collection_path: str
    :return: google.cloud.firestore_v1.collection.CollectionReference
    """
    col_ref = get_db_client().collection(collection_path)
    return col_ref


def get_field_value_server_timestamp():
    return firestore.SERVER_TIMESTAMP
