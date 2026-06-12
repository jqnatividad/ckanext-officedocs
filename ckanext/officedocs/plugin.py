import ckan.plugins as p
import ckan.plugins.toolkit as tk

from urllib.parse import quote_plus


SUPPORTED_FORMATS_CONFIG = "ckanext.officedocs.supported_formats"
DEFAULT_SUPPORTED_FORMATS = (
    "DOC DOCX XLS XLSX XLSB PPT PPTX PPS PPSX ODT ODS ODP"
)

PRIVATE_FALLBACK_CONFIG = "ckanext.officedocs.enable_private_fallback"
DEFAULT_PRIVATE_FALLBACK = False

IFRAME_HEIGHT_CONFIG = "ckanext.officedocs.iframe_height"
DEFAULT_IFRAME_HEIGHT = "400px"


def get_supported_formats():
    value = tk.config.get(
        SUPPORTED_FORMATS_CONFIG, DEFAULT_SUPPORTED_FORMATS
    )
    return [
        format_.upper()
        for format_ in tk.aslist(value)
    ]


def private_fallback_enabled():
    return tk.asbool(
        tk.config.get(PRIVATE_FALLBACK_CONFIG, DEFAULT_PRIVATE_FALLBACK)
    )


def get_iframe_height():
    return tk.config.get(IFRAME_HEIGHT_CONFIG, DEFAULT_IFRAME_HEIGHT)


@tk.blanket.config_declarations
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
        resource = data_dict.get("resource", {})
        package = data_dict.get("package", {})
        resource_url = resource.get("url", "")
        return {
            "resource_url": quote_plus(resource_url),
            "resource_download_url": resource_url,
            "private_package": package.get("private", False),
            "iframe_height": get_iframe_height(),
        }

    def can_view(self, data_dict):
        try:
            res = data_dict.get("resource", {}).get("format", "").upper()
            if res not in get_supported_formats():
                return False
            pkg_private = data_dict.get("package", {}).get("private", False)
            if pkg_private:
                return private_fallback_enabled()
            return True
        except Exception:
            return False

    def view_template(self, context, data_dict):
        return "officedocs/preview.html"

    def form_template(self, context, data_dict):
        return "officedocs/form.html"
