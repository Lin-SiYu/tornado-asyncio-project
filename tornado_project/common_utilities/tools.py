import uuid


def get_uuid1():
    """ make a UUID based on the host ID and current time
    """
    s = uuid.uuid1()
    return str(s)