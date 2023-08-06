from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implements
from zope.interface import Interface


class INoticeBoard(Interface):
    """Marker interface for the NoticeBoard"""


class INoticeBoardSchema(model.Schema):
    """A Folderish type for notice categories with a specific workflow"""


class NoticeBoard(Container):
    implements(INoticeBoard)
