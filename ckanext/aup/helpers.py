import ckan.plugins as p
import ckanext.aup.interface as interface
from ckan.common import c

def aup_changed():
    """Return True when the AUP has been changed"""

    # FIXME handle user argument

    for impl in p.PluginImplementations(interface.IAcceptableUse):
        changed = impl.aup_changed(c.userobj)
        if changed:
            return True

    return False


def aup_revision():
    """Return the current revision of the AUP the user has agreed to or None"""

    # FIXME handle user argument

    for impl in p.PluginImplementations(interface.IAcceptableUse):
        revision = impl.aup_changed(c.userobj)
        if revision:
            return revision

    return None


def get_helpers():
    return {
        "aup_changed": aup_changed,
        "aup_revision": aup_revision,
    }
