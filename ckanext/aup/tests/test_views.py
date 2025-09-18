"""Tests for views.py."""

import pytest

import ckan.model as model
import ckan.tests.factories as factories
import ckan.tests.helpers as helpers
import ckan.plugins.toolkit as tk
import ckanext.aup.plugin as plugin


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
    def test_aup_update_accepted(self, app, reset_db):
        user = factories.User(
            plugin_extras={
                'acceptable_use_policy_revision': '41'
            }
        )
        user_token = factories.APIToken(user=user["id"])

        data = {
            "accept": "",
        }
        auth = {"Authorization": user_token["token"]}
        res = app.post(
            tk.h.url_for("aup.aup_update"),
            data=data,
            extra_environ=auth,
        )
        assert res.status_code == 200
        res_dict = json.loads(res.data)
        assert res_dict["success"] is False

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
    def test_aup_update_rejected(self, app, reset_db):
        user = factories.User(
            plugin_extras={
                'acceptable_use_policy_revision': '41'
            }
        )
        user_token = factories.APIToken(user=user["id"])

        data = {
            "reject": "",
        }
        auth = {"Authorization": user_token["token"]}
        res = app.post(
            tk.h.url_for("aup.aup_update"),
            data=data,
            extra_environ=auth,
        )
        assert res.status_code == 302
        assert res.headers[u'Location'] == tk.url_for(u'aup.aup_rejected', _external=True)
