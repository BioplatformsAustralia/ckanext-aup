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
    aup_status = "unknown"

    try:
        form_dict = logic.clean_dict(
            dict_fns.unflatten(logic.tuplize_dict(logic.parse_params(request.form)))
        )

        if "reject" in form_dict:
            aup_status = "reject"
            return h.redirect_to(
                "aup.aup_rejected",
                return_to=form_dict.get("return_to", "home.index"),
                aup_status=aup_status,
            )

        if "accept" in form_dict:
            aup_status = "accept"

        if aup_status != "accept":
            return abort(401, _("Unknown AUP status"))

        data_dict = {
            # FIXME allow override by API call
            "user_name": g.userobj.name,
        }

        # Accept the AUP
        get_action("aup_update")(context, data_dict)

    except dict_fns.DataError:
        return abort(400, _("Integrity Error"))
    except NotAuthorized:
        message = _("Unauthorized")
        return abort(401, _(message))
    except NotFound as e:
        h.flash_error(_("User not found"))
        return h.redirect_to("home.index")
    except ValidationError as e:
        h.flash_error(e.error_summary)
        return h.redirect_to("home.index")
    else:
        h.flash_success(_("Acceptable Use Policy accepted"))

    return h.redirect_to(
        form_dict.get("return_to", "home.index"), aup_status=aup_status
    )


def aup_rejected():
    return render("ckanext_aup/aup_rejected.html")


def aup_published():
    return render("ckanext_aup/aup_view.html")


aup.add_url_rule("/aup/rejected", view_func=aup_rejected)
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
