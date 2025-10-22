import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.aup.logic as logic
import ckanext.aup.action as action
import ckanext.aup.views as views
import ckanext.aup.interface as interface
import ckanext.aup.helpers as helpers
import ckanext.aup.auth as auth

from logging import getLogger

logger = getLogger(__name__)


class AupPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(interface.IAcceptableUse, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "aup")

    # ITemplateHelpers

    def get_helpers(self):
        return helpers.get_helpers()

    # IAcceptableUse

    def aup_changed(self, user_name):
        return logic.aup_changed(user_name)

    def aup_update(self, user_name, revision):
        return logic.aup_update(user_name, revision)

    def aup_clear(self, user_name):
        return logic.aup_clear(user_name)

    def aup_revision(self, user_name):
        return logic.aup_revision(user_name)

    def aup_published(self):
        return logic.aup_published()

    def aup_required(self):
        return logic.aup_required()

    # IActions

    def get_actions(self):
        return action.get_actions()

    # IAuthFunctions

    def get_auth_functions(self):
        return auth.get_auth_functions()

    # IBlueprint

    def get_blueprint(self):
        return views.get_blueprints()
