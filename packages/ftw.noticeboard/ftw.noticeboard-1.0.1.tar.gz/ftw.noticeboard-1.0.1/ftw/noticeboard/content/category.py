from ftw.noticeboard import _
from plone.app.textfield import RichText
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import Interface


class INoticeCategory(Interface):
    """Marker interface for the Notice category"""


class INoticeCategorySchema(model.Schema):
    """A Folderish type for notices categories, which holds notices"""

    conditions = RichText(
        title=_(u'label_conditions', default=u'Terms and Conditions'),
        description=_(u'description_conditions',
                      default=u'Those conditions needs to be accepted for posting in this category'),
        required=True,
        allowed_mime_types=('text/html',)
    )


class NoticeCategory(Container):
    implements(INoticeCategory)


alsoProvides(INoticeCategory, IFormFieldProvider)
