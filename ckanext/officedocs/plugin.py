import ckan.lib.helpers as h
import ckan.plugins as p
import ckan.plugins.toolkit as tk

from six.moves.urllib.parse import quote_plus


class OfficeDocsPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.IResourceView)

    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")
        tk.add_public_directory(config_, "public")
        tk.add_resource("fanstatic", "officedocs")

    def info(self):
        return {
            "name": "officedocs_view",
            "title": tk._("Office Previewer"),
            "default_title": tk._("Preview"),
            "icon": "compass",
            "always_available": True,
            "iframed": False,
        }

    def setup_template_variables(self, context, data_dict):
        url = quote_plus(data_dict["resource"]["url"])
        return {
            "resource_url": url
        }

    def can_view(self, data_dict):
        supported_formats = [
            "DOC", "DOCX", "XLS",
            "XLSX", "PPT", "PPTX",
            "PPS", "ODT", "ODS", "ODP"
        ]
        try:
            res = data_dict["resource"].get("format", "").upper()
            return res in supported_formats
        except:
            return False

    def view_template(self, context, data_dict):
        return "officedocs/preview.html"

    def form_template(self, context, data_dict):
        return "officedocs/form.html"
