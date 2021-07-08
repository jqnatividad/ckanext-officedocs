import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from six.moves.urllib.parse import quote_plus


class OfficeDocsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IResourceView)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'officedocs')

    def info(self):
        return {
            "name": "officedocs_view",
            "title": toolkit._('Office Previewer'),
            "default_title": toolkit._('Preview'),
            "icon": "compass",
            "always_available": True,
            "iframed": False,
        }

    def setup_template_variables(self, context, data_dict):
        url = quote_plus(data_dict["resource"]["url"])
        private_package = data_dict["package"]["private"]
        return {
            "resource_url": url,
            "private_package": private_package
        }

    def can_view(self, data_dict):
        supported_formats = [
            "DOC", "DOCX", "XLS", "XLSX", "PPT", "PPTX", "PPS", "ODT", "ODS", "ODP"
        ]
        format_upper = data_dict['resource'].get('format', '').upper()
        if format_upper in supported_formats:
            return True
        return False

    def view_template(self, context, data_dict):
        return "officedocs/preview.html"

    def form_template(self, context, data_dict):
        return "officedocs/form.html"
