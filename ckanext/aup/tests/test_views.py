"""Tests for views.py."""

import pytest

import ckanext.aup.validators as validators


import ckan.plugins.toolkit as tk


@pytest.mark.ckan_config("ckan.plugins", "aup")
@pytest.mark.usefixtures("with_plugins")
def test_aup_rejected(app, reset_db):
    resp = app.get(tk.h.url_for("aup.aup_rejected"))
    assert resp.status_code == 200
    # look for phrase from rejection template
    assert (resp.body.find('has been rejected by the user') >= 0)
