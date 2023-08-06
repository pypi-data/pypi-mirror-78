.. contents:: Table of Contents


Introduction
============

`ftw.noticebaord` provides a simple structure to manage Notices in a Intranet environment.
People (Intranet users) can post and manage their Notices in this separate space.

Usage
-----

`ftw.noticebaord` comes with a predefined and ready to work with workflow:

- All Authenticated users can add new Notices in Notice Categories.
- Admins (Site Administrator / Manager) can manage the Board itself, the Categories and all Notices.
- It's possible to create multiple Boards per Plone Site

Once you installed the package and applied the profile (see install section) you can add a new Board in the Plone root.
You can make it addable wherever you wish to though.
After adding some categories the Board is ready to use. As soon as people are authenticated they are
also authorized to use the Board.


Features
--------
- New DX based content types:

    + NoticeBoard (Container for Categories)
    + NoticeCategory (Container for Notices)
    + Notice
    + NoticeImage (Custom Image DX Type - This way we can control the add permission)

- Views:

    + Noticeboard Overview which all Categories and Notices for a Category can be shown via toggle.
    + Noticeboard Overview is implemented according to https://www.w3.org/TR/wai-aria-practices/examples/accordion/accordion.html
    + Notice detail view, which shows images in a slider using `ftw.slider`
    + My notices view shows all my notices regardless if they are expired or not

- General:

    + Using collective.quickupload Upload Portlet on Notice view for multipload of images.
    + Using a customized `IPublication` behavior to define how long the Notice should be active.
    + "Terms and conditions" can be defined per Category. The User needs to accept them in order to create a new Notice.


Theming
-------

This package is implemented using ftw.themeing - So SCSS only, no default CSS for the default plone theme.


Compatibility
-------------

Plone 4.3.x


Installation
============

- Add the package to your buildout configuration:

::

    [instance]
    eggs +=
        ...
        ftw.noticeboard

- And apply `ftw.noticeboard` default profile

- Add new NoticeBoard and NoticeCategories


Technical hints:
================

This package uses `ftw.lawgiver` for the worklfow generation. It's not mandatory to use the predefined worklfow.
This package also uses `collective.deletepermission` in order to make it possible for users to delete their own Notices.
Styles are introduced with ftw.theming. So the package is right now not really styled at all, that's your job.
If you are using a ftw.theming based Theme. Like plonetheme.blueberry or plonetheme.onegovbear it will look acceptable


Development
===========

1. Fork this repo
2. Clone your fork
3. Shell: ``ln -s development.cfg buildout.cfg``
4. Shell: ``python bootstrap.py``
5. Shell: ``bin/buildout``

Run ``bin/test`` to test your changes.

Or start an instance by running ``bin/instance fg``.


Links
=====

- Github: https://github.com/4teamwork/ftw.noticeboard
- Issues: https://github.com/4teamwork/ftw.noticeboard/issues
- Pypi: http://pypi.python.org/pypi/ftw.noticeboard


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.noticeboard`` is licensed under GNU General Public License, version 2.
