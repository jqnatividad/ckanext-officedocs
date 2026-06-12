import ckan.plugins as p
from ckan.tests import factories

from ckanext.officedocs.plugin import (
    OfficeDocsPlugin,
    SUPPORTED_FORMATS_CONFIG,
    PRIVATE_FALLBACK_CONFIG,
    IFRAME_HEIGHT_CONFIG,
)


def test_view_on_resource_page():
    sysadmin = factories.Sysadmin()
    dataset = factories.Dataset()
    resource = factories.Resource(
        package_id = dataset['id'],
        url = 'http://link.to.some.data',
        format = 'XLS'
    )
    resource_view = factories.ResourceView(
        resource_id = resource['id'],
        title = 'Preview',
        view_type = 'officedocs_view'
    )

    response = p.toolkit.get_action('resource_view_show')(
        {'user': sysadmin.get('name')},
        {'id': resource_view.get('id')}
    )

    assert response.get('title') == 'Preview'
    assert response.get('view_type') == 'officedocs_view'


def test_can_view_uses_default_supported_formats(monkeypatch, ckan_config):
    monkeypatch.delitem(
        ckan_config, SUPPORTED_FORMATS_CONFIG, raising=False
    )

    assert OfficeDocsPlugin().can_view({
        "package": {"private": False},
        "resource": {"format": "docx"},
    })


def test_can_view_uses_configured_supported_formats(
    monkeypatch, ckan_config
):
    monkeypatch.setitem(
        ckan_config,
        SUPPORTED_FORMATS_CONFIG,
        "docm xlsm PPTM ppsm",
    )
    plugin = OfficeDocsPlugin()

    assert plugin.can_view({
        "package": {"private": False},
        "resource": {"format": "DoCm"},
    })
    assert not plugin.can_view({
        "package": {"private": False},
        "resource": {"format": "DOCX"},
    })


def test_can_view_public_supported_format(monkeypatch, ckan_config):
    monkeypatch.delitem(
        ckan_config, PRIVATE_FALLBACK_CONFIG, raising=False
    )

    assert OfficeDocsPlugin().can_view({
        "package": {"private": False},
        "resource": {"format": "docx"},
    })


def test_can_view_private_blocked_by_default(monkeypatch, ckan_config):
    monkeypatch.delitem(
        ckan_config, PRIVATE_FALLBACK_CONFIG, raising=False
    )

    assert not OfficeDocsPlugin().can_view({
        "package": {"private": True},
        "resource": {"format": "docx"},
    })


def test_can_view_private_allowed_when_fallback_enabled(
    monkeypatch, ckan_config
):
    monkeypatch.setitem(
        ckan_config, PRIVATE_FALLBACK_CONFIG, "true"
    )

    assert OfficeDocsPlugin().can_view({
        "package": {"private": True},
        "resource": {"format": "docx"},
    })


def test_can_view_private_fallback_still_checks_format(
    monkeypatch, ckan_config
):
    monkeypatch.setitem(
        ckan_config, PRIVATE_FALLBACK_CONFIG, "true"
    )

    assert not OfficeDocsPlugin().can_view({
        "package": {"private": True},
        "resource": {"format": "pdf"},
    })


def test_setup_template_variables_encodes_url_and_sets_flags(ckan_config):
    result = OfficeDocsPlugin().setup_template_variables({}, {
        "resource": {"url": "http://example.com/my doc.docx"},
        "package": {"private": True},
    })

    assert result["resource_url"] == "http%3A%2F%2Fexample.com%2Fmy+doc.docx"
    assert result["resource_download_url"] == "http://example.com/my doc.docx"
    assert result["private_package"] is True


def test_setup_template_variables_handles_missing_keys(ckan_config):
    result = OfficeDocsPlugin().setup_template_variables({}, {})

    assert result["resource_url"] == ""
    assert result["resource_download_url"] == ""
    assert result["private_package"] is False


def test_setup_template_variables_iframe_height_default(
    monkeypatch, ckan_config
):
    monkeypatch.delitem(ckan_config, IFRAME_HEIGHT_CONFIG, raising=False)

    result = OfficeDocsPlugin().setup_template_variables({}, {})

    assert result["iframe_height"] == "400px"


def test_setup_template_variables_iframe_height_configured(
    monkeypatch, ckan_config
):
    monkeypatch.setitem(ckan_config, IFRAME_HEIGHT_CONFIG, "75vh")

    result = OfficeDocsPlugin().setup_template_variables({}, {})

    assert result["iframe_height"] == "75vh"
