import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.aup.logic as logic
import ckanext.aup.action as action


class AupPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IActions)
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

    def aup_changed(self, user_obj):
        return logic.aup_changed(user_obj)

    def aup_update(self, user_obj):
        return logic.aup_update(user_obj)

    def aup_clear(self, user_obj):
        return logic.aup_clear(user_obj)

    def aup_revision(self, user_obj):
        return logic.aup_revision(user_obj)

    # IActions

    def get_actions(self):
        return action.get_actions()
