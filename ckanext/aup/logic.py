def aup_changed(user_obj):
    """Return True if the Acceptable Use Policy has been updated

    This will return True if the Acceptable Use Policy was
    updated since the user last accepted the policy

    :rtype: bool
    """
    return False

def aup_update(user_obj):
    """Update users acceptance of the Acceptable Use Policy

    :rtype: bool
    """
    return True

def aup_clear(user_obj):
    """Clear users acceptance of the Acceptable Use Policy

    :rtype: bool
    """
    return False

def aup_revision(user_obj):
    """Return a string with the current Acceptable Use Policy revision

    :rtype: string
    """
    return ""
