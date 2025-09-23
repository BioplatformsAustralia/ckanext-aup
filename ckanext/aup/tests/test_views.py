"""Tests for views.py."""

import pytest
import logging

import ckan.model as model
import ckan.logic as logic
import ckan.tests.factories as factories
import ckan.tests.helpers as helpers
import ckan.plugins.toolkit as tk
import ckanext.aup.plugin as plugin

log = logging.getLogger(__name__)

@pytest.mark.ckan_config("ckan.plugins", "aup")
@pytest.mark.usefixtures("with_plugins")
def test_aup_rejected(app, reset_db):
    resp = app.get(tk.h.url_for("aup.aup_rejected"))
    assert resp.status_code == 200
    # look for phrase from rejection template
    assert (resp.body.find('has been rejected by the user') >= 0)

@pytest.mark.ckan_config("ckan.plugins", "aup")
@pytest.mark.usefixtures("with_plugins")
def test_aup_published(app, reset_db):
    resp = app.get(tk.h.url_for("aup.aup_published"))
    assert resp.status_code == 200
    # look for phrase from rejection template
    assert (resp.body.find('placeholder for where you should describe the Acceptable Use Policy') >= 0)


@pytest.mark.ckan_config("ckanext.aup.policy_revision", "42")
@pytest.mark.usefixtures("with_request_context")
@pytest.mark.ckan_config("ckan.plugins", "aup")
@pytest.mark.usefixtures("with_plugins")
class TestAUPViewsUpdates(object):
    @pytest.mark.usefixtures("clean_db")
    @pytest.mark.ckan_config('ckan.auth.create_default_api_keys', True)
    def test_aup_update_accepted(self, app, reset_db):
        user = factories.User(
            plugin_extras={
                'acceptable_use_policy_revision': '41'
            }
        )

        if tk.check_ckan_version(min_version='2.10'):
            user_token = factories.APIToken(user=user["id"])
            key = str(user_token["token"])
        else:
            key = user['apikey']

        data = {
            "accept": "",
        }
        auth = {"Authorization": key}
        res = app.post(
            tk.h.url_for("aup.aup_update"),
            data=data,
            headers=auth,
        )
        assert res.status_code == 200

        context = {
            'user': user['name'],
            "ignore_auth": True
            }
        result = helpers.call_action(
            "aup_revision",
            context=context,
        )

        assert(result == "42")

    @pytest.mark.usefixtures("clean_db")
    @pytest.mark.ckan_config('ckan.auth.create_default_api_keys', True)
    def test_aup_update_rejected(self, app, reset_db):
        user = factories.User(
            plugin_extras={
                'acceptable_use_policy_revision': '41'
            }
        )

        if tk.check_ckan_version(min_version='2.10'):
            user_token = factories.APIToken(user=user["id"])
            key = str(user_token["token"])
        else:
            key = user['apikey']

        data = {
            "reject": "",
        }
        auth = {"Authorization": key}
        res = app.post(
            tk.h.url_for("aup.aup_update"),
            data=data,
            headers=auth,
        )

        if tk.check_ckan_version(min_version='2.10'):
            path = res.request.path
        else:
            res.autocorrect_location_header = False
            path = res.headers['location']

        assert res.status_code == 200
        assert path == tk.url_for('aup.aup_rejected')

    @pytest.mark.usefixtures("clean_db")
    @pytest.mark.ckan_config('ckan.auth.create_default_api_keys', True)
    def test_aup_update_nostatus(self, app, reset_db):
        user = factories.User(
            plugin_extras={
                'acceptable_use_policy_revision': '41'
            }
        )

        if tk.check_ckan_version(min_version='2.10'):
            user_token = factories.APIToken(user=user["id"])
            key = str(user_token["token"])
        else:
            key = user['apikey']

        data = {}
        auth = {"Authorization": key}

        res = app.post(
            tk.h.url_for("aup.aup_update"),
            data=data,
            headers=auth,
        )

        assert res.status_code == 401

    @pytest.mark.usefixtures("clean_db")
    def test_aup_update_unauthorized(self, app, reset_db):
        user = factories.User()

        data = {}
        res = app.post(
            tk.h.url_for("aup.aup_update"),
            data=data,
        )

        assert res.status_code == 401
    
    @pytest.mark.usefixtures("clean_db")
    @pytest.mark.ckan_config('ckan.auth.create_default_api_keys', True)
    def test_aup_update_user_deleted(self, app, reset_db):
        sysadmin = factories.Sysadmin()
        user = factories.User(
            plugin_extras={
                'acceptable_use_policy_revision': '41'
            }
        )

        if tk.check_ckan_version(min_version='2.10'):
            user_token = factories.APIToken(user=user["id"])
            key = str(user_token["token"])
        else:
            key = user['apikey']

        data = {}
        auth = {"Authorization": key}

        context = {
            'user': sysadmin['name'],
            "ignore_auth": True
            }

        result = helpers.call_action(
            "user_delete",
            context=context,
            id=user["name"]
        )

        with pytest.raises(logic.NotFound):
            res = app.post(
                tk.h.url_for("aup.aup_update"),
                data=data,
                headers=auth,
            )
