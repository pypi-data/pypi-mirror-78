from ftw.noticeboard import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.content import Item
from plone.supermodel import model
from plone.supermodel.directives import primary
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import Interface
from plone.namedfile.field import NamedBlobImage


class INoticeImage(Interface):
    """Marker interface for the NoticeImage"""


class INoticeImageSchema(model.Schema):

    primary('image')
    image = NamedBlobImage(
        title=_(u'label_image', default=u'Image'),
        required=True
    )


class NoticeImage(Item):
    implements(INoticeImage)


alsoProvides(INoticeImageSchema, IFormFieldProvider)
