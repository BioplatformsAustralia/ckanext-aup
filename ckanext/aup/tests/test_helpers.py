"""Tests for helpers.py."""

import pytest
import logging
import ckan.tests.factories as factories
import ckan.plugins.toolkit as tk
import ckanext.aup.helpers as aup_helpers
import ckan.model as model
from ckan.common import g

log = logging.getLogger(__name__)


@pytest.mark.ckan_config("ckanext.aup.policy_revision", "42")
@pytest.mark.ckan_config("ckan.plugins", "aup")
@pytest.mark.usefixtures("with_plugins", "with_request_context")
class TestAUPHelpers(object):
    def test_aup_changed_default(self):
        user = factories.User(
            plugin_extras={
                'acceptable_use_policy_revision': '41'
            }
        )

        userobj = model.User.by_name(user["name"])

        log.info(user)
        log.info(userobj)

        g.user = user["name"]
        g.userobj = userobj

        assert aup_helpers.aup_changed() == True

        user2 = factories.User(
            plugin_extras={
                'acceptable_use_policy_revision': '42'
            }
        )

        user2obj = model.User.by_name(user2["name"])

        g.user = user2["name"]
        g.userobj = user2obj

        assert aup_helpers.aup_changed() == False

    @pytest.mark.usefixtures("clean_db")
    def test_aup_changed_user_id(self):
        user = factories.User(
            plugin_extras={
                'acceptable_use_policy_revision': '41'
            }
        )

        assert aup_helpers.aup_changed(user["name"]) == True

        user2 = factories.User(
            plugin_extras={
                'acceptable_use_policy_revision': '42'
            }
        )

        assert aup_helpers.aup_changed(user2["name"]) == False

    @pytest.mark.usefixtures("clean_db")
    def test_aup_revision_default(self):
        user = factories.User(
            plugin_extras={
                'acceptable_use_policy_revision': '3.11'
            }
        )

        userobj = model.User.by_name(user["name"])

        g.user = user["name"]
        g.userobj = userobj
        
        assert aup_helpers.aup_revision() == "3.11"

    @pytest.mark.usefixtures("clean_db")
    def test_aup_revision_user_id(self):
        user = factories.User()

        user2 = factories.User(
            plugin_extras={
                'acceptable_use_policy_revision': '3.11'
            }
        )

        assert aup_helpers.aup_revision(user_id=user2['name']) == "3.11"



    def test_aup_published(self):
        assert aup_helpers.aup_published() == "42"

    def test_aup_required(self,app):
        required = [
            tk.url_for('home.index'),
            tk.url_for('home.about'),
            tk.url_for('dataset.search'),
        ]

        not_required = [
            tk.url_for('aup.aup_rejected'),
        ]

        for path in required:
            with app.flask_app.test_request_context(path):
                assert aup_helpers.aup_required() == True

        for path in not_required:
            with app.flask_app.test_request_context(path):
                assert aup_helpers.aup_required() == False

    def test_get_helpers(self):
        assert "aup_changed" in aup_helpers.get_helpers()
        assert "aup_revision" in aup_helpers.get_helpers()
        assert "aup_required" in aup_helpers.get_helpers()
        assert "aup_published" in aup_helpers.get_helpers()
