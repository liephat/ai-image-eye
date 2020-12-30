import shortuuid


def create_id():
    """
    Creates a non-sequential ID, e.g. 'LehoYzNiQhKh95wVcRQKvJ'.
    """
    return shortuuid.uuid()
