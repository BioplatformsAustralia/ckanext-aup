import ckan.plugins.toolkit as tk
from ckan.common import g
from ckan import logic
from ckan.lib.base import request
from ckan.logic import NotFound


from logging import getLogger

logger = getLogger(__name__)

AUP_KEY="acceptable_use_policy_revision"

# FIXME Add config declarations
CONFIG_AUP_REVISION = "ckanext.aup.policy_revision"
CONFIG_AUP_REVISION_DEFAULT = "0.1"


def _get_user(user_name):
    if not user_name:
        raise NotFound

    user_id = { "id": user_name, "include_plugin_extras": True }
    user = tk.get_action('user_show')(_get_admin_ctx(), user_id)
    return user

def _get_admin_ctx():
    site_user = tk.get_action("get_site_user")({'ignore_auth': True}, {})["name"]
    admin_ctx = {"ignore_auth": True, "user": site_user }
    return admin_ctx

def _get_aup(user_name):
    user = _get_user(user_name)
    plugin_extras = _get_plugin_extras(user)
    return plugin_extras.get(AUP_KEY, None)

def _save_aup(user_name, revision):
    user = _get_user(user_name)
    plugin_extras = _get_plugin_extras(user)
    plugin_extras[AUP_KEY] = revision
    user['plugin_extras'] = plugin_extras
    tk.get_action('user_update')(_get_admin_ctx(), user)

def _get_plugin_extras(user):
    if 'plugin_extras' in user and user.get('plugin_extras') is not None:
        return user.get('plugin_extras')
    else:
        return {}


def aup_changed(user_name):
    """Return True if the Acceptable Use Policy has been updated

    This will return True if the Acceptable Use Policy was
    updated since the user last accepted the policy

    :rtype: bool
    """
    
    current_revision = tk.config.get(CONFIG_AUP_REVISION, CONFIG_AUP_REVISION_DEFAULT)
    user_revision = _get_aup(user_name)

    return user_revision != current_revision

def aup_update(user_name, revision=None):
    """Update users acceptance of the Acceptable Use Policy

    :rtype: bool
    """

    current_revision = tk.config.get(CONFIG_AUP_REVISION, CONFIG_AUP_REVISION_DEFAULT)

    update_to_revision = current_revision

    if revision:
        update_to_revision = revision

    _save_aup(user_name, update_to_revision)

    return True

def aup_clear(user_name):
    """Clear users acceptance of the Acceptable Use Policy

    :rtype: bool
    """

    _save_aup(user_name, "")

    return True

def aup_revision(user_name):
    """Return a string with the current Acceptable Use Policy revision for the user

    :rtype: string
    """

    user_revision = _get_aup(user_name)

    return '' if user_revision is None else str(user_revision)

def aup_published():
    """Return a string with the current Acceptable Use Policy revision that is required

    :rtype: string
    """
    current_revision = tk.config.get(CONFIG_AUP_REVISION, CONFIG_AUP_REVISION_DEFAULT)

    return current_revision

def aup_required():
    """Return true if agreement to the AUP is required for that page

    :rtype: bool
    """

    # exclude rejected AUP instructions
    if request.path.startswith('/aup/rejected'):
        return False

    return True
