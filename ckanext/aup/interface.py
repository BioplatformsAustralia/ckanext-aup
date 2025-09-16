from typing import Optional

import ckantoolkit as tk

import ckan.plugins.interfaces as interfaces


class IAcceptableUse(interfaces.Interface):
    def aup_changed(self, user_name):
        """Return True if the Acceptable Use Policy has been updated

        This will return True if the Acceptable Use Policy was
        updated since the user last accepted the policy

        :rtype: bool
        """
        return False

    def aup_update(self, user_name, revision):
        """Update users acceptance of the Acceptable Use Policy

        :rtype: bool
        """
        return True

    def aup_clear(self, user_name):
        """Clear users acceptance of the Acceptable Use Policy

        :rtype: bool
        """
        return False

    def aup_revision(self):
        """Return a string with the current Acceptable Use Policy revision for the user

        :rtype: string
        """
        return ""

    def aup_published(self):
        """Return a string with the current Acceptable Use Policy revision that is required

        :rtype: string
        """
        return ""

    def aup_required(self):
        """Return true if agreement to the AUP is required for that page

        :rtype: bool
        """

        return True
