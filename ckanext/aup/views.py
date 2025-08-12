from flask import Blueprint
from ckan.common import _, g
from ckan.lib.base import render, abort, request
from ckan.logic import get_action, ValidationError, NotFound, NotAuthorized
import ckan.logic as logic
import ckan.lib.helpers as h
import ckan.lib.navl.dictization_functions as dict_fns

from logging import getLogger

logger = getLogger(__name__)

aup = Blueprint("aup", __name__)


def aup_update():
    context = {"user": g.user}

    try:
        form_dict = logic.clean_dict(
            dict_fns.unflatten(logic.tuplize_dict(logic.parse_params(request.form)))
        )

        # FIXME check for accept value
        logger.warn(form_dict)

        data_dict = {
            # FIXME allow override by API call
            "user_id": g.userobj.id,
        }

        # Accept the AUP
        get_action("aup_update")(context, data_dict)

    except dict_fns.DataError:
        return abort(400, _("Integrity Error"))
    except NotAuthorized:
        message = _("Unauthorized to create pass {}").format(id)
        return abort(401, _(message))
    except NotFound as e:
        h.flash_error(_("User not found"))
        return h.redirect_to(u'home.index')
    except ValidationError as e:
        h.flash_error(e.error_summary)
        return h.redirect_to(u'home.index')
    else:
        h.flash_success(_("Acceptable Use Policy accepted"))

    return h.redirect_to(form_dict.get("return_to", u'home.index'))


def aup_published():
    return render(
        "ckanext_aup/aup_view.html"
    )

aup.add_url_rule("/about/acceptable_use", view_func=aup_published)

aup.add_url_rule(
    rule="/aup/update",
    view_func=aup_update,
    methods=[
        "POST",
    ],
)


def get_blueprints():
    return [aup]
