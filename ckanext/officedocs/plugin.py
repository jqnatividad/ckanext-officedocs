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
            "icon": "windows",
            "always_available": False,
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
            "XLSX", "XLSB", "PPT", "PPTX",
            "PPS", "PPSX", "ODT", "ODS", "ODP"
        ]
        try:
            pkg_private = data_dict.get("package",{}).get("private", False)
            if not pkg_private:
                res = data_dict.get("resource",{}).get("format", "").upper()
                return res in supported_formats
            else:
                return False
        except Exception:
            return False

    def view_template(self, context, data_dict):
        return "officedocs/preview.html"

    def form_template(self, context, data_dict):
        return "officedocs/form.html"
