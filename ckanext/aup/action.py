from __future__ import annotations

import ckan.plugins.toolkit as tk
import ckan.plugins as p
import ckanext.aup.interface as interface
from ckan import model
from ckan.logic import validate
from ckanext.toolbelt.decorators import Collector
from . import schema

action, get_actions = Collector().split()

def _get_userobj(context, data_dict):
    if data_dict.get('user_id'):
        return model.User.get(data_dict['user_id'])

    user = context.get('user', None)
    return model.User.get(user)

@action
@validate(schema.aup_update)
def aup_update(context, data_dict):
    # only update non-self user if admin
    # only to provided revision if admin
    tk.check_access("aup_update", context, data_dict)

    userobj = _get_userobj(context, data_dict)

    revision = None
    for impl in p.PluginImplementations(interface.IAcceptableUse):
        revision = impl.aup_published()

    revision = data_dict.get("revision", revision)

    update = False
    for impl in p.PluginImplementations(interface.IAcceptableUse):
        update = impl.aup_update(userobj,revision)
        if update:
            return update

    return update


@action
@tk.side_effect_free
@validate(schema.aup_revision)
def aup_revision(context, data_dict):
    # only non-self user if admin
    tk.check_access("aup_revision", context, data_dict)

    userobj = _get_userobj(context, data_dict)

    return


@action
@validate(schema.aup_clear)
def aup_clear(context, data_dict):
    # only update non-self user if admin
    tk.check_access("aup_clear", context, data_dict)

    userobj = _get_userobj(context, data_dict)

    return


@action
@tk.side_effect_free
@validate(schema.aup_published)
def aup_published(context, data_dict):
    tk.check_access("aup_published", context, data_dict)

    for impl in p.PluginImplementations(interface.IAcceptableUse):
        revision = impl.aup_published()
        if revision:
            return revision

    return ""
