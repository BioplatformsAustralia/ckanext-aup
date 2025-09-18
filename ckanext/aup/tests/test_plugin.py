"""
Tests for plugin.py.

Tests are written using the pytest library (https://docs.pytest.org), and you
should read the testing guidelines in the CKAN docs:
https://docs.ckan.org/en/2.9/contributing/testing.html

To write tests for your extension you should install the pytest-ckan package:

    pip install pytest-ckan

This will allow you to use CKAN specific fixtures on your tests.

For instance, if your test involves database access you can use `clean_db` to
reset the database:

    import pytest

    from ckan.tests import factories

    @pytest.mark.usefixtures("clean_db")
    def test_some_action():

        dataset = factories.Dataset()

        # ...

For functional tests that involve requests to the application, you can use the
`app` fixture:

    from ckan.plugins import toolkit

    def test_some_endpoint(app):

        url = toolkit.url_for('myblueprint.some_endpoint')

        response = app.get(url)

        assert response.status_code == 200


To temporary patch the CKAN configuration for the duration of a test you can use:

    import pytest

    @pytest.mark.ckan_config("ckanext.myext.some_key", "some_value")
    def test_some_action():
        pass
"""
import pytest

import ckan.model as model
import ckan.tests.factories as factories
import ckan.tests.helpers as helpers
import ckan.plugins.toolkit as tk
import ckanext.aup.plugin as plugin

from ckan.plugins import plugin_loaded


@pytest.mark.ckan_config("ckan.plugins", "aup")
@pytest.mark.usefixtures("with_plugins")
def test_plugin():
    assert plugin_loaded("aup")


@pytest.mark.ckan_config("ckanext.aup.policy_revision", "42")
@pytest.mark.ckan_config("ckan.plugins", "aup")
@pytest.mark.usefixtures("with_plugins")
class TestAUPPlugin(object):
    @pytest.mark.usefixtures("clean_db")
    def test_aup_changed(self):
        user = factories.User(
        #    plugin_extras={
        #        'acceptable_use_policy_revision': '41'
        #    }
        )

        context = {
            'user': user,
            "ignore_auth": True
            }
        result = helpers.call_action(
            "aup_changed",
            context=context,
        )

        assert(result == True)

        user2 = factories.User(
        #    plugin_extras={
        #        'acceptable_use_policy_revision': '42'
        #    }
        )

        context = {
            'user': user2,
            "ignore_auth": True
            }
        result = helpers.call_action(
            "aup_changed",
            context=context,
        )

        assert(result == False)


    def test_aup_update_default(self):
        pass

    def test_aup_update_specific(self):
        pass

    def test_aup_clear(self):
        pass

    def test_aup_revision(self):
        pass

    def test_aup_published(self):
        result = helpers.call_action(
            "aup_published"
        )

        assert(result == "42")

    def test_aup_required(self):
        pass
