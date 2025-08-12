from __future__ import annotations

import ckan.plugins.toolkit as tk
from ckan.logic import validate
from ckanext.toolbelt.decorators import Collector
from . import schema

action, get_actions = Collector().split()


@action
@validate(schema.aup_update)
def aup_update(context, data_dict):
    tk.check_access("aup_update", context, data_dict)

    # retreive user obj
    # only update non-self user if admin
    # only to provided revision if admin

    return 


@action
@tk.side_effect_free
@validate(schema.aup_revision)
def aup_revision(context, data_dict):
    tk.check_access("aup_revision", context, data_dict)

    # retreive user obj
    # only non-self user if admin

    return


@action
@validate(schema.aup_clear)
def aup_clear(context, data_dict):
    tk.check_access("aup_clear", context, data_dict)

    # retreive user obj
    # only update non-self user if admin

    return


@action
@tk.side_effect_free
@validate(schema.aup_published)
def aup_published(context, data_dict):
    tk.check_access("aup_published", context, data_dict)

    return
