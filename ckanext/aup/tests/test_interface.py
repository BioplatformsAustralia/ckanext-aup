"""
Tests for interface.py.
"""
import pytest

import ckan.tests.factories as factories
import ckanext.aup.interface as interface


class TestAUPInterface(object):
    def test_aup_changed(self):
        aup = interface.IAcceptableUse()

        user = factories.User(
            plugin_extras={
                'acceptable_use_policy_revision': '41'
            }
        )

        result = aup.aup_changed(user["name"])

        assert(result == False)

    def test_aup_update(self):
        aup = interface.IAcceptableUse()

        user = factories.User(
            plugin_extras={
                'acceptable_use_policy_revision': '41'
            }
        )

        result = aup.aup_update(user["name"],"42")

        assert(result == True)

    def test_aup_clear(self):
        aup = interface.IAcceptableUse()

        user = factories.User(
            plugin_extras={
                'acceptable_use_policy_revision': '3.11'
            }
        )

        result = aup.aup_clear(user["name"])

        assert(result == False)

    def test_aup_revision(self):
        aup = interface.IAcceptableUse()

        result = aup.aup_revision()

        assert(result == "")

    def test_aup_published(self):
        aup = interface.IAcceptableUse()

        result = aup.aup_published()

        assert(result == "")

    def test_aup_required(self):
        aup = interface.IAcceptableUse()

        result = aup.aup_required()

        assert(result == True)
