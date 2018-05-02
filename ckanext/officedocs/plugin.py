import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


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
        from urllib import quote_plus
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
        try:
            return data_dict['resource'].get('format', '').upper() in supported_formats
        except:
            return False

    def view_template(self, context, data_dict):
        return "officedocs/preview.html"

    def form_template(self, context, data_dict):
        return "officedocs/form.html"
