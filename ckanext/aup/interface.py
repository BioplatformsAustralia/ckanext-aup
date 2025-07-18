from typing import Optional

import ckantoolkit as tk

import ckan.plugins.interfaces as interfaces


class IAcceptableUse(interfaces.Interface):
    def aup_changed(self, user_obj):
        """Return True if the Acceptable Use Policy has been updated

        This will return True if the Acceptable Use Policy was
        updated since the user last accepted the policy

        :rtype: bool
        """
        return False

    def aup_update(self, user_obj):
        """Update users acceptance of the Acceptable Use Policy

        :rtype: bool
        """
        return True

    def aup_clear(self, user_obj):
        """Clear users acceptance of the Acceptable Use Policy

        :rtype: bool
        """
        return False

    def aup_revision(self):
        """Return a string with the current Acceptable Use Policy revision

        :rtype: string
        """
        return ""
