import ckan.plugins as p
from ckan.tests import factories

from ckanext.officedocs.plugin import (
    OfficeDocsPlugin,
    SUPPORTED_FORMATS_CONFIG,
    PRIVATE_FALLBACK_CONFIG,
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
