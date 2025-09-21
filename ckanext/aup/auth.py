# coding: utf8
import ckan.plugins.toolkit as tk
import ckan.authz as authz
from ckan.common import g, _
from ckanext.toolbelt.decorators import Collector

from logging import getLogger

log = getLogger(__name__)

action, get_auth_functions = Collector().split()

def _is_logged_in():
    if tk.check_ckan_version(min_version='2.9'):
        return g.user
    else:
        return authz.auth_is_loggedin_user()


def _only_registered_user():
    if not _is_logged_in():
        return {'success': False, 'msg': _('User is not logged in')}
    return {'success': True}


def _only_self_for_field(data_dict, field):
    """Only allow access for self to resource"""
    if not _is_logged_in():
        return {'success': False, 'msg': _('User is not logged in')}

    if not g.userobj:
        return {'success': False}

    # user must be self to touch field
    if data_dict.get(field, None) and
        not (model.User.get(g.user).name == model.User.get(data_dict.get(field))):
        return {'success': False, 'msg': _('User must be self')}

    # fall through
    return {}


def _only_admin_user_for_field(data_dict, field):
    """ Only allowed to sysadmins or organization admins """
    if not _is_logged_in():
        return {'success': False, 'msg': _('User is not logged in')}

    if not g.userobj:
        return {'success': False}

    if authz.is_sysadmin(g.user):
        return {'success': True}

    # user must be a sysadmin to touch field
    if data_dict.get(field, None) and not authz.is_sysadmin(g.user):
        return {'success': False, 'msg': _('User must be a sysadmin')}

    # fall through
    return {}


def _only_self_or_admin_for_field(data_dict, field):
    result = _only_admin_user_for_field(data_dict, field)

    if result.get('success') == True:
        return result

    return result | _only_self_for_field(data_dict, field)


@action
def aup_changed(context, data_dict):
    # retreive user obj
    # only non-self user if admin

    return _only_registered_user() | _only_self_or_admin_for_field(data_dict, "user_id")


@action
def aup_update(context, data_dict):
    # retreive user obj
    # only update non-self user if admin
    # only to provided revision if admin

    return _only_registered_user() | _only_admin_user_for_field(data_dict, "revision") |  _only_self_or_admin_for_field(data_dict, "user_id")


@action
def aup_revision(context, data_dict):
    # retreive user obj
    # only non-self user if admin

    return _only_registered_user() | _only_self_or_admin_for_field(data_dict, "user_id")


@action
def aup_clear(context, data_dict):
    # retreive user obj
    # only update non-self user if admin

    return _only_registered_user() | _only_self_or_admin_for_field(data_dict, "user_id")


@action
@tk.auth_allow_anonymous_access
def aup_published(context, data_dict):
    return {"success": True}
