import ckan.plugins as p
from ckan.tests import factories

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
