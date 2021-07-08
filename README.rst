=============
ckanext-officedocs
=============

This plugin provides the option of using the `Microsoft Online Doc Viewer <https://products.office.com/en/office-online/view-office-documents-online>`_ for
previewing both MS Office and OpenOffice documents as an IResourceView

------------
Supported formats
------------

This plugin will attempt to preview the following formats

    "DOC", "DOCX", "XLS", "XLSX", "PPT", "PPTX", "PPS", "ODT", "ODS", "ODP"

------------
Installation
------------

To install ckanext-officedocs:

1. Clone this repository into the place where you normally install extensions,
   by default this will be /usr/lib/ckan/default/src/

2. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

3. Install the ckanext-officedocs Python package into your virtual environment::

     cd ckanext-officedocs
     python setup.py install

4. Add ``officedocs_view`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).
   
5. If you wish for views to be created automatically for you, then you should 
   add ``officedocs_view`` to the end of the ``ckan.views.default_views`` option in your 
   config file.

      ckan.views.default_views = ... officedocs_view

6. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


------------
FAQ
------------
Q: It doesn't work, my documents aren't previewing

A: For this extension to work, the documents to be previewed must be accessible to the
wider internet, and will only work if you use a hostname, and not just an IP address.
