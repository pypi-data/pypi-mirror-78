from collective.quickupload.portlet.quickuploadportlet import Assignment
from plone.app.portlets.storage import PortletAssignmentMapping
from plone.portlets.constants import CONTENT_TYPE_CATEGORY
from plone.portlets.interfaces import IPortletManager
from zope.component import getUtility


def add_quickupload_portlet(portal):
    # Do not set up quickupload portlet in profile's portlet.xml.
    # The Form provided there does not work without a actual request.
    # Thus we avoid to setup the portlet in tests.
    # Note to future me: If you ever wanna reliable produce a segmentation fault,
    # just remove the condition :-D
    return
    if portal.REQUEST.URL not in ['http://foo', 'http://nohost']:
        manager = getUtility(IPortletManager, name='plone.rightcolumn')
        category = manager.get(CONTENT_TYPE_CATEGORY)
        portal_type = 'ftw.noticeboard.Notice'

        mapping = category.get(portal_type, None)

        if mapping is None:
            mapping = mapping[portal_type] = PortletAssignmentMapping(
                manager=manager,
                category=CONTENT_TYPE_CATEGORY,
                name=portal_type)

        if 'quickupload' not in mapping:
            portlet = Assignment(
                header='Upload',
                upload_portal_type='ftw.noticeboard.NoticeImage',
                upload_media_type='image'
            )
            mapping['quickupload'] = portlet
