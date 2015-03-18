=============
ckanext-officedocs
=============

This plugin provides the option of using the Microsoft Office viewer for
previewing content as an IResourceView


------------
Installation
------------

To install ckanext-officedocs:

1. Clone this repository into the place where you normally install extensions,
   by default this will be /usr/lib/ckan/default/src/

2. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

3. Install the ckanext-gdoc Python package into your virtual environment::

     cd ckanext-officedocs
     python setup.py install

3. Add ``officedocs_view`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload

