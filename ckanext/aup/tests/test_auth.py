"""Tests for auth.py."""

import pytest

import ckan.tests.factories as factories
import ckan.tests.helpers as test_helpers
import ckan.model as model
import ckan.logic as logic
from ckan.common import g


@pytest.mark.ckan_config("ckanext.aup.policy_revision", "42")
@pytest.mark.ckan_config("ckan.plugins", "aup image_view")
@pytest.mark.usefixtures("with_request_context", "with_plugins", "clean_db")
class TestAUPAuth(object):
    def test_aup_changed_default(self):
        user = factories.User()
        # simulate logged in session
        userobj = model.User.by_name(user["name"])
        g.user = user["name"]
        g.userobj = userobj
        context = {"user": user["name"], "model": model}
        assert test_helpers.call_auth("aup_changed", context=context)

    def test_aup_changed_with_own_userid(self):
        user = factories.User()
        # simulate logged in session
        userobj = model.User.by_name(user["name"])
        g.user = user["name"]
        g.userobj = userobj
        context = {"user": user["name"], "model": model}
        assert test_helpers.call_auth(
            "aup_changed", context=context, user_id=user["name"]
        )

    def test_aup_changed_with_other_userid(self):
        user = factories.User()
        # simulate logged in session
        userobj = model.User.by_name(user["name"])
        g.user = user["name"]
        g.userobj = userobj
        user2 = factories.User()
        context = {"user": user["name"], "model": model}
        with pytest.raises(logic.NotAuthorized):
            assert test_helpers.call_auth(
                "aup_changed", context=context, user_id=user2["name"]
            )

    def test_aup_changed_sysadmin_with_other_userid(self):
        user = factories.User()
        sysadmin = factories.Sysadmin()
        userobj = model.User.by_name(sysadmin["name"])
        # simulate logged in session
        g.user = user["name"]
        g.userobj = userobj
        context = {"user": sysadmin["name"], "model": model}
        assert test_helpers.call_auth(
            "aup_changed", context=context, user_id=user["name"]
        )

    def test_aup_update_default(self):
        user = factories.User()
        # simulate logged in session
        userobj = model.User.by_name(user["name"])
        g.user = user["name"]
        g.userobj = userobj
        context = {"user": user["name"], "model": model}
        assert test_helpers.call_auth("aup_update", context=context)

    def test_aup_update_with_own_userid(self):
        user = factories.User()
        # simulate logged in session
        userobj = model.User.by_name(user["name"])
        g.user = user["name"]
        g.userobj = userobj
        context = {"user": user["name"], "model": model}
        assert test_helpers.call_auth(
            "aup_update", context=context, user_id=user["name"]
        )

    def test_aup_update_with_other_userid(self):
        user = factories.User()
        # simulate logged in session
        userobj = model.User.by_name(user["name"])
        g.user = user["name"]
        g.userobj = userobj
        user2 = factories.User()
        context = {"user": user["name"], "model": model}
        with pytest.raises(logic.NotAuthorized):
            assert test_helpers.call_auth(
                "aup_update", context=context, user_id=user2["name"]
            )

    def test_aup_update_sysadmin_with_other_userid(self):
        user = factories.User()
        sysadmin = factories.Sysadmin()
        userobj = model.User.by_name(sysadmin["name"])
        # simulate logged in session
        g.user = user["name"]
        g.userobj = userobj
        context = {"user": sysadmin["name"], "model": model}
        assert test_helpers.call_auth(
            "aup_update", context=context, user_id=user["name"]
        )

    def test_aup_update_revision_sysadmin(self):
        revision = "43"
        user = factories.User()
        sysadmin = factories.Sysadmin()
        userobj = model.User.by_name(sysadmin["name"])
        # simulate logged in session
        g.user = user["name"]
        g.userobj = userobj
        context = {"user": sysadmin["name"], "model": model}
        assert test_helpers.call_auth(
            "aup_update", context=context, user_id=user["name"], revision=revision
        )

    def test_aup_update_revision_non_sysadmin(self):
        revision = "43"
        user = factories.User()
        userobj = model.User.by_name(user["name"])
        # simulate logged in session
        g.user = user["name"]
        g.userobj = userobj
        context = {"user": user["name"], "model": model}
        with pytest.raises(logic.NotAuthorized):
            assert test_helpers.call_auth(
                "aup_update", context=context, user_id=user["name"], revision=revision
            )

    def test_aup_revision_default(self):
        user = factories.User()
        # simulate logged in session
        userobj = model.User.by_name(user["name"])
        g.user = user["name"]
        g.userobj = userobj
        context = {"user": user["name"], "model": model}
        assert test_helpers.call_auth("aup_revision", context=context)

    def test_aup_revision_with_own_userid(self):
        user = factories.User()
        # simulate logged in session
        userobj = model.User.by_name(user["name"])
        g.user = user["name"]
        g.userobj = userobj
        context = {"user": user["name"], "model": model}
        assert test_helpers.call_auth(
            "aup_revision", context=context, user_id=user["name"]
        )

    def test_aup_revision_with_other_userid(self):
        user = factories.User()
        # simulate logged in session
        userobj = model.User.by_name(user["name"])
        g.user = user["name"]
        g.userobj = userobj
        user2 = factories.User()
        context = {"user": user["name"], "model": model}
        with pytest.raises(logic.NotAuthorized):
            assert test_helpers.call_auth(
                "aup_revision", context=context, user_id=user2["name"]
            )

    def test_aup_revision_sysadmin_with_other_userid(self):
        user = factories.User()
        sysadmin = factories.Sysadmin()
        userobj = model.User.by_name(sysadmin["name"])
        # simulate logged in session
        g.user = user["name"]
        g.userobj = userobj
        context = {"user": sysadmin["name"], "model": model}
        assert test_helpers.call_auth(
            "aup_revision", context=context, user_id=user["name"]
        )

    def test_aup_clear_default(self):
        user = factories.User()
        # simulate logged in session
        userobj = model.User.by_name(user["name"])
        g.user = user["name"]
        g.userobj = userobj
        context = {"user": user["name"], "model": model}
        assert test_helpers.call_auth("aup_clear", context=context)

    def test_aup_clear_with_own_userid(self):
        user = factories.User()
        # simulate logged in session
        userobj = model.User.by_name(user["name"])
        g.user = user["name"]
        g.userobj = userobj
        context = {"user": user["name"], "model": model}
        assert test_helpers.call_auth(
            "aup_clear", context=context, user_id=user["name"]
        )

    def test_aup_clear_with_other_userid(self):
        user = factories.User()
        # simulate logged in session
        userobj = model.User.by_name(user["name"])
        g.user = user["name"]
        g.userobj = userobj
        user2 = factories.User()
        context = {"user": user["name"], "model": model}
        with pytest.raises(logic.NotAuthorized):
            assert test_helpers.call_auth(
                "aup_clear", context=context, user_id=user2["name"]
            )

    def test_aup_clear_sysadmin_with_other_userid(self):
        user = factories.User()
        sysadmin = factories.Sysadmin()
        userobj = model.User.by_name(sysadmin["name"])
        # simulate logged in session
        g.user = user["name"]
        g.userobj = userobj
        context = {"user": sysadmin["name"], "model": model}
        assert test_helpers.call_auth(
            "aup_clear", context=context, user_id=user["name"]
        )

    def test_aup_published(self):
        user = factories.User()
        context = {"user": user["name"], "model": model}
        assert test_helpers.call_auth("aup_published", context=context)

    def test_resource_show_aup_changed(self):
        user = factories.User()
        # simulate logged in session
        userobj = model.User.by_name(user["name"])
        g.user = user["name"]
        g.userobj = userobj
        context = {"user": user["name"], "model": model}
        with pytest.raises(logic.NotAuthorized):
            assert test_helpers.call_auth("resource_show", context=context)

    def test_resource_show_aup_not_changed(self):
        dataset = factories.Dataset()
        resource = factories.Resource(package_id=dataset["id"])

        user = factories.User(plugin_extras={"acceptable_use_policy_revision": "42"})
        # simulate logged in session
        userobj = model.User.by_name(user["name"])
        g.user = user["name"]
        g.userobj = userobj
        context = {"user": user["name"], "model": model}
        data_dict = {"id": resource["id"]}
        assert test_helpers.call_auth("resource_show", context=context, **data_dict)

    def test_resource_view_show_aup_changed(self):
        user = factories.User()
        # simulate logged in session
        userobj = model.User.by_name(user["name"])
        g.user = user["name"]
        g.userobj = userobj
        context = {"user": user["name"], "model": model}
        with pytest.raises(logic.NotAuthorized):
            assert test_helpers.call_auth("resource_view_show", context=context)

    def test_resource_view_show_aup_not_changed(self):
        resource_view = factories.ResourceView()

        user = factories.User(plugin_extras={"acceptable_use_policy_revision": "42"})
        # simulate logged in session
        userobj = model.User.by_name(user["name"])
        g.user = user["name"]
        g.userobj = userobj
        context = {"user": user["name"], "model": model}
        data_dict = {"id": resource_view["id"]}
        assert test_helpers.call_auth(
            "resource_view_show", context=context, **data_dict
        )
