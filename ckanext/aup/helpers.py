import ckan.plugins as p
import ckanext.aup.interface as interface
import ckan.plugins.toolkit as tk
import ckan.lib.dictization.model_dictize as model_dictize
from ckan.common import g


def _get_user_name(user_id):
    if not user_id:
        return g.userobj.name

    site_user = tk.get_action("get_site_user")({"ignore_auth": True}, {})["name"]
    admin_ctx = {"ignore_auth": True, "user": site_user}
    user_id = {"id": user_id, "include_plugin_extras": True}
    return tk.get_action("user_show")(admin_ctx, user_id).get("name", None)


def aup_changed(user_id=None):
    """Return True when the AUP has been changed"""

    user_name = _get_user_name(user_id)

    for impl in p.PluginImplementations(interface.IAcceptableUse):
        changed = impl.aup_changed(user_name)
        if changed:
            return True

    return False


def aup_revision(user_id=None):
    """Return the current revision of the AUP the user has agreed to or None"""

    user_name = _get_user_name(user_id)

    for impl in p.PluginImplementations(interface.IAcceptableUse):
        revision = impl.aup_revision(user_name)
        if revision:
            return revision

    return None


def aup_published():
    """Return the current revision of the AUP that the system is enforcing"""

    for impl in p.PluginImplementations(interface.IAcceptableUse):
        revision = impl.aup_published()
        if revision:
            return revision

    return ""


def aup_required():
    """Return true if agreement to the AUP is required for that page"""

    for impl in p.PluginImplementations(interface.IAcceptableUse):
        required = impl.aup_required()
        if required is not None:
            return required

    return True


def get_helpers():
    return {
        "aup_changed": aup_changed,
        "aup_revision": aup_revision,
        "aup_published": aup_published,
        "aup_required": aup_required,
    }
