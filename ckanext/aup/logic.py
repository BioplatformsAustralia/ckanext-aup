import ckan.plugins.toolkit as tk
from ckan.common import g

AUP_KEY="acceptable_use_policy_revision"

# FIXME Add config declarations
CONFIG_AUP_REVISION = "ckanext.aup.policy_revision"
CONFIG_AUP_REVISION_DEFAULT = "0.1"

def _get_user(user_obj):
    # Default to own user
    username = user_obj.name

    user_id = { "id": username, "include_plugin_extras": True }
    user = tk.get_action('user_show')(_get_admin_ctx(), user_id)
    return user

def _get_admin_ctx():
    site_user = tk.get_action("get_site_user")({'ignore_auth': True}, {})["name"]
    admin_ctx = {"ignore_auth": True, "user": site_user }
    return admin_ctx

def _get_aup(user_obj):
    user = _get_user(user_obj)
    plugin_extras = _get_plugin_extras(user)
    return plugin_extras.get(AUP_KEY, None)

def _save_aup(user_obj, revision):
    user = _get_user(user_obj)
    plugin_extras = _get_plugin_extras(user)
    plugin_extras[AUP_KEY] = revision
    user['plugin_extras'] = plugin_extras
    tk.get_action('user_update')(_get_admin_ctx(), user)

def _get_plugin_extras(user):
    if 'plugin_extras' in user and user.get('plugin_extras') is not None:
        return user.get('plugin_extras')
    else:
        return {}


def aup_changed(user_obj):
    """Return True if the Acceptable Use Policy has been updated

    This will return True if the Acceptable Use Policy was
    updated since the user last accepted the policy

    :rtype: bool
    """
    
    current_revision = tk.config.get(CONFIG_AUP_REVISION, CONFIG_AUP_REVISION_DEFAULT)
    user_revision = _get_aup(user_obj)

    return user_revision != current_revision

def aup_update(user_obj):
    """Update users acceptance of the Acceptable Use Policy

    :rtype: bool
    """

    current_revision = tk.config.get(CONFIG_AUP_REVISION, CONFIG_AUP_REVISION_DEFAULT)
    _save_aup(user_obj, current_revision)

    return True

def aup_clear(user_obj):
    """Clear users acceptance of the Acceptable Use Policy

    :rtype: bool
    """

    _save_aup(user_obj, "")

    return True

def aup_revision(user_obj):
    """Return a string with the current Acceptable Use Policy revision

    :rtype: string
    """

    user_revision = _get_aup(user_obj)

    return '' if user_revision is None else str(user_revision)

def aup_published():
    """Return a string with the current Acceptable Use Policy revision that is required

    :rtype: string
    """
    current_revision = tk.config.get(CONFIG_AUP_REVISION, CONFIG_AUP_REVISION_DEFAULT)

    return current_revision
