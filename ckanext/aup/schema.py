import ckan.plugins.toolkit as tk
from six import text_type

def aup_revision():
    #  user_id (string)
    not_empty = tk.get_validator("not_empty")
    ignore_missing = tk.get_validator("ignore_missing")
    user_id_or_name_exists = tk.get_validator("user_id_or_name_exists")
    convert_user_name_or_id_to_id = tk.get_validator("convert_user_name_or_id_to_id")

    return {
        "user_id": [
            ignore_missing,
            text_type,
            user_id_or_name_exists,
            convert_user_name_or_id_to_id,
        ],
    }


def aup_update():
    #  user_id (string)
    #  revision (string)
    not_empty = tk.get_validator("not_empty")
    ignore_missing = tk.get_validator("ignore_missing")
    user_id_or_name_exists = tk.get_validator("user_id_or_name_exists")
    convert_user_name_or_id_to_id = tk.get_validator("convert_user_name_or_id_to_id")

    return {
        "user_id": [
            ignore_missing,
            text_type,
            user_id_or_name_exists,
            convert_user_name_or_id_to_id,
        ],
        "revision": [
            ignore_missing,
            text_type,
        ],
    }


def aup_clear():
    #  user_id (string)
    #  package_id (string)
    #  valid_until (iso date string) - (optional)
    not_empty = tk.get_validator("not_empty")
    ignore_missing = tk.get_validator("ignore_missing")
    user_id_or_name_exists = tk.get_validator("user_id_or_name_exists")
    convert_user_name_or_id_to_id = tk.get_validator("convert_user_name_or_id_to_id")

    return {
        "user_id": [
            not_empty,
            text_type,
            user_id_or_name_exists,
            convert_user_name_or_id_to_id,
        ],
    }
