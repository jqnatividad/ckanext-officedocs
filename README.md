# ckanext-officedocs

This plugin provides the option of using the [Microsoft Office Web
Viewer](https://www.microsoft.com/en-us/microsoft-365/blog/2013/04/10/office-web-viewer-view-office-documents-in-a-browser/)
for previewing both MS Office and OpenOffice documents as an
IResourceView

## Also consider ckanext-webpageviewplus

[ckanext-webpageviewplus](https://github.com/dathere/ckanext-webpageviewplus) (from version
0.7.0) shows Word, Excel and PowerPoint files through the same Microsoft viewer, as one of the
well-known services in its "Website (Plus)" view, and adds what this extension doesn't:

- a security setting per view, so the embedded viewer can't act as your CKAN site;
- a consent card, so visitors can choose before anything loads from Microsoft (each preview
  sends the visitor to Microsoft and gives Microsoft the file's address);
- a height that fits (16:9 for slides), a control bar with Open in new tab, Fullscreen (Expand
  on iPhone) and Share, lazy loading, and accessibility work;
- `ckan webpageviewplus check-views`, which lists views whose page has gone.

It needs a separate domain for uploads: Microsoft's viewer only works with its own origin, and
ckanext-webpageviewplus never gives one to an embedded page until uploads are served from a
separate domain. On sites without one, keep using this extension, which embeds the viewer
without a sandbox. Both refuse files in private datasets, which Microsoft can't fetch.

## Supported formats

By default, this plugin will attempt to preview the following formats:

> \"DOC\", \"DOCX\", \"XLS\", \"XLSX\", \"XLSB\", \"PPT\", \"PPTX\", \"PPS\",
> \"PPSX\", \"ODT\", \"ODS\", \"ODP\"

The supported formats can be configured in your CKAN configuration file:

```ini
ckanext.officedocs.supported_formats = DOC DOCX XLS XLSX XLSB PPT PPTX PPS PPSX ODT ODS ODP
```

Formats are separated by spaces and matched case-insensitively. For example,
to add macro-enabled Microsoft Office formats:

```ini
ckanext.officedocs.supported_formats = DOC DOCX DOCM XLS XLSX XLSM XLSB PPT PPTX PPTM PPS PPSX PPSM ODT ODS ODP
```

## Private package fallback

Microsoft's online viewer can only render resources that are publicly reachable,
so by default the previewer is not offered for resources in private datasets.

You can opt in to a client-side fallback for private resources:

```ini
ckanext.officedocs.enable_private_fallback = true
```

When enabled, private Office resources show a fallback panel instead of the
online viewer:

- On a Chromium-based browser (Chrome, Edge, Brave, Opera), the panel offers an
  "Open document" link and suggests installing an Office viewer extension
  ([Office](https://chromewebstore.google.com/detail/office/ndjpnladcallmjemlbaebfadecfhkepb)
  or [Office Editing for Docs, Sheets & Slides](https://chromewebstore.google.com/detail/office-editing-for-docs-s/gbkeegbaiigmenfmjfclcdgdpimamgkj)).
  With such an extension installed, opening the document renders it in the
  browser using the viewer's own session, which can reach the private resource.
- On other browsers (Firefox, Safari), the panel explains that previewing
  private files requires a Chromium-based browser with one of those extensions.

Note: browser extensions cannot be detected from a web page, so the fallback
always shows the tip/link rather than auto-detecting whether an extension is
present.

## Viewer height

The height of the Office viewer iframe (used for public resources) is
configurable:

```ini
ckanext.officedocs.iframe_height = 400px
```

Any valid CSS length is accepted (e.g. `600px`, `75vh`). Defaults to `400px`.

## Configuration reference

All options are declared via CKAN's config declaration, so you can inspect
them with `ckan config declaration officedocs` and validate your config with
`ckan config validate`.

| Option | Default | Description |
| --- | --- | --- |
| `ckanext.officedocs.supported_formats` | `DOC DOCX XLS XLSX XLSB PPT PPTX PPS PPSX ODT ODS ODP` | Space-separated formats to preview (case-insensitive). |
| `ckanext.officedocs.enable_private_fallback` | `false` | Enable the Chromium fallback preview for private resources. |
| `ckanext.officedocs.iframe_height` | `400px` | CSS height of the public-resource viewer iframe. |

## Installation

To install ckanext-officedocs:

1.  Clone this repository into the place where you normally install
    extensions, by default this will be /usr/lib/ckan/default/src/

2.  Activate your CKAN virtual environment, for example:

        . /usr/lib/ckan/default/bin/activate

3.  Install the ckanext-officedocs Python package into your virtual
    environment:

        cd ckanext-officedocs
        python setup.py install

4.  Add `officedocs_view` to the `ckan.plugins` setting in your CKAN
    config file (by default the config file is located at
    `/etc/ckan/default/production.ini`).

5.  If you wish for views to be created automatically for you, then you
    should add `officedocs_view` to the end of the
    `ckan.views.default_views` option in your config file.

    > ckan.views.default\_views = \... officedocs\_view

6.  Restart CKAN. For example if you\'ve deployed CKAN with Apache on
    Ubuntu:

        sudo service apache2 reload

    or if you\'re using `supervisor`:

        sudo supervisorctl restart ckan-uwsgi:\*

## FAQ

Q: It doesn\'t work, my documents aren\'t previewing

A: For the Microsoft online viewer to work, the documents to be previewed must be
accessible to the wider internet (i.e. the Dataset Package is PUBLIC, not PRIVATE), 
and will only work if you use a hostname, and not just an IP address. To preview
private resources, see the [Private package fallback](#private-package-fallback)
section above.
