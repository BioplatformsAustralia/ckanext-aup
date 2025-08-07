import ckan.plugins as p
import ckanext.aup.interface as interface
from ckan.common import c

def aup_changed(user=None):
    """Return True when the AUP has been changed"""

    if not user:
        user = c.userobj

    for impl in p.PluginImplementations(interface.IAcceptableUse):
        changed = impl.aup_changed(user)
        if changed:
            return True

    return False


def aup_revision(user=None):
    """Return the current revision of the AUP the user has agreed to or None"""

    if not user:
        user = c.userobj

    for impl in p.PluginImplementations(interface.IAcceptableUse):
        revision = impl.aup_changed(user)
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


def get_helpers():
    return {
        "aup_changed": aup_changed,
        "aup_revision": aup_revision,
        "aup_published": aup_published,
    }
