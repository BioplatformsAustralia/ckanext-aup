"""Tests for auth.py."""

import pytest

import ckan.tests.factories as factories
import ckan.tests.helpers as test_helpers
import ckan.model as model

@pytest.mark.ckan_config("ckanext.aup.policy_revision", "42")
@pytest.mark.ckan_config("ckan.plugins", "aup")
@pytest.mark.usefixtures("with_request_context", "with_plugins", "clean_db")
class TestAUPAuth(object):
    def test_aup_changed_default(self):
        user = factories.User()
        context = {"user": user["name"], "model": model}
        assert test_helpers.call_auth("aup_changed", context=context)

    def test_aup_changed_with_own_userid(self):
        user = factories.User()
        context = {"user": user["name"], "model": model}
        assert test_helpers.call_auth("aup_changed", context=context, user_id=user["name"])

    def test_aup_changed_with_other_userid(self):
        user = factories.User()
        user2 = factories.User()
        context = {"user": user["name"], "model": model}
        with pytest.raises(logic.NotAuthorized):
           assert test_helpers.call_auth("aup_changed", context=context, user_id=user2["name"])

    def test_aup_changed_sysadmin_with_other_userid(self):
        user = factories.User()
        sysadmin = factories.Sysadmin()
        context = {"user": sysadmin["name"], "model": model}
        assert test_helpers.call_auth("aup_changed", context=context, user_id=user["name"])

    def test_aup_update_default(self):
        user = factories.User()
        context = {"user": user["name"], "model": model}
        assert test_helpers.call_auth("aup_update", context=context)

    def test_aup_update_with_own_userid(self):
        user = factories.User()
        context = {"user": user["name"], "model": model}
        assert test_helpers.call_auth("aup_update", context=context, user_id=user["name"])

    def test_aup_update_with_other_userid(self):
        user = factories.User()
        user2 = factories.User()
        context = {"user": user["name"], "model": model}
        with pytest.raises(logic.NotAuthorized):
           assert test_helpers.call_auth("aup_update", context=context, user_id=user2["name"])
    
    def test_aup_update_sysadmin_with_other_userid(self):
        user = factories.User()
        sysadmin = factories.Sysadmin()
        context = {"user": sysadmin["name"], "model": model}
        assert test_helpers.call_auth("aup_update", context=context, user_id=user["name"])

    def test_aup_revision_default(self):
        user = factories.User()
        context = {"user": user["name"], "model": model}
        assert test_helpers.call_auth("aup_revision", context=context)

    def test_aup_revision_with_own_userid(self):
        user = factories.User()
        context = {"user": user["name"], "model": model}
        assert test_helpers.call_auth("aup_revision", context=context, user_id=user["name"])

    def test_aup_revision_with_other_userid(self):
        user = factories.User()
        user2 = factories.User()
        context = {"user": user["name"], "model": model}
        with pytest.raises(logic.NotAuthorized):
           assert test_helpers.call_auth("aup_revision", context=context, user_id=user2["name"])

    def test_aup_revision_sysadmin_with_other_userid(self):
        user = factories.User()
        sysadmin = factories.Sysadmin()
        context = {"user": sysadmin["name"], "model": model}
        assert test_helpers.call_auth("aup_revision", context=context, user_id=user["name"])

    def test_aup_clear_default(self):
        user = factories.User()
        context = {"user": user["name"], "model": model}
        assert test_helpers.call_auth("aup_clear", context=context)

    def test_aup_clear_with_own_userid(self):
        user = factories.User()
        context = {"user": user["name"], "model": model}
        assert test_helpers.call_auth("aup_clear", context=context, user_id=user["name"])

    def test_aup_clear_with_other_userid(self):
        user = factories.User()
        user2 = factories.User()
        context = {"user": user["name"], "model": model}
        with pytest.raises(logic.NotAuthorized):
           assert test_helpers.call_auth("aup_clear", context=context, user_id=user2["name"])
    
    def test_aup_clear_sysadmin_with_other_userid(self):
        user = factories.User()
        sysadmin = factories.Sysadmin()
        context = {"user": sysadmin["name"], "model": model}
        assert test_helpers.call_auth("aup_clear", context=context, user_id=user["name"])
    
    def test_aup_published(self):
        user = factories.User()
        context = {"user": user["name"], "model": model}
        assert test_helpers.call_auth("aup_published", context=context)
