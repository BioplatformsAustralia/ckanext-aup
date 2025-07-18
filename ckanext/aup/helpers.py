import ckan.plugins as p
import ckanext.aup.interface as interface
from ckan.common import c

def aup_changed():
    """Return True when the AUP has been changed"""

    for impl in p.PluginImplementations(interface.IAcceptableUse):
        changed = impl.aup_changed(c.userobj)
        if changed:
            return True

    return False


def get_helpers():
    return {
        "aup_changed": aup_changed,
    }
