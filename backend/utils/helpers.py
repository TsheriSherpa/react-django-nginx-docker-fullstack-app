""" Helper Functions """
from rest_framework import exceptions


def get_client_ip(request):
    """Get Client IP

    Arguments:
        request {dict}

    Returns:
        str
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        request_ip = x_forwarded_for.split(",")[0]
    else:
        request_ip = request.META.get("REMOTE_ADDR")
    return request_ip


def dict_key_exists(key, dictionary):
    """Find if key exists in dictionary

    Args:
        key (str): key to search in dict
        dictionary (dict): dictionary to search from
    """
    for dict_key in dictionary.keys():
        if dict_key == key:
            return True
    return False


def dict_get_value(key, dictionary):
    """Get key value from dictionary

    Args:
        key (str|int): key to get value for
        dictionary (dict): dict to search from
    """
    for dict_key in dictionary.keys():
        if dict_key == key:
            return dictionary.get(dict_key)
    return None


def get_error_message(serializer):
    """
    Get First Error From Serailizer Errors Dict

    Args:
        serializer {Serializer}
    Returns:
        erro {str}
    """
    key = list(serializer.errors.keys())[0]
    error = list(serializer.errors.values())[0][0]

    if type(error) is exceptions.ErrorDetail:
        error = str(list(serializer.errors.values())[0][0])

    while type(error) is not str:
        key = list(error.keys())[0]
        error = str(list(error.values())[0][0])

    return error.replace("This", key)
