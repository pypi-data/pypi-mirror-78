.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

===========================
collective.behavior.gallery
===========================

This product allows you to display a gallery viewlet with all the images
of a folderish content type.


Features
--------

- The behavior can be defined on any folderish content type
- The thumbs shown in gallery don't show in folder content anymore to avoid duplicates
- Content files (other than pictures) are displayed in a specific viewlet, making it movable
- Gallery images open in overlay with previous / next navigation


Translations
------------

This product has been translated into

- French


Installation
------------

Install collective.behavior.gallery by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.behavior.gallery


and then running ``bin/buildout``.

You can then install the package in ``plone_control_panel`` and activate the
``FolderishGallery`` behavior on the Dexterity folderish content types you
want.


Contribute
----------

- Issue Tracker: https://github.com/IMIO/collective.behavior.gallery/issues
- Source Code: https://github.com/IMIO/collective.behavior.gallery


License
-------

The project is licensed under the GPLv2.
