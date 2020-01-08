from __future__ import absolute_import

import ckan.plugins as p
import ckan.plugins.toolkit as toolkit

from future import standard_library

standard_library.install_aliases()

from urllib import quote_plus


class OfficeDocsPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.IResourceView)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("fanstatic", "officedocs")

    def info(self):
        return {
            "name": "officedocs_view",
            "title": toolkit._("Office Previewer"),
            "default_title": toolkit._("Preview"),
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
        except KeyError:
            return False

    def view_template(self, context, data_dict):
        return "officedocs/preview.html"

    def form_template(self, context, data_dict):
        return "officedocs/form.html"
